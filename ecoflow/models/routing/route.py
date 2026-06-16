# -*- coding: utf-8 -*-
import math

from odoo import api, fields, models
from odoo.exceptions import UserError


def _haversine_km(lat1, lng1, lat2, lng2):
    """Great-circle distance in km between two WGS84 points."""
    if None in (lat1, lng1, lat2, lng2):
        return 0.0
    radius = 6371.0
    d_lat = math.radians(lat2 - lat1)
    d_lng = math.radians(lng2 - lng1)
    a = (
        math.sin(d_lat / 2) ** 2
        + math.cos(math.radians(lat1))
        * math.cos(math.radians(lat2))
        * math.sin(d_lng / 2) ** 2
    )
    return 2 * radius * math.asin(math.sqrt(a))


class EcoflowRoute(models.Model):
    _name = "ecoflow.route"
    _description = "Collection Route"
    _inherit = ["mail.thread"]
    _order = "date desc, id desc"

    name = fields.Char(
        string="Reference", required=True, copy=False, default="New", readonly=True
    )
    date = fields.Date(required=True, default=fields.Date.context_today, tracking=True)
    zone_id = fields.Many2one("ecoflow.zone", string="Zone", tracking=True)
    vehicle_id = fields.Many2one("fleet.vehicle", string="Vehicle", tracking=True)
    driver_id = fields.Many2one("res.partner", string="Driver", tracking=True)
    state = fields.Selection(
        [
            ("draft", "Draft"),
            ("planned", "Planned"),
            ("dispatched", "Dispatched"),
            ("done", "Completed"),
            ("cancel", "Cancelled"),
        ],
        default="draft",
        required=True,
        tracking=True,
    )
    stop_ids = fields.One2many("ecoflow.route.stop", "route_id", string="Stops")
    stop_count = fields.Integer(compute="_compute_stats", store=True)
    planned_distance = fields.Float(
        string="Planned Distance (km)", compute="_compute_stats", store=True
    )
    depot_lat = fields.Float(string="Depot Latitude", digits=(10, 7))
    depot_lng = fields.Float(string="Depot Longitude", digits=(10, 7))

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get("name") or vals.get("name") == "New":
                vals["name"] = self.env["ir.sequence"].next_by_code(
                    "ecoflow.route"
                ) or "New"
        return super().create(vals_list)

    @api.depends("stop_ids", "stop_ids.distance_from_prev")
    def _compute_stats(self):
        for route in self:
            route.stop_count = len(route.stop_ids)
            route.planned_distance = sum(
                route.stop_ids.mapped("distance_from_prev")
            )

    def action_load_orders(self):
        """Pull scheduled, unrouted service orders for the route's zone/date."""
        self.ensure_one()
        domain = [
            ("state", "=", "scheduled"),
            ("route_stop_id", "=", False),
        ]
        if self.zone_id:
            domain.append(("zone_id", "=", self.zone_id.id))
        if self.date:
            domain.append(("scheduled_date", "=", self.date))
        orders = self.env["ecoflow.service.order"].search(domain)
        if not orders:
            raise UserError("No unrouted scheduled orders match this route.")
        Stop = self.env["ecoflow.route.stop"]
        seq = len(self.stop_ids)
        for order in orders:
            seq += 1
            stop = Stop.create(
                {
                    "route_id": self.id,
                    "sequence": seq,
                    "order_id": order.id,
                }
            )
            order.write({"route_stop_id": stop.id, "state": "assigned"})
        return True

    def action_optimize(self):
        """Nearest-neighbour sequencing from the depot using Haversine distance."""
        self.ensure_one()
        stops = self.stop_ids.filtered(lambda s: s.geo_lat and s.geo_lng)
        if not stops:
            raise UserError("Stops need site coordinates to be optimized.")
        remaining = list(stops)
        cur_lat, cur_lng = self.depot_lat, self.depot_lng
        ordered = []
        # If no depot set, start from the first stop.
        if not (cur_lat and cur_lng):
            first = remaining.pop(0)
            first.write({"sequence": 1, "distance_from_prev": 0.0})
            ordered.append(first)
            cur_lat, cur_lng = first.geo_lat, first.geo_lng
        seq = len(ordered)
        while remaining:
            nearest = min(
                remaining,
                key=lambda s: _haversine_km(cur_lat, cur_lng, s.geo_lat, s.geo_lng),
            )
            seq += 1
            dist = _haversine_km(cur_lat, cur_lng, nearest.geo_lat, nearest.geo_lng)
            nearest.write({"sequence": seq, "distance_from_prev": dist})
            ordered.append(nearest)
            remaining.remove(nearest)
            cur_lat, cur_lng = nearest.geo_lat, nearest.geo_lng
        self.state = "planned"
        return True

    def action_dispatch(self):
        self.write({"state": "dispatched"})

    def action_complete(self):
        for route in self:
            route.stop_ids.mapped("order_id").filtered(
                lambda o: o.state == "assigned"
            )
            route.state = "done"

    def action_cancel(self):
        self.write({"state": "cancel"})


class EcoflowRouteStop(models.Model):
    _name = "ecoflow.route.stop"
    _description = "Route Stop"
    _order = "route_id, sequence"

    route_id = fields.Many2one(
        "ecoflow.route", string="Route", required=True, ondelete="cascade"
    )
    sequence = fields.Integer(default=10)
    order_id = fields.Many2one(
        "ecoflow.service.order", string="Service Order", required=True
    )
    site_id = fields.Many2one(
        related="order_id.site_id", store=True, readonly=True, string="Site"
    )
    geo_lat = fields.Float(related="order_id.site_id.geo_lat", store=True, readonly=True)
    geo_lng = fields.Float(related="order_id.site_id.geo_lng", store=True, readonly=True)
    distance_from_prev = fields.Float(string="Leg Distance (km)", readonly=True)
    service_state = fields.Selection(
        related="order_id.state", string="Order Status", readonly=True
    )

    def action_service_done(self):
        """Mark the stop's order serviced and create a proof event."""
        Event = self.env["ecoflow.service.event"]
        for stop in self:
            Event.register_service(stop.order_id, status="serviced")
        return True
