# -*- coding: utf-8 -*-
{
    "name": "ECOFLOW Base",
    "version": "18.0.1.0.0",
    "summary": "Shared foundation for the ECOFLOW environmental operations ERP",
    "description": """
ECOFLOW Base
============
Shared masters and configuration for the ECOFLOW waste-management suite:
waste streams, materials, service zones, bins/containers and partner
(service-site) extensions. Compatible with Odoo 18.0 and 19.0.
""",
    "author": "SA Systems",
    "maintainer": "SA Systems",
    "website": "https://sasystems.solutions/custom-web-app-development",
    "support": "info@sasystems.solutions",
    "category": "Industries",
    "license": "OPL-1",
    "price": 10.00,
    "currency": "USD",
    "depends": ["base", "mail", "stock"],
    "data": [
        "security/ecoflow_security.xml",
        "security/ir.model.access.csv",
        "data/ecoflow_base_data.xml",
        "views/waste_stream_views.xml",
        "views/material_views.xml",
        "views/zone_views.xml",
        "views/bin_views.xml",
        "views/partner_views.xml",
        "views/ecoflow_menus.xml",
    ],
    "demo": [
        "demo/ecoflow_base_demo.xml",
    ],
    "images": ["static/description/banner.png"],
    "application": True,
    "installable": True,
}
