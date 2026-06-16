# -*- coding: utf-8 -*-
from odoo import fields, models


class EcoflowServiceOrder(models.Model):
    _inherit = "ecoflow.service.order"

    route_stop_id = fields.Many2one(
        "ecoflow.route.stop", string="Route Stop", readonly=True, copy=False
    )
    route_id = fields.Many2one(
        related="route_stop_id.route_id", store=True, readonly=True, string="Route"
    )
