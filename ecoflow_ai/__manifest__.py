# -*- coding: utf-8 -*-
{
    "name": "ECOFLOW AI Intelligence",
    "version": "18.0.1.0.0",
    "category": "Industries",
    "summary": "AI-powered demand forecasting, smart dispatch, anomaly "
               "detection and operational insights for ECOFLOW.",
    "description": """
ECOFLOW AI Intelligence
=======================

Adds an on-premise, privacy-first intelligence layer to ECOFLOW:

* Demand forecasting per zone & waste stream (trend + seasonality)
* Predictive bin fill-levels and smart collection recommendations
* Route efficiency scoring and savings estimation
* Anomaly detection (contamination, mass-balance drift, missed-pickup spikes)
* AI Insights engine with plain-language recommendations
* Region-aware intelligence (regulatory framework & units per region)

No data leaves your server. All models are deterministic and explainable.
""",
    "author": "SA Systems",
    "maintainer": "SA Systems",
    "website": "https://sasystems.solutions/custom-web-app-development",
    "support": "info@sasystems.solutions",
    "license": "OPL-1",
    "price": 0.00,
    "currency": "USD",
    "depends": [
        "ecoflow_dashboard",
    ],
    "data": [
        "security/ir.model.access.csv",
        "data/ai_data.xml",
        "views/ai_insight_views.xml",
        "views/ai_forecast_views.xml",
        "views/bin_prediction_views.xml",
        "views/res_config_settings_views.xml",
        "views/ai_center_action.xml",
        "views/ai_menus.xml",
    ],
    "demo": [
        "demo/ai_demo.xml",
    ],
    "assets": {
        "web.assets_backend": [
            "ecoflow_ai/static/src/scss/ai_center.scss",
            "ecoflow_ai/static/src/js/ai_center.js",
            "ecoflow_ai/static/src/xml/ai_center.xml",
        ],
    },
    "images": ["static/description/banner.png"],
    "installable": True,
    "application": False,
    "auto_install": False,
}
