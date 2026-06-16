# -*- coding: utf-8 -*-
"""Global and region-specific configuration for ECOFLOW AI.

Regions tailor the platform to local regulatory frameworks, measurement units
and language of waste codes. The selected region drives defaults used across
the AI layer (e.g. how impact is labelled) and is exposed to the cockpit.
"""
from odoo import api, fields, models

PARAM_REGION = "ecoflow.region"
PARAM_UNITS = "ecoflow.unit_system"
PARAM_FORECAST_HORIZON = "ecoflow.forecast_horizon"
PARAM_FULL_THRESHOLD = "ecoflow.bin_full_threshold"
PARAM_AI_ENABLED = "ecoflow.ai_enabled"
PARAM_DEFAULT_CURRENCY = "ecoflow.default_currency_id"

# Region -> (regulatory framework label, default unit system, default currency)
REGION_PROFILES = {
    "global": ("Generic / ISO", "metric", "USD"),
    "eu": ("EU Waste Framework Directive (EWC)", "metric", "EUR"),
    "uk": ("UK Environment Agency (EWC)", "metric", "GBP"),
    "us": ("US EPA / RCRA", "imperial", "USD"),
    "au": ("Australia NEPM / EPA", "metric", "AUD"),
    "gcc": ("GCC / MENA Environmental Regs", "metric", "AED"),
    "in": ("India CPCB / SWM Rules", "metric", "INR"),
}


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    ecoflow_region = fields.Selection(
        [("global", "Global / Generic"),
         ("eu", "European Union"),
         ("uk", "United Kingdom"),
         ("us", "United States"),
         ("au", "Australia"),
         ("gcc", "GCC / Middle East"),
         ("in", "India")],
        string="Operating Region", default="global",
        config_parameter=PARAM_REGION,
        help="Tailors regulatory framework, units and waste-code language.")
    ecoflow_unit_system = fields.Selection(
        [("metric", "Metric (kg, km)"),
         ("imperial", "Imperial (lb, mi)")],
        string="Unit System", default="metric",
        config_parameter=PARAM_UNITS)
    ecoflow_default_currency_id = fields.Many2one(
        "res.currency", string="Default Currency",
        config_parameter=PARAM_DEFAULT_CURRENCY,
        help="Platform-wide default currency for ECOFLOW pricing and "
             "recovered-value figures. Suggested from the operating region; "
             "every record stays individually multi-currency.")
    ecoflow_regulatory_framework = fields.Char(
        string="Regulatory Framework", compute="_compute_framework",
        readonly=True)
    ecoflow_ai_enabled = fields.Boolean(
        string="Enable AI Intelligence", default=True,
        config_parameter=PARAM_AI_ENABLED,
        help="Master switch for forecasting, predictions and insights.")
    ecoflow_forecast_horizon = fields.Integer(
        string="Forecast Horizon (days)", default=7,
        config_parameter=PARAM_FORECAST_HORIZON)
    ecoflow_bin_full_threshold = fields.Float(
        string="Bin Full Threshold %", default=90.0,
        config_parameter=PARAM_FULL_THRESHOLD)

    @api.depends("ecoflow_region")
    def _compute_framework(self):
        for rec in self:
            profile = REGION_PROFILES.get(rec.ecoflow_region or "global")
            rec.ecoflow_regulatory_framework = profile[0] if profile else ""

    @api.onchange("ecoflow_region")
    def _onchange_region(self):
        """Align the unit system and currency with the chosen region."""
        profile = REGION_PROFILES.get(self.ecoflow_region or "global")
        if profile:
            self.ecoflow_unit_system = profile[1]
            currency = self.env["res.currency"].search(
                [("name", "=", profile[2])], limit=1)
            if currency:
                self.ecoflow_default_currency_id = currency

    def action_run_ai_now(self):
        """Convenience button: run the full AI pipeline immediately."""
        self.env["ecoflow.ai.insight"].sudo()._cron_generate()
        return {
            "type": "ir.actions.client",
            "tag": "display_notification",
            "params": {
                "title": "ECOFLOW AI",
                "message": "Forecasts, predictions and insights refreshed.",
                "type": "success",
                "sticky": False,
            },
        }
