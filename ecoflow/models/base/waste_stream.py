# -*- coding: utf-8 -*-
from odoo import api, fields, models


class EcoflowWasteStream(models.Model):
    _name = "ecoflow.waste.stream"
    _description = "Waste Stream"
    _order = "name"

    name = fields.Char(required=True)
    code = fields.Char(required=True, copy=False)
    hazard_class = fields.Selection(
        [
            ("none", "Non-hazardous"),
            ("low", "Low Hazard"),
            ("medium", "Medium Hazard"),
            ("high", "High Hazard"),
        ],
        default="none",
        required=True,
    )
    recyclable = fields.Boolean(default=False)
    color = fields.Integer(string="Color Index")
    default_waste_code = fields.Char(string="Default Regulatory Code")
    active = fields.Boolean(default=True)
    note = fields.Text()

    _sql_constraints = [
        ("code_uniq", "unique(code)", "The waste stream code must be unique."),
    ]

    @api.depends("name", "code")
    def _compute_display_name(self):
        for rec in self:
            rec.display_name = "[%s] %s" % (rec.code or "", rec.name or "")
