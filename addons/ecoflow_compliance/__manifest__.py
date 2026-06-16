# -*- coding: utf-8 -*-
{
    "name": "ECOFLOW Compliance",
    # Series-agnostic version so the module installs on Odoo 18 and 19
    # alike (a "19.0.x" string is rejected by Odoo 18, and vice-versa).
    # Odoo prefixes the running series automatically, so this reports as
    # 1.0 on whichever series is running.
    "version": "1.0.0",
    "summary": "Waste codes, electronic manifests and permit register",
    "description": """
ECOFLOW Compliance
==================
Regulatory waste-code library, electronic chain-of-custody manifests built
from service events, and a permit register with expiry tracking. Compatible
with Odoo 18.0 and 19.0.
""",
    "author": "SA Systems",
    "maintainer": "SA Systems",
    "website": "https://sasystems.solutions/custom-web-app-development",
    "support": "info@sasystems.solutions",
    "category": "Industries",
    "license": "OPL-1",
    "price": 5.00,
    "currency": "USD",
    "depends": ["ecoflow_collection", "fleet"],
    "data": [
        "security/ir.model.access.csv",
        "data/compliance_data.xml",
        "views/waste_code_views.xml",
        "views/manifest_views.xml",
        "views/permit_views.xml",
        "views/compliance_menus.xml",
    ],
    "demo": [
        "demo/compliance_demo.xml",
    ],
    "images": ["static/description/banner.png"],
    "application": False,
    "installable": True,
}
