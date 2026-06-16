# -*- coding: utf-8 -*-
from odoo import fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    is_service_site = fields.Boolean(string="Is a Service Site")
    ecoflow_zone_id = fields.Many2one("ecoflow.zone", string="Service Zone")
    access_notes = fields.Text(string="Access Notes")
    gate_code = fields.Char(string="Gate / Access Code")
    geo_lat = fields.Float(string="Latitude", digits=(10, 7))
    geo_lng = fields.Float(string="Longitude", digits=(10, 7))
    bin_ids = fields.One2many("ecoflow.bin", "site_id", string="Bins")
    bin_count = fields.Integer(string="Bin Count", compute="_compute_bin_count")

    def _compute_bin_count(self):
        data = self.env["ecoflow.bin"].read_group(
            [("site_id", "in", self.ids)], ["site_id"], ["site_id"]
        )
        mapped = {d["site_id"][0]: d["site_id_count"] for d in data}
        for rec in self:
            rec.bin_count = mapped.get(rec.id, 0)
