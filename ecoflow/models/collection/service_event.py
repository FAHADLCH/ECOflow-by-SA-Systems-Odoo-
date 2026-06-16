# -*- coding: utf-8 -*-
from odoo import api, fields, models


class EcoflowServiceEvent(models.Model):
    _name = "ecoflow.service.event"
    _description = "Proof-of-Service Event"
    _order = "timestamp desc"

    name = fields.Char(string="Reference", compute="_compute_name", store=True)
    order_id = fields.Many2one("ecoflow.service.order", string="Service Order")
    bin_id = fields.Many2one("ecoflow.bin", string="Bin")
    site_id = fields.Many2one(
        related="order_id.site_id", store=True, readonly=True, string="Site"
    )
    timestamp = fields.Datetime(default=fields.Datetime.now, required=True)
    geo_lat = fields.Float(string="Latitude", digits=(10, 7))
    geo_lng = fields.Float(string="Longitude", digits=(10, 7))
    status = fields.Selection(
        [
            ("serviced", "Serviced"),
            ("blocked", "Blocked Access"),
            ("contaminated", "Contaminated"),
            ("overweight", "Overweight"),
            ("missed", "Missed"),
        ],
        default="serviced",
        required=True,
    )
    photo = fields.Image(string="Proof Photo", max_width=1024, max_height=1024)
    net_weight = fields.Float(string="Captured Weight (kg)")
    note = fields.Char()

    @api.depends("bin_id", "timestamp")
    def _compute_name(self):
        for rec in self:
            ref = rec.bin_id.name or "EVT"
            rec.name = "%s @ %s" % (ref, rec.timestamp or "")

    @api.model
    def register_service(self, order, status="serviced", weight=0.0, geo=None):
        """Create an event and reflect it on the order + bin. Idempotent-ish helper."""
        vals = {
            "order_id": order.id,
            "bin_id": order.bin_id.id,
            "status": status,
            "net_weight": weight,
        }
        if geo:
            vals.update({"geo_lat": geo.get("lat"), "geo_lng": geo.get("lng")})
        event = self.create(vals)
        if status == "serviced":
            order.write({"state": "done", "event_id": event.id})
            if order.bin_id:
                order.bin_id.write(
                    {"last_serviced": event.timestamp, "fill_level": 0.0}
                )
        elif status == "missed":
            order.write({"state": "missed", "event_id": event.id})
        return event
