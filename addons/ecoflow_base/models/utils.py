# -*- coding: utf-8 -*-
"""Shared helpers for the ECOFLOW suite."""

# Configuration parameter holding the platform-wide default currency id.
# Set from the ECOFLOW settings panel; falls back to the company currency.
PARAM_DEFAULT_CURRENCY = "ecoflow.default_currency_id"


def ecoflow_default_currency(env):
    """Resolve the default currency for ECOFLOW monetary fields.

    Honours the regional/platform default currency configured in settings and
    falls back to the active company currency, keeping the suite multi-currency
    by design.
    """
    param = env["ir.config_parameter"].sudo().get_param(PARAM_DEFAULT_CURRENCY)
    if param:
        try:
            currency = env["res.currency"].browse(int(param)).exists()
        except (TypeError, ValueError):
            currency = None
        if currency:
            return currency
    return env.company.currency_id
