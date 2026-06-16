# -*- coding: utf-8 -*-
from odoo import fields, models

from odoo.addons.ecoflow_base.models.utils import ecoflow_default_currency


class EcoflowService(models.Model):
    _name = "ecoflow.service"
    _description = "Collection Service"
    _order = "name"

    name = fields.Char(required=True)
    code = fields.Char(required=True, copy=False)
    waste_stream_id = fields.Many2one(
        "ecoflow.waste.stream", string="Waste Stream", required=True
    )
    container_type = fields.Selection(
        [
            ("wheelie", "Wheelie Bin"),
            ("skip", "Skip"),
            ("rolloff", "Roll-off"),
            ("compactor", "Compactor"),
            ("fel", "Front-end Loader"),
        ],
        default="wheelie",
    )
    billing_method = fields.Selection(
        [
            ("flat", "Flat per Service"),
            ("lift", "Per Lift"),
            ("weight", "Per Tonne"),
        ],
        default="flat",
        required=True,
    )
    currency_id = fields.Many2one(
        "res.currency",
        string="Currency",
        default=lambda self: ecoflow_default_currency(self.env),
    )
    unit_price = fields.Monetary(
        string="Unit Price", currency_field="currency_id"
    )
    sla_hours = fields.Integer(string="SLA (hours)", default=24)
    active = fields.Boolean(default=True)

    _sql_constraints = [
        ("code_uniq", "unique(code)", "The service code must be unique."),
    ]
