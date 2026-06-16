# -*- coding: utf-8 -*-
from odoo import api, fields, models


class EcoflowPermit(models.Model):
    _name = "ecoflow.permit"
    _description = "Permit / Licence"
    _inherit = ["mail.thread"]
    _order = "valid_to"

    name = fields.Char(string="Permit No.", required=True, copy=False)
    permit_type = fields.Selection(
        [
            ("operating", "Operating Licence"),
            ("transport", "Transport Permit"),
            ("site", "Site Permit"),
            ("driver", "Driver Certification"),
        ],
        default="operating",
        required=True,
    )
    holder_id = fields.Many2one("res.partner", string="Holder")
    vehicle_id = fields.Many2one("fleet.vehicle", string="Vehicle")
    scope = fields.Char()
    valid_from = fields.Date(required=True, default=fields.Date.context_today)
    valid_to = fields.Date(required=True, tracking=True)
    state = fields.Selection(
        [
            ("valid", "Valid"),
            ("expiring", "Expiring Soon"),
            ("expired", "Expired"),
        ],
        compute="_compute_state",
        store=True,
    )
    days_to_expiry = fields.Integer(
        compute="_compute_state", store=True, string="Days to Expiry"
    )
    active = fields.Boolean(default=True)

    @api.depends("valid_to")
    def _compute_state(self):
        today = fields.Date.context_today(self)
        expiry_window = int(
            self.env["ir.config_parameter"]
            .sudo()
            .get_param("ecoflow.permit_expiry_days", 30)
        )
        for rec in self:
            if not rec.valid_to:
                rec.state = "valid"
                rec.days_to_expiry = 0
                continue
            delta = (rec.valid_to - today).days
            rec.days_to_expiry = delta
            if delta < 0:
                rec.state = "expired"
            elif delta <= expiry_window:
                rec.state = "expiring"
            else:
                rec.state = "valid"

    @api.model
    def _cron_check_expiry(self):
        """Scheduled: recompute states and post activities for expiring permits."""
        permits = self.search([("active", "=", True)])
        permits._compute_state()
        for permit in permits.filtered(lambda p: p.state == "expiring"):
            permit.message_post(
                body="Permit %s expires in %s day(s)."
                % (permit.name, permit.days_to_expiry)
            )
        return True
