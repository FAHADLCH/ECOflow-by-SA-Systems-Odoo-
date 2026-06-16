# -*- coding: utf-8 -*-
"""Extends the cockpit data provider with AI KPIs and chart series."""
from datetime import timedelta

from odoo import api, models, fields


class EcoflowDashboard(models.AbstractModel):
    _inherit = "ecoflow.dashboard"

    @api.model
    def get_ai_kpis(self):
        """Return AI-layer KPIs and chart-ready series for the cockpit."""
        Insight = self.env["ecoflow.ai.insight"].sudo()
        Pred = self.env["ecoflow.bin.prediction"].sudo()
        Fc = self.env["ecoflow.ai.forecast"].sudo()

        critical = Insight.search_count([("severity", "=", "critical")])
        warnings = Insight.search_count([("severity", "=", "warning")])
        opportunities = Insight.search_count([("severity", "=", "opportunity")])
        collect_now = Pred.search_count([("recommendation", "=", "collect_now")])

        insights = Insight.search([], limit=6)
        insight_cards = [{
            "id": i.id,
            "name": i.name,
            "description": i.description or "",
            "recommendation": i.recommendation or "",
            "category": i.category,
            "severity": i.severity,
            "impact_label": i.impact_label or "",
            "confidence": i.confidence,
            "icon": i.icon or "fa-lightbulb-o",
            "action_xmlid": i.action_xmlid or "",
        } for i in insights]

        # 7-day demand forecast (total predicted collections per day)
        forecast_points = Fc.search([], order="forecast_date asc")
        bucket = {}
        for p in forecast_points:
            key = fields.Date.to_string(p.forecast_date)
            bucket[key] = bucket.get(key, 0.0) + p.predicted_orders
        forecast_labels = sorted(bucket.keys())[:7]
        forecast_series = [round(bucket[k], 1) for k in forecast_labels]

        # 14-day actual collections (for the trend chart)
        Order = self.env["ecoflow.service.order"].sudo()
        today = fields.Date.context_today(self)
        actual_labels, actual_done, actual_missed = [], [], []
        for d in range(13, -1, -1):
            day = today - timedelta(days=d)
            actual_labels.append(fields.Date.to_string(day))
            actual_done.append(Order.search_count(
                [("scheduled_date", "=", day), ("state", "=", "done")]))
            actual_missed.append(Order.search_count(
                [("scheduled_date", "=", day), ("state", "=", "missed")]))

        # recovery mix by stream (recovered kg) for a doughnut
        Batch = self.env["ecoflow.process.batch"].sudo()
        done = Batch.search([("state", "=", "done")])
        mix = {}
        for b in done:
            label = b.waste_stream_id.name or "Other"
            mix[label] = mix.get(label, 0.0) + b.recovered_kg
        mix_labels = list(mix.keys())
        mix_values = [round(v, 0) for v in mix.values()]

        return {
            "critical": critical,
            "warnings": warnings,
            "opportunities": opportunities,
            "collect_now": collect_now,
            "insights": insight_cards,
            "charts": {
                "forecast": {"labels": forecast_labels, "data": forecast_series},
                "actual": {
                    "labels": actual_labels,
                    "done": actual_done,
                    "missed": actual_missed,
                },
                "recovery_mix": {"labels": mix_labels, "data": mix_values},
            },
        }
