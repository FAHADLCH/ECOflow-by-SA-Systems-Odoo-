# -*- coding: utf-8 -*-
from odoo import fields, models


class EcoflowZone(models.Model):
    _name = "ecoflow.zone"
    _description = "Service Zone"
    _order = "name"

    name = fields.Char(required=True)
    code = fields.Char(copy=False)
    depot_id = fields.Many2one("res.partner", string="Depot / Base")
    color = fields.Integer(string="Color Index")
    active = fields.Boolean(default=True)
    note = fields.Text()
