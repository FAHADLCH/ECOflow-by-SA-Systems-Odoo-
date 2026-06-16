# -*- coding: utf-8 -*-
"""Predictive bin fill-level model for smart, demand-driven collection."""
from odoo import api, fields, models

from . import ai_engine

# Default assumed daily fill gain (%) when a bin has no measured history.
DEFAULT_DAILY_GAIN = 12.0
FULL_THRESHOLD = 90.0


class EcoflowBinPrediction(models.Model):
    _name = "ecoflow.bin.prediction"
    _description = "Predictive Bin Fill Level"
    _order = "days_to_full asc, predicted_fill desc"

    name = fields.Char(compute="_compute_name", store=True)
    bin_id = fields.Many2one(
        "ecoflow.bin", string="Bin", required=True, ondelete="cascade")
    site_id = fields.Many2one(
        related="bin_id.site_id", store=True, string="Site")
    zone_id = fields.Many2one(
        related="bin_id.zone_id", store=True, string="Zone")
    waste_stream_id = fields.Many2one(
        related="bin_id.waste_stream_id", store=True, string="Stream")
    current_fill = fields.Float(string="Current Fill %")
    daily_gain = fields.Float(string="Avg Daily Gain %")
    predicted_fill = fields.Float(string="Predicted Fill % (3d)")
    days_to_full = fields.Integer(string="Days to Full")
    recommendation = fields.Selection(
        [("collect_now", "Collect Now"),
         ("schedule_soon", "Schedule Soon"),
         ("monitor", "Monitor"),
         ("defer", "Defer")],
        default="monitor")
    priority_score = fields.Integer(string="Priority", help="0-100 urgency")
    generated_on = fields.Datetime(default=fields.Datetime.now, readonly=True)

    @api.depends("bin_id", "recommendation")
    def _compute_name(self):
        for rec in self:
            rec.name = "%s — %s" % (
                rec.bin_id.name or "Bin",
                dict(self._fields["recommendation"].selection).get(
                    rec.recommendation, ""))

    # ------------------------------------------------------------------
    @api.model
    def _estimate_daily_gain(self, ecobin):
        """Estimate a bin's daily fill gain from its service cadence.

        Uses the bin's linked service SLA window as a proxy when no telemetry
        history exists: a tighter SLA implies faster filling.
        """
        # crude but explainable: 100% over the typical days between services
        cadence = 7.0
        order = self.env["ecoflow.service.order"].sudo().search(
            [("bin_id", "=", ecobin.id)], order="scheduled_date desc", limit=2)
        if len(order) == 2:
            delta = abs((order[0].scheduled_date - order[1].scheduled_date).days)
            if delta:
                cadence = float(delta)
        return round(100.0 / cadence, 2) if cadence else DEFAULT_DAILY_GAIN

    @api.model
    def generate(self):
        """Recompute predictions for all in-service bins. Returns row count."""
        Bin = self.env["ecoflow.bin"].sudo()
        bins = Bin.search([("status", "=", "in_service")])
        self.sudo().search([]).unlink()
        rows = []
        for ecobin in bins:
            current = ecobin.fill_level or 0.0
            gain = self._estimate_daily_gain(ecobin) or DEFAULT_DAILY_GAIN
            pred3 = ai_engine.project_fill_level(current, gain, 3)
            dtf = ai_engine.days_until_full(current, gain, FULL_THRESHOLD)

            if current >= FULL_THRESHOLD or dtf <= 0:
                rec, score = "collect_now", 100
            elif dtf <= 1:
                rec, score = "collect_now", 90
            elif dtf <= 3:
                rec, score = "schedule_soon", 70
            elif dtf <= 6:
                rec, score = "monitor", 40
            else:
                rec, score = "defer", 15

            rows.append({
                "bin_id": ecobin.id,
                "current_fill": round(current, 1),
                "daily_gain": gain,
                "predicted_fill": round(pred3, 1),
                "days_to_full": dtf,
                "recommendation": rec,
                "priority_score": score,
            })
        if rows:
            self.sudo().create(rows)
        return len(rows)

    @api.model
    def action_generate_predictions(self):
        self.generate()
        return {
            "type": "ir.actions.act_window",
            "name": "Predictive Bin Fill",
            "res_model": "ecoflow.bin.prediction",
            "view_mode": "list,graph,pivot",
            "target": "current",
        }

    def action_create_service_order(self):
        """Turn a 'collect now' recommendation into a scheduled service order."""
        Order = self.env["ecoflow.service.order"].sudo()
        Service = self.env["ecoflow.service"].sudo()
        created = self.env["ecoflow.service.order"]
        for rec in self:
            if not rec.bin_id.site_id:
                continue
            service = Service.search(
                [("waste_stream_id", "=", rec.waste_stream_id.id)], limit=1)
            if not service:
                service = Service.search([], limit=1)
            if not service:
                continue
            order = Order.create({
                "site_id": rec.bin_id.site_id.id,
                "service_id": service.id,
                "bin_id": rec.bin_id.id,
                "scheduled_date": fields.Date.context_today(self),
                "priority": "2" if rec.priority_score >= 90 else "1",
                "state": "scheduled",
            })
            created |= order
        if created:
            return {
                "type": "ir.actions.act_window",
                "name": "Generated Service Orders",
                "res_model": "ecoflow.service.order",
                "view_mode": "list,form",
                "domain": [("id", "in", created.ids)],
                "target": "current",
            }
        return {"type": "ir.actions.act_window_close"}
