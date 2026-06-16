# -*- coding: utf-8 -*-
from odoo import api, fields, models


class EcoflowBin(models.Model):
    _name = "ecoflow.bin"
    _description = "Bin / Container Asset"
    _inherit = ["mail.thread"]
    _order = "name"

    name = fields.Char(string="Reference", required=True, copy=False, default="New")
    rfid_tag = fields.Char(string="RFID Tag", copy=False, tracking=True)
    serial = fields.Char(string="Serial Number", copy=False)
    bin_type = fields.Selection(
        [
            ("wheelie", "Wheelie Bin"),
            ("skip", "Skip"),
            ("rolloff", "Roll-off"),
            ("compactor", "Compactor"),
            ("fel", "Front-end Loader"),
        ],
        default="wheelie",
        required=True,
    )
    capacity_l = fields.Float(string="Capacity (L)")
    waste_stream_id = fields.Many2one("ecoflow.waste.stream", string="Waste Stream")
    site_id = fields.Many2one("res.partner", string="Service Site", tracking=True)
    zone_id = fields.Many2one("ecoflow.zone", string="Zone")
    status = fields.Selection(
        [
            ("stock", "In Stock"),
            ("in_service", "In Service"),
            ("suspended", "Suspended"),
            ("maintenance", "Maintenance"),
            ("retired", "Retired"),
        ],
        default="stock",
        required=True,
        tracking=True,
    )
    fill_level = fields.Float(string="Fill Level (%)")
    last_serviced = fields.Datetime(string="Last Serviced", readonly=True)
    active = fields.Boolean(default=True)

    _sql_constraints = [
        ("rfid_uniq", "unique(rfid_tag)", "The RFID tag must be unique."),
    ]

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get("name") or vals.get("name") == "New":
                vals["name"] = self.env["ir.sequence"].next_by_code(
                    "ecoflow.bin"
                ) or "New"
        return super().create(vals_list)

    def _set_in_service(self, site):
        for rec in self:
            rec.write({"status": "in_service", "site_id": site.id})
