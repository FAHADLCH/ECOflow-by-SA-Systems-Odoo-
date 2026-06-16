# -*- coding: utf-8 -*-
from odoo import api, fields, models

PARAM_TOLERANCE = "ecoflow.mass_balance_tolerance"
PARAM_PERMIT_DAYS = "ecoflow.permit_expiry_days"
PARAM_TARGET_DIVERSION = "ecoflow.target_diversion_rate"

DEFAULT_TOLERANCE = 0.02
DEFAULT_PERMIT_DAYS = 30
DEFAULT_TARGET_DIVERSION = 75.0


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    ecoflow_mass_balance_tolerance = fields.Float(
        string="Mass Balance Tolerance",
        help="Allowed deviation (as a fraction, e.g. 0.02 = 2%) between "
        "process batch input and recovered + residual output.",
        config_parameter=PARAM_TOLERANCE,
        default=DEFAULT_TOLERANCE,
    )
    ecoflow_permit_expiry_days = fields.Integer(
        string="Permit Expiry Window (days)",
        help="A permit is flagged as 'Expiring Soon' when its remaining "
        "validity falls within this many days.",
        config_parameter=PARAM_PERMIT_DAYS,
        default=DEFAULT_PERMIT_DAYS,
    )
    ecoflow_target_diversion_rate = fields.Float(
        string="Target Diversion Rate (%)",
        help="Organisation-wide diversion target used on the operations "
        "cockpit to colour the diversion KPI.",
        config_parameter=PARAM_TARGET_DIVERSION,
        default=DEFAULT_TARGET_DIVERSION,
    )
