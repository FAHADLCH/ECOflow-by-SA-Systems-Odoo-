# -*- coding: utf-8 -*-
{
    "name": "ECOFLOW Dashboard & Branding",
    # Series-agnostic version so the module installs on Odoo 18 and 19
    # alike (a "19.0.x" string is rejected by Odoo 18, and vice-versa).
    # Odoo prefixes the running series automatically, so this reports as
    # 1.0 on whichever series is running.
    "version": "1.0.0",
    "summary": "SA Systems branded cockpit, KPI dashboards, graphical reporting and settings",
    "description": """
ECOFLOW Dashboard & Branding
============================
Adds the SA Systems branded operations cockpit, KPI tiles, graphical
analysis (graph + pivot) across collection, routing, recycling and
compliance, plus a central configuration panel for operational thresholds.
Compatible with Odoo 18.0 and 19.0.
""",
    "author": "SA Systems",
    "maintainer": "SA Systems",
    "website": "https://sasystems.solutions/custom-web-app-development",
    "support": "info@sasystems.solutions",
    "category": "Industries",
    "license": "OPL-1",
    "price": 5.00,
    "currency": "USD",
    "depends": [
        "web",
        "ecoflow_collection",
        "ecoflow_routing",
        "ecoflow_recycling",
        "ecoflow_compliance",
    ],
    "data": [
        "data/branding_data.xml",
        "views/res_config_settings_views.xml",
        "views/reporting_views.xml",
        "views/dashboard_menus.xml",
    ],
    "assets": {
        "web.assets_backend": [
            "ecoflow_dashboard/static/src/scss/ecoflow.scss",
            "ecoflow_dashboard/static/src/js/cockpit.js",
            "ecoflow_dashboard/static/src/xml/cockpit.xml",
        ],
    },
    "demo": [
        "demo/cockpit_demo.xml",
    ],
    "images": ["static/description/banner.png"],
    "application": True,
    "installable": True,
}
