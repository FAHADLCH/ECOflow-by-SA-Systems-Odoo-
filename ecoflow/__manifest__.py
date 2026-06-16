# -*- coding: utf-8 -*-
{
    "name": "ECOFLOW Waste Management",
    "version": "18.0.1.0.0",
    "summary": "AI-native ERP for waste collection, routing, recovery and "
               "compliance — one integrated suite.",
    "description": """
ECOFLOW Waste Management
========================
A complete, AI-native ERP for environmental-services operators, delivered as a
single application. ECOFLOW covers the full operational lifecycle:

* **Masters** — waste streams, recoverable materials, service zones and a
  bin / container registry, with multi-currency commodity pricing.
* **Collection** — service catalog (flat / per-lift / per-tonne), service
  orders and proof-of-service capture (RFID + geo + photo).
* **Routing** — daily route plans, nearest-neighbour stop sequencing and
  vehicle / driver dispatch.
* **Recycling** — weighbridge tickets, MRF process batches with mass-balance
  checks, recovered outputs and diversion / recovery yield.
* **Compliance** — regulatory waste-code library, electronic chain-of-custody
  manifests and a permit register with expiry tracking.
* **Cockpit & analytics** — a branded operations cockpit, KPI tiles and
  graph / pivot reporting across every domain.
* **AI intelligence** — on-premise, privacy-first demand forecasting,
  predictive bin fill-levels, route efficiency scoring, anomaly detection and a
  plain-language insights engine. No data leaves your server.

Region-aware throughout (regulatory framework, units and default currency).
Compatible with Odoo Community and Enterprise.
""",
    "author": "SA Systems",
    "maintainer": "SA Systems",
    "website": "https://sasystems.solutions/custom-web-app-development",
    "support": "info@sasystems.solutions",
    "category": "Industries",
    "license": "OPL-1",
    "price": 299.00,
    "currency": "USD",
    "depends": ["base", "mail", "stock", "fleet", "web"],
    "data": [
        "security/ecoflow_security.xml",
        "security/ir.model.access.csv",
        "data/base/ecoflow_base_data.xml",
        "views/base/waste_stream_views.xml",
        "views/base/material_views.xml",
        "views/base/zone_views.xml",
        "views/base/bin_views.xml",
        "views/base/partner_views.xml",
        "views/base/ecoflow_menus.xml",
        "data/collection/collection_data.xml",
        "views/collection/service_views.xml",
        "views/collection/service_order_views.xml",
        "views/collection/service_event_views.xml",
        "views/collection/collection_menus.xml",
        "data/routing/routing_data.xml",
        "views/routing/route_views.xml",
        "views/routing/service_order_views.xml",
        "views/routing/routing_menus.xml",
        "data/recycling/recycling_data.xml",
        "views/recycling/weigh_ticket_views.xml",
        "views/recycling/process_batch_views.xml",
        "views/recycling/recycling_menus.xml",
        "data/compliance/compliance_data.xml",
        "views/compliance/waste_code_views.xml",
        "views/compliance/manifest_views.xml",
        "views/compliance/permit_views.xml",
        "views/compliance/compliance_menus.xml",
        "data/dashboard/branding_data.xml",
        "views/dashboard/res_config_settings_views.xml",
        "views/dashboard/reporting_views.xml",
        "views/dashboard/dashboard_menus.xml",
        "data/ai/ai_data.xml",
        "views/ai/ai_insight_views.xml",
        "views/ai/ai_forecast_views.xml",
        "views/ai/bin_prediction_views.xml",
        "views/ai/res_config_settings_views.xml",
        "views/ai/ai_center_action.xml",
        "views/ai/ai_menus.xml",
    ],
    "assets": {
        "web.assets_backend": [
            "ecoflow/static/src/scss/ecoflow.scss",
            "ecoflow/static/src/js/cockpit.js",
            "ecoflow/static/src/xml/cockpit.xml",
            "ecoflow/static/src/scss/ai_center.scss",
            "ecoflow/static/src/js/ai_center.js",
            "ecoflow/static/src/xml/ai_center.xml",
        ],
    },
    "demo": [
        "demo/base/ecoflow_base_demo.xml",
        "demo/collection/collection_demo.xml",
        "demo/recycling/recycling_demo.xml",
        "demo/compliance/compliance_demo.xml",
        "demo/dashboard/cockpit_demo.xml",
        "demo/ai/ai_demo.xml",
    ],
    "images": ["static/description/banner.png"],
    "application": True,
    "installable": True,
}
