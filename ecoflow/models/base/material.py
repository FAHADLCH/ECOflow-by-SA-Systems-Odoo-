# -*- coding: utf-8 -*-
from odoo import fields, models

from .utils import ecoflow_default_currency


class EcoflowMaterial(models.Model):
    _name = "ecoflow.material"
    _description = "Recoverable Material / Commodity"
    _order = "name"

    name = fields.Char(required=True)
    code = fields.Char(required=True, copy=False)
    waste_stream_id = fields.Many2one("ecoflow.waste.stream", string="Source Stream")
    grade = fields.Char()
    currency_id = fields.Many2one(
        "res.currency",
        string="Currency",
        default=lambda self: ecoflow_default_currency(self.env),
    )
    market_price = fields.Monetary(
        string="Market Price / Tonne", currency_field="currency_id"
    )
    uom_name = fields.Char(string="Unit", default="kg")
    active = fields.Boolean(default=True)

    _sql_constraints = [
        ("code_uniq", "unique(code)", "The material code must be unique."),
    ]
