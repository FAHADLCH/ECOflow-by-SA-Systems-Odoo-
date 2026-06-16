# -*- coding: utf-8 -*-
"""AI Insights: scans operations and emits plain-language recommendations.

This is the explainable 'AI' surface customers see first. Each insight has a
category, severity, a human title/description, an impact estimate and an
optional deep-link action. Insights are regenerated on demand and by a daily
cron, and are surfaced both as records and on the cockpit.
"""
from datetime import timedelta

from odoo import api, fields, models

from . import ai_engine

SEVERITY = [
    ("critical", "Critical"),
    ("warning", "Warning"),
    ("opportunity", "Opportunity"),
    ("info", "Info"),
]
CATEGORY = [
    ("collection", "Collection"),
    ("routing", "Routing"),
    ("recovery", "Recovery"),
    ("compliance", "Compliance"),
    ("demand", "Demand"),
]


class EcoflowAiInsight(models.Model):
    _name = "ecoflow.ai.insight"
    _description = "AI Operational Insight"
    _order = "severity_rank asc, impact_value desc, create_date desc"

    name = fields.Char(string="Insight", required=True)
    description = fields.Text()
    recommendation = fields.Text(string="Recommended Action")
    category = fields.Selection(CATEGORY, required=True, default="collection")
    severity = fields.Selection(SEVERITY, required=True, default="info")
    severity_rank = fields.Integer(compute="_compute_rank", store=True)
    impact_value = fields.Float(
        string="Estimated Impact", help="Indicative magnitude for ranking.")
    impact_label = fields.Char(string="Impact")
    confidence = fields.Integer(string="Confidence %", default=80)
    action_xmlid = fields.Char(string="Action XML ID")
    icon = fields.Char(default="fa-lightbulb-o")
    generated_on = fields.Datetime(default=fields.Datetime.now, readonly=True)

    @api.depends("severity")
    def _compute_rank(self):
        order = {"critical": 0, "warning": 1, "opportunity": 2, "info": 3}
        for rec in self:
            rec.severity_rank = order.get(rec.severity, 9)

    # ------------------------------------------------------------------
    # Analyzers — each returns a list of insight dicts
    # ------------------------------------------------------------------
    @api.model
    def _insight_missed_collections(self):
        Order = self.env["ecoflow.service.order"].sudo()
        today = fields.Date.context_today(self)
        since = today - timedelta(days=14)
        # daily missed counts over the trailing window
        series = []
        cur = since
        while cur <= today:
            cnt = Order.search_count([
                ("scheduled_date", "=", cur), ("state", "=", "missed")])
            series.append(float(cnt))
            cur += timedelta(days=1)
        out = []
        if sum(series) == 0:
            return out
        zscores = ai_engine.robust_zscores(series)
        if zscores and zscores[-1] >= 2.0 and series[-1] > 0:
            out.append({
                "name": "Missed-collection spike detected today",
                "description": (
                    "Today's missed collections (%d) are well above the "
                    "14-day norm. This usually signals an access, vehicle or "
                    "staffing issue on a specific route." % int(series[-1])),
                "recommendation": (
                    "Review today's missed orders and re-dispatch before "
                    "SLA breach; check the affected zone for access problems."),
                "category": "collection",
                "severity": "critical",
                "impact_value": series[-1] * 100,
                "impact_label": "%d at-risk SLAs" % int(series[-1]),
                "confidence": 85,
                "action_xmlid": "ecoflow_collection.action_service_order",
                "icon": "fa-exclamation-triangle",
            })
        return out

    @api.model
    def _insight_diversion_gap(self):
        Batch = self.env["ecoflow.process.batch"].sudo()
        done = Batch.search([("state", "=", "done")])
        if not done:
            return []
        total_in = sum(done.mapped("input_kg"))
        total_rec = sum(done.mapped("recovered_kg"))
        if total_in <= 0:
            return []
        diversion = total_rec / total_in * 100
        target = float(self.env["ir.config_parameter"].sudo().get_param(
            "ecoflow.target_diversion_rate", 75.0))
        if diversion + 0.5 < target:
            gap = target - diversion
            return [{
                "name": "Diversion rate below target",
                "description": (
                    "Current diversion is %.1f%% against a %.0f%% target. "
                    "Closing the gap improves both compliance posture and "
                    "commodity revenue." % (diversion, target)),
                "recommendation": (
                    "Audit residual streams in recent batches for "
                    "mis-sorted recyclables; tighten inbound contamination "
                    "checks at the gate."),
                "category": "recovery",
                "severity": "warning",
                "impact_value": gap * 50,
                "impact_label": "%.1f%% to target" % gap,
                "confidence": 82,
                "action_xmlid": "ecoflow_recycling.action_process_batch",
                "icon": "fa-recycle",
            }]
        return [{
            "name": "Diversion target achieved",
            "description": (
                "Diversion is %.1f%%, at or above the %.0f%% target. "
                "Strong recovery performance." % (diversion, target)),
            "recommendation": (
                "Maintain current sorting discipline and consider raising "
                "the diversion target to lock in the gain."),
            "category": "recovery",
            "severity": "opportunity",
            "impact_value": (diversion - target) * 10,
            "impact_label": "+%.1f%% over target" % (diversion - target),
            "confidence": 88,
            "action_xmlid": "ecoflow_recycling.action_process_batch",
            "icon": "fa-trophy",
        }]

    @api.model
    def _insight_mass_balance(self):
        Batch = self.env["ecoflow.process.batch"].sudo()
        bad = Batch.search([("state", "=", "done"), ("balance_ok", "=", False)])
        if not bad:
            return []
        return [{
            "name": "Mass-balance drift on completed batches",
            "description": (
                "%d completed batch(es) closed outside the configured "
                "mass-balance tolerance. This can indicate weighing errors "
                "or unrecorded outputs." % len(bad)),
            "recommendation": (
                "Re-check scale calibration and recovery-output entries for "
                "the flagged batches."),
            "category": "recovery",
            "severity": "warning",
            "impact_value": len(bad) * 60,
            "impact_label": "%d batches" % len(bad),
            "confidence": 80,
            "action_xmlid": "ecoflow_recycling.action_process_batch",
            "icon": "fa-balance-scale",
        }]

    @api.model
    def _insight_permits(self):
        Permit = self.env["ecoflow.permit"].sudo()
        expired = Permit.search_count([("state", "=", "expired")])
        expiring = Permit.search_count([("state", "=", "expiring")])
        out = []
        if expired:
            out.append({
                "name": "Expired permits in force",
                "description": (
                    "%d permit(s) have expired. Operating against an expired "
                    "licence is a serious regulatory exposure." % expired),
                "recommendation": "Suspend affected activity and renew immediately.",
                "category": "compliance",
                "severity": "critical",
                "impact_value": expired * 200,
                "impact_label": "%d expired" % expired,
                "confidence": 99,
                "action_xmlid": "ecoflow_compliance.action_permit",
                "icon": "fa-id-card",
            })
        if expiring:
            out.append({
                "name": "Permits expiring soon",
                "description": (
                    "%d permit(s) fall inside the renewal window. Start "
                    "renewals now to avoid a lapse." % expiring),
                "recommendation": "Begin renewal paperwork for expiring permits.",
                "category": "compliance",
                "severity": "warning",
                "impact_value": expiring * 90,
                "impact_label": "%d expiring" % expiring,
                "confidence": 95,
                "action_xmlid": "ecoflow_compliance.action_permit",
                "icon": "fa-calendar-times-o",
            })
        return out

    @api.model
    def _insight_smart_collection(self):
        Pred = self.env["ecoflow.bin.prediction"].sudo()
        urgent = Pred.search([("recommendation", "=", "collect_now")])
        if not urgent:
            return []
        return [{
            "name": "Bins predicted to overflow",
            "description": (
                "%d bin(s) are at or near capacity based on predicted fill "
                "rates. Collecting them now prevents overflow and missed "
                "revenue." % len(urgent)),
            "recommendation": (
                "Generate priority service orders for the flagged bins from "
                "the Predictive Bin Fill view."),
            "category": "collection",
            "severity": "warning",
            "impact_value": len(urgent) * 80,
            "impact_label": "%d bins" % len(urgent),
            "confidence": 78,
            "action_xmlid": "ecoflow_ai.action_bin_prediction",
            "icon": "fa-trash",
        }]

    @api.model
    def _insight_demand_trend(self):
        Fc = self.env["ecoflow.ai.forecast"].sudo()
        rising = Fc.search([("trend", "=", "rising")], limit=1)
        if not rising:
            return []
        zones = Fc.search([("trend", "=", "rising")]).mapped("zone_id.name")
        zones = list(dict.fromkeys([z for z in zones if z]))[:3]
        if not zones:
            return []
        return [{
            "name": "Rising collection demand forecast",
            "description": (
                "Demand is trending up in: %s. Capacity may need adjusting "
                "in the coming week." % ", ".join(zones)),
            "recommendation": (
                "Pre-plan extra routes or shifts for the affected zones."),
            "category": "demand",
            "severity": "opportunity",
            "impact_value": 120,
            "impact_label": "%d zone(s)" % len(zones),
            "confidence": 75,
            "action_xmlid": "ecoflow_ai.action_ai_forecast",
            "icon": "fa-line-chart",
        }]

    # ------------------------------------------------------------------
    @api.model
    def generate(self):
        """Run all analyzers and replace the insight set. Returns row count."""
        analyzers = [
            self._insight_permits,
            self._insight_missed_collections,
            self._insight_diversion_gap,
            self._insight_mass_balance,
            self._insight_smart_collection,
            self._insight_demand_trend,
        ]
        rows = []
        for fn in analyzers:
            try:
                rows.extend(fn())
            except Exception:  # an analyzer must never break the whole run
                continue
        self.sudo().search([]).unlink()
        if rows:
            self.sudo().create(rows)
        return len(rows)

    @api.model
    def _cron_generate(self):
        """Daily refresh: forecasts, predictions, then insights."""
        self.env["ecoflow.ai.forecast"].sudo().generate()
        self.env["ecoflow.bin.prediction"].sudo().generate()
        self.generate()

    @api.model
    def action_refresh_insights(self):
        self.env["ecoflow.ai.forecast"].sudo().generate()
        self.env["ecoflow.bin.prediction"].sudo().generate()
        self.generate()
        return {
            "type": "ir.actions.act_window",
            "name": "AI Insights",
            "res_model": "ecoflow.ai.insight",
            "view_mode": "kanban,list,form",
            "target": "current",
        }

    def action_open_target(self):
        """Open the deep-link action attached to this insight, if any."""
        self.ensure_one()
        if not self.action_xmlid:
            return False
        try:
            return self.env["ir.actions.act_window"]._for_xml_id(
                self.action_xmlid)
        except Exception:
            return False
