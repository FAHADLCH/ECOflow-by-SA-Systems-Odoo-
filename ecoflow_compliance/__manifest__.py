# -*- coding: utf-8 -*-
{
    "name": "ECOFLOW Compliance",
    "version": "19.0.1.0.0",
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
    "price": 10.00,
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
