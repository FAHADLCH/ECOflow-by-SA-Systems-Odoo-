# -*- coding: utf-8 -*-
from odoo import api, fields, models


class EcoflowDashboard(models.AbstractModel):
    _name = "ecoflow.dashboard"
    _description = "ECOFLOW Operations Dashboard Data Provider"

    @api.model
    def get_kpis(self):
        """Return aggregated KPIs for the operations cockpit.

        Reads are done with sudo() because this is a read-only aggregate
        dashboard surfaced to any internal user who can open the cockpit.
        """
        today = fields.Date.context_today(self)
        order = self.env["ecoflow.service.order"].sudo()
        route = self.env["ecoflow.route"].sudo()
        batch = self.env["ecoflow.process.batch"].sudo()
        ticket = self.env["ecoflow.weigh.ticket"].sudo()
        permit = self.env["ecoflow.permit"].sudo()
        manifest = self.env["ecoflow.manifest"].sudo()

        orders_today = order.search([("scheduled_date", "=", today)])
        done_today = orders_today.filtered(lambda o: o.state == "done")
        missed_today = orders_today.filtered(lambda o: o.state == "missed")
        completion = (
            len(done_today) / len(orders_today) * 100.0 if orders_today else 0.0
        )

        active_routes = route.search(
            [("state", "in", ("planned", "dispatched"))]
        )
        planned_distance = sum(active_routes.mapped("planned_distance"))

        done_batches = batch.search([("state", "=", "done")])
        total_input = sum(done_batches.mapped("input_kg"))
        total_recovered = sum(done_batches.mapped("recovered_kg"))
        diversion = (
            total_recovered / total_input * 100.0 if total_input else 0.0
        )

        posted_tickets = ticket.search([("state", "=", "posted")])
        tonnes_handled = sum(posted_tickets.mapped("net_weight")) / 1000.0

        expiring_permits = permit.search_count([("state", "=", "expiring")])
        expired_permits = permit.search_count([("state", "=", "expired")])
        open_manifests = manifest.search_count(
            [("state", "in", ("draft", "generated", "transit"))]
        )

        get_param = self.env["ir.config_parameter"].sudo().get_param
        target_diversion = float(
            get_param("ecoflow.target_diversion_rate", 75.0)
        )

        return {
            "orders_today": len(orders_today),
            "orders_done": len(done_today),
            "orders_missed": len(missed_today),
            "completion_rate": round(completion, 1),
            "active_routes": len(active_routes),
            "planned_distance": round(planned_distance, 1),
            "diversion_rate": round(diversion, 1),
            "target_diversion": round(target_diversion, 1),
            "tonnes_handled": round(tonnes_handled, 1),
            "recovered_kg": round(total_recovered, 0),
            "expiring_permits": expiring_permits,
            "expired_permits": expired_permits,
            "open_manifests": open_manifests,
        }
