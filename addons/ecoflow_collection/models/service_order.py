# -*- coding: utf-8 -*-
from odoo import api, fields, models


class EcoflowServiceOrder(models.Model):
    _name = "ecoflow.service.order"
    _description = "Service Order"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "scheduled_date desc, id desc"

    name = fields.Char(
        string="Reference", required=True, copy=False, default="New", readonly=True
    )
    site_id = fields.Many2one(
        "res.partner", string="Service Site", required=True, tracking=True
    )
    service_id = fields.Many2one(
        "ecoflow.service", string="Service", required=True, tracking=True
    )
    bin_id = fields.Many2one("ecoflow.bin", string="Bin")
    waste_stream_id = fields.Many2one(
        related="service_id.waste_stream_id", store=True, readonly=True
    )
    zone_id = fields.Many2one(
        related="site_id.ecoflow_zone_id", store=True, readonly=True, string="Zone"
    )
    scheduled_date = fields.Date(
        string="Scheduled", required=True, default=fields.Date.context_today, tracking=True
    )
    priority = fields.Selection(
        [("0", "Normal"), ("1", "High"), ("2", "Urgent")],
        default="0",
    )
    state = fields.Selection(
        [
            ("draft", "Draft"),
            ("scheduled", "Scheduled"),
            ("assigned", "Assigned"),
            ("done", "Serviced"),
            ("missed", "Missed"),
            ("cancel", "Cancelled"),
        ],
        default="draft",
        required=True,
        tracking=True,
    )
    event_id = fields.Many2one(
        "ecoflow.service.event", string="Service Event", readonly=True
    )

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get("name") or vals.get("name") == "New":
                vals["name"] = self.env["ir.sequence"].next_by_code(
                    "ecoflow.service.order"
                ) or "New"
        return super().create(vals_list)

    def action_schedule(self):
        self.write({"state": "scheduled"})

    def action_cancel(self):
        self.write({"state": "cancel"})

    def action_reset(self):
        self.write({"state": "draft"})

    def action_mark_missed(self):
        self.write({"state": "missed"})
