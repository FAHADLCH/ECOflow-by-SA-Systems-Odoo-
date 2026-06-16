# -*- coding: utf-8 -*-
"""AI demand forecast for collections, by zone and waste stream."""
from datetime import date, timedelta

from odoo import api, fields, models

from . import ai_engine

# How many days of history to learn from, and how far ahead to project.
HISTORY_DAYS = 60
DEFAULT_HORIZON = 7


class EcoflowAiForecast(models.Model):
    _name = "ecoflow.ai.forecast"
    _description = "AI Demand Forecast"
    _order = "forecast_date asc, zone_id, waste_stream_id"

    name = fields.Char(compute="_compute_name", store=True)
    run_id = fields.Char(
        string="Run Reference", index=True,
        help="Identifier shared by all rows produced in one generation run.")
    zone_id = fields.Many2one("ecoflow.zone", string="Zone", ondelete="cascade")
    waste_stream_id = fields.Many2one(
        "ecoflow.waste.stream", string="Waste Stream", ondelete="cascade")
    forecast_date = fields.Date(required=True, index=True)
    horizon_day = fields.Integer(string="Day Ahead")
    predicted_orders = fields.Float(string="Predicted Collections")
    lower_bound = fields.Float()
    upper_bound = fields.Float()
    trend = fields.Selection(
        [("rising", "Rising"), ("stable", "Stable"), ("falling", "Falling")],
        default="stable")
    generated_on = fields.Datetime(default=fields.Datetime.now, readonly=True)

    @api.depends("zone_id", "waste_stream_id", "forecast_date")
    def _compute_name(self):
        for rec in self:
            parts = []
            if rec.zone_id:
                parts.append(rec.zone_id.name)
            if rec.waste_stream_id:
                parts.append(rec.waste_stream_id.name)
            label = " · ".join(parts) or "All zones"
            rec.name = "%s — %s" % (label, rec.forecast_date or "")

    # ------------------------------------------------------------------
    # Generation
    # ------------------------------------------------------------------
    @api.model
    def _collect_history(self, zone, stream, since):
        """Return ``[(date, count)]`` of completed/scheduled orders per day."""
        Order = self.env["ecoflow.service.order"].sudo()
        domain = [("scheduled_date", ">=", since)]
        if zone:
            domain.append(("zone_id", "=", zone.id))
        if stream:
            domain.append(("waste_stream_id", "=", stream.id))
        groups = Order.read_group(
            domain, ["scheduled_date"], ["scheduled_date:day"], lazy=False)
        counts = {}
        for g in groups:
            raw = g.get("scheduled_date:day")
            if not raw:
                continue
            # Odoo returns a label like "16 Jun 2026"; fall back to range key.
            d = g.get("__range", {}).get("scheduled_date:day", {}).get("from")
            if d:
                d = fields.Date.to_date(d)
            else:
                d = fields.Date.context_today(self)
            counts[d] = counts.get(d, 0) + g.get("__count", 0)
        # densify: fill missing days with 0 so the series is evenly spaced
        series = []
        cur = since
        today = fields.Date.context_today(self)
        while cur <= today:
            series.append((cur, float(counts.get(cur, 0))))
            cur += timedelta(days=1)
        return series

    @api.model
    def generate(self, horizon=DEFAULT_HORIZON):
        """Regenerate forecasts for every active zone × recyclable-aware stream.

        Returns the number of forecast rows written.
        """
        since = fields.Date.context_today(self) - timedelta(days=HISTORY_DAYS)
        zones = self.env["ecoflow.zone"].sudo().search([("active", "=", True)])
        streams = self.env["ecoflow.waste.stream"].sudo().search(
            [("active", "=", True)])
        run_ref = fields.Datetime.now().strftime("RUN-%Y%m%d%H%M%S")

        # wipe previous forecasts so the table always reflects the latest run
        self.sudo().search([]).unlink()

        rows = []
        # one combined series per (zone, stream) that actually has history
        for zone in zones:
            for stream in streams:
                history = self._collect_history(zone, stream, since)
                if sum(v for _, v in history) == 0:
                    continue
                slope, _ = ai_engine.linear_trend([v for _, v in history])
                label = ai_engine.trend_label(slope)
                points = ai_engine.forecast_series(history, horizon=horizon)
                for i, p in enumerate(points, start=1):
                    rows.append({
                        "run_id": run_ref,
                        "zone_id": zone.id,
                        "waste_stream_id": stream.id,
                        "forecast_date": p["date"],
                        "horizon_day": i,
                        "predicted_orders": p["value"],
                        "lower_bound": p["lower"],
                        "upper_bound": p["upper"],
                        "trend": label,
                    })
        if rows:
            self.sudo().create(rows)
        return len(rows)

    @api.model
    def action_generate_forecast(self):
        """UI entry point: regenerate and reopen the list."""
        self.generate()
        return {
            "type": "ir.actions.act_window",
            "name": "AI Demand Forecast",
            "res_model": "ecoflow.ai.forecast",
            "view_mode": "graph,pivot,list",
            "target": "current",
        }
