# -*- coding: utf-8 -*-
from odoo import fields, models


class EcoflowWasteCode(models.Model):
    _name = "ecoflow.waste.code"
    _description = "Regulatory Waste Code"
    _order = "code"

    name = fields.Char(string="Description", required=True)
    code = fields.Char(required=True, copy=False)
    regulator = fields.Char(help="e.g. EWC, EPA, local authority")
    hazardous = fields.Boolean(default=False)
    waste_stream_id = fields.Many2one("ecoflow.waste.stream", string="Waste Stream")
    active = fields.Boolean(default=True)

    _sql_constraints = [
        ("code_uniq", "unique(code)", "The waste code must be unique."),
    ]

    def _compute_display_name(self):
        for rec in self:
            rec.display_name = "[%s] %s" % (rec.code or "", rec.name or "")
