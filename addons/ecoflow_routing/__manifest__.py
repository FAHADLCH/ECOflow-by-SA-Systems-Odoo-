# -*- coding: utf-8 -*-
{
    "name": "ECOFLOW Routing",
    # Series-agnostic version so the module installs on Odoo 18 and 19
    # alike (a "19.0.x" string is rejected by Odoo 18, and vice-versa).
    # Odoo prefixes the running series automatically, so this reports as
    # 1.0 on whichever series is running.
    "version": "1.0.0",
    "summary": "Route plans, stop sequencing and dispatch for collection",
    "description": """
ECOFLOW Routing
===============
Daily route plans, ordered stops built from service orders, vehicle/driver
assignment and a nearest-neighbour stop sequencer. Compatible with Odoo
18.0 and 19.0.
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
        "data/routing_data.xml",
        "views/route_views.xml",
        "views/service_order_views.xml",
        "views/routing_menus.xml",
    ],
    "images": ["static/description/banner.png"],
    "application": False,
    "installable": True,
}
