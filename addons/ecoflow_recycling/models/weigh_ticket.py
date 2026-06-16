# -*- coding: utf-8 -*-
from odoo import api, fields, models


class EcoflowWeighTicket(models.Model):
    _name = "ecoflow.weigh.ticket"
    _description = "Weigh Ticket"
    _inherit = ["mail.thread"]
    _order = "timestamp desc"

    name = fields.Char(
        string="Ticket", required=True, copy=False, default="New", readonly=True
    )
    direction = fields.Selection(
        [("inbound", "Inbound"), ("outbound", "Outbound")],
        default="inbound",
        required=True,
    )
    source = fields.Selection(
        [
            ("event", "Collection Event"),
            ("gate", "Gate Weigh"),
            ("transfer", "Transfer"),
        ],
        default="gate",
        required=True,
    )
    event_id = fields.Many2one("ecoflow.service.event", string="Service Event")
    waste_stream_id = fields.Many2one(
        "ecoflow.waste.stream", string="Waste Stream", required=True
    )
    facility_id = fields.Many2one("res.partner", string="Facility")
    vehicle_id = fields.Many2one("fleet.vehicle", string="Vehicle")
    gross_weight = fields.Float(string="Gross (kg)")
    tare_weight = fields.Float(string="Tare (kg)")
    net_weight = fields.Float(
        string="Net (kg)", compute="_compute_net", store=True
    )
    timestamp = fields.Datetime(default=fields.Datetime.now, required=True)
    state = fields.Selection(
        [("draft", "Draft"), ("posted", "Posted")],
        default="draft",
        required=True,
        tracking=True,
    )

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get("name") or vals.get("name") == "New":
                vals["name"] = self.env["ir.sequence"].next_by_code(
                    "ecoflow.weigh.ticket"
                ) or "New"
        return super().create(vals_list)

    @api.depends("gross_weight", "tare_weight")
    def _compute_net(self):
        for rec in self:
            rec.net_weight = max(rec.gross_weight - rec.tare_weight, 0.0)

    def action_post(self):
        for rec in self:
            if rec.event_id and rec.net_weight:
                rec.event_id.net_weight = rec.net_weight
            rec.state = "posted"
        return True
