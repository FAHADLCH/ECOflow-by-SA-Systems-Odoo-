# -*- coding: utf-8 -*-
{
    "name": "ECOFLOW Recycling",
    "version": "18.0.1.0.0",
    "summary": "Weighbridge tickets, MRF processing, recovery and diversion",
    "description": """
ECOFLOW Recycling
=================
Captures weigh tickets, runs material-recovery process batches, records
recovered outputs and residuals, and computes diversion / recovery yield.
Compatible with Odoo 18.0 and 19.0.
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
        "data/recycling_data.xml",
        "views/weigh_ticket_views.xml",
        "views/process_batch_views.xml",
        "views/recycling_menus.xml",
    ],
    "demo": [
        "demo/recycling_demo.xml",
    ],
    "images": ["static/description/banner.png"],
    "application": False,
    "installable": True,
}
