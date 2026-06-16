# -*- coding: utf-8 -*-
from odoo import api, fields, models
from odoo.exceptions import UserError

from odoo.addons.ecoflow_base.models.utils import ecoflow_default_currency


class EcoflowProcessBatch(models.Model):
    _name = "ecoflow.process.batch"
    _description = "MRF Process Batch"
    _inherit = ["mail.thread"]
    _order = "date desc, id desc"

    name = fields.Char(
        string="Batch", required=True, copy=False, default="New", readonly=True
    )
    date = fields.Date(default=fields.Date.context_today, required=True)
    facility_id = fields.Many2one("res.partner", string="Facility")
    waste_stream_id = fields.Many2one(
        "ecoflow.waste.stream", string="Input Stream", required=True
    )
    input_kg = fields.Float(string="Input (kg)", required=True)
    residual_kg = fields.Float(string="Residual (kg)")
    recovered_kg = fields.Float(
        string="Recovered (kg)", compute="_compute_recovered", store=True
    )
    recovery_rate = fields.Float(
        string="Recovery Rate (%)", compute="_compute_recovered", store=True
    )
    output_ids = fields.One2many(
        "ecoflow.recovery.output", "batch_id", string="Recovered Outputs"
    )
    state = fields.Selection(
        [("draft", "Draft"), ("processing", "Processing"), ("done", "Done")],
        default="draft",
        required=True,
        tracking=True,
    )
    balance_ok = fields.Boolean(
        string="Mass Balance OK", compute="_compute_recovered", store=True
    )

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get("name") or vals.get("name") == "New":
                vals["name"] = self.env["ir.sequence"].next_by_code(
                    "ecoflow.process.batch"
                ) or "New"
        return super().create(vals_list)

    @api.depends("output_ids.recovered_kg", "residual_kg", "input_kg")
    def _compute_recovered(self):
        tolerance_frac = float(
            self.env["ir.config_parameter"]
            .sudo()
            .get_param("ecoflow.mass_balance_tolerance", 0.02)
        )
        for rec in self:
            recovered = sum(rec.output_ids.mapped("recovered_kg"))
            rec.recovered_kg = recovered
            rec.recovery_rate = (
                (recovered / rec.input_kg * 100.0) if rec.input_kg else 0.0
            )
            # Mass balance: recovered + residual should equal input within
            # the configured tolerance fraction.
            accounted = recovered + rec.residual_kg
            tolerance = rec.input_kg * tolerance_frac
            rec.balance_ok = abs(rec.input_kg - accounted) <= tolerance

    def action_start(self):
        self.write({"state": "processing"})

    def action_done(self):
        tolerance_pct = (
            float(
                self.env["ir.config_parameter"]
                .sudo()
                .get_param("ecoflow.mass_balance_tolerance", 0.02)
            )
            * 100.0
        )
        for rec in self:
            if not rec.balance_ok:
                raise UserError(
                    "Mass balance is out of tolerance for %s. "
                    "Recovered + residual must equal input (±%.1f%%)."
                    % (rec.name, tolerance_pct)
                )
            rec.state = "done"
        return True


class EcoflowRecoveryOutput(models.Model):
    _name = "ecoflow.recovery.output"
    _description = "Recovery Output"
    _order = "batch_id, id"

    batch_id = fields.Many2one(
        "ecoflow.process.batch", string="Batch", required=True, ondelete="cascade"
    )
    material_id = fields.Many2one(
        "ecoflow.material", string="Material", required=True
    )
    recovered_kg = fields.Float(string="Recovered (kg)", required=True)
    grade = fields.Char()
    bale_ref = fields.Char(string="Bale Reference")
    currency_id = fields.Many2one(
        "res.currency",
        string="Currency",
        default=lambda self: ecoflow_default_currency(self.env),
    )
    market_value = fields.Monetary(
        string="Est. Value",
        compute="_compute_value",
        store=True,
        currency_field="currency_id",
    )

    @api.depends("recovered_kg", "material_id.market_price")
    def _compute_value(self):
        for rec in self:
            price_per_kg = (rec.material_id.market_price or 0.0) / 1000.0
            rec.market_value = rec.recovered_kg * price_per_kg
