# -*- coding: utf-8 -*-
{
    "name": "ECOFLOW Collection",
    # Series-agnostic version so the module installs on Odoo 18 and 19
    # alike (a "19.0.x" string is rejected by Odoo 18, and vice-versa).
    # Odoo prefixes the running series automatically, so this reports as
    # 1.0 on whichever series is running.
    "version": "1.0.0",
    "summary": "Service catalog, service orders and proof-of-service capture",
    "description": """
ECOFLOW Collection
==================
Defines the collection service catalog, generates service orders (demand),
and records proof-of-service events (RFID + geo + photo). Compatible with
Odoo 18.0 and 19.0.
""",
    "author": "SA Systems",
    "maintainer": "SA Systems",
    "website": "https://sasystems.solutions/custom-web-app-development",
    "support": "info@sasystems.solutions",
    "category": "Industries",
    "license": "OPL-1",
    "price": 5.00,
    "currency": "USD",
    "depends": ["ecoflow_base"],
    "data": [
        "security/ir.model.access.csv",
        "data/collection_data.xml",
        "views/service_views.xml",
        "views/service_order_views.xml",
        "views/service_event_views.xml",
        "views/collection_menus.xml",
    ],
    "demo": [
        "demo/collection_demo.xml",
    ],
    "images": ["static/description/banner.png"],
    "application": False,
    "installable": True,
}
