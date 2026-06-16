# -*- coding: utf-8 -*-
from odoo import api, fields, models
from odoo.exceptions import UserError


class EcoflowManifest(models.Model):
    _name = "ecoflow.manifest"
    _description = "Waste Manifest (Chain of Custody)"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "date desc, id desc"

    name = fields.Char(
        string="Manifest No.", required=True, copy=False, default="New", readonly=True
    )
    date = fields.Date(default=fields.Date.context_today, required=True, tracking=True)
    generator_id = fields.Many2one(
        "res.partner", string="Generator", required=True, tracking=True
    )
    transporter_id = fields.Many2one("res.partner", string="Transporter", tracking=True)
    facility_id = fields.Many2one(
        "res.partner", string="Receiving Facility", tracking=True
    )
    waste_code_id = fields.Many2one(
        "ecoflow.waste.code", string="Waste Code", required=True
    )
    line_ids = fields.One2many("ecoflow.manifest.line", "manifest_id", string="Lines")
    total_qty = fields.Float(
        string="Total (kg)", compute="_compute_total", store=True
    )
    hazardous = fields.Boolean(related="waste_code_id.hazardous", store=True)
    state = fields.Selection(
        [
            ("draft", "Draft"),
            ("generated", "Generator Signed"),
            ("transit", "In Transit"),
            ("received", "Received"),
            ("closed", "Closed"),
            ("cancel", "Cancelled"),
        ],
        default="draft",
        required=True,
        tracking=True,
    )
    generator_sign = fields.Char(string="Generator Signature", readonly=True)
    transporter_sign = fields.Char(string="Transporter Signature", readonly=True)
    facility_sign = fields.Char(string="Facility Signature", readonly=True)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get("name") or vals.get("name") == "New":
                vals["name"] = self.env["ir.sequence"].next_by_code(
                    "ecoflow.manifest"
                ) or "New"
        return super().create(vals_list)

    @api.depends("line_ids.qty_kg")
    def _compute_total(self):
        for rec in self:
            rec.total_qty = sum(rec.line_ids.mapped("qty_kg"))

    def _sign(self, field_name):
        signature = "%s / %s" % (self.env.user.name, fields.Datetime.now())
        self.write({field_name: signature})

    def action_generator_sign(self):
        self.ensure_one()
        if not self.line_ids:
            raise UserError("Add at least one manifest line before signing.")
        self._sign("generator_sign")
        self.state = "generated"

    def action_transporter_sign(self):
        self.ensure_one()
        self._sign("transporter_sign")
        self.state = "transit"

    def action_facility_sign(self):
        self.ensure_one()
        self._sign("facility_sign")
        self.state = "received"

    def action_close(self):
        for rec in self:
            if not (rec.generator_sign and rec.facility_sign):
                raise UserError(
                    "Manifest %s needs generator and facility signatures "
                    "before closing." % rec.name
                )
            rec.state = "closed"

    def action_cancel(self):
        self.write({"state": "cancel"})


class EcoflowManifestLine(models.Model):
    _name = "ecoflow.manifest.line"
    _description = "Manifest Line"
    _order = "manifest_id, id"

    manifest_id = fields.Many2one(
        "ecoflow.manifest", string="Manifest", required=True, ondelete="cascade"
    )
    event_id = fields.Many2one("ecoflow.service.event", string="Service Event")
    waste_stream_id = fields.Many2one("ecoflow.waste.stream", string="Waste Stream")
    qty_kg = fields.Float(string="Quantity (kg)", required=True)
    container_count = fields.Integer(string="Containers", default=1)
