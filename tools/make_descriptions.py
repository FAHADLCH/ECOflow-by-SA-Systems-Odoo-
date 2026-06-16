"""Generate Odoo App Store `static/description/index.html` + `LICENSE` for each
ECOFLOW module. Self-contained, inline-styled, SA Systems branded HTML that the
Odoo Apps store renders on the product page.
"""
import os

WS = "/Users/fahad/Desktop/Odoo Apps/Waste Management System "
ADDONS = WS  # modules live at repo root (Odoo Apps Store layout)

RED = "#cc0000"
RED_HI = "#e8482c"
CHARCOAL = "#161b1c"
CHARCOAL_2 = "#1e2629"
INK = "#161b1c"
SLATE = "#5b6166"
SURFACE = "#f5f6f7"

# (title, tagline, intro, [ (icon_emoji, head, body) ... features ], [highlights] )
MODULES = {
    "ecoflow_base": {
        "title": "ECOFLOW Base",
        "tag": "The shared foundation for the ECOFLOW environmental-operations suite",
        "intro": "ECOFLOW Base provides the master data and configuration every other "
                 "ECOFLOW module builds on: waste streams, materials, service zones, "
                 "bins &amp; containers, and service-site (partner) extensions. Install it "
                 "once and the whole waste &amp; recycling platform clicks together.",
        "features": [
            ("\U0001F5C2\uFE0F", "Waste streams &amp; materials", "Model every stream (MSW, recycling, organics, C&amp;D, hazardous, e-waste) and the materials recovered from them, with codes and units."),
            ("\U0001F4CD", "Service zones", "Group sites into operational zones for routing, reporting and capacity planning."),
            ("\U0001F5D1\uFE0F", "Bins &amp; containers", "Track containers by type, capacity and location, ready for fill-level intelligence."),
            ("\U0001F465", "Service-site partners", "Extend customers/sites with environmental attributes used across collection, compliance and analytics."),
            ("\U0001F510", "Roles &amp; security", "Ships the ECOFLOW user / dispatcher / manager groups and a clean menu structure."),
            ("\u267B\uFE0F", "Built for Odoo 18 &amp; 19", "Modern list/form views, chatter, and activity tracking out of the box."),
        ],
        "highlights": ["Waste streams", "Materials", "Zones", "Bins", "Partner sites", "Security groups"],
    },
    "ecoflow_collection": {
        "title": "ECOFLOW Collection",
        "tag": "Service catalog, service orders and proof-of-service capture",
        "intro": "Turn demand into auditable work. ECOFLOW Collection defines your "
                 "collection service catalog, generates service orders, and records "
                 "proof-of-service events with RFID, geolocation and photo evidence.",
        "features": [
            ("\U0001F4CB", "Service catalog", "Define recurring and on-demand collection services per stream, container and frequency."),
            ("\U0001F9FE", "Service orders", "Generate demand as structured orders that flow into routing and recycling."),
            ("\U0001F4F8", "Proof of service", "Capture RFID scans, GPS coordinates and photos at the point of collection."),
            ("\u2705", "Status workflow", "Track each order from draft through completion with a clean, guided flow."),
            ("\U0001F4CA", "Analytics-ready", "Every event feeds the dashboards and the AI forecasting engine."),
            ("\U0001F517", "Seamless suite fit", "Built directly on ECOFLOW Base masters \u2014 no duplicate data entry."),
        ],
        "highlights": ["Service catalog", "Service orders", "RFID", "Geo-tag", "Photo proof", "Status flow"],
    },
    "ecoflow_routing": {
        "title": "ECOFLOW Routing",
        "tag": "Route plans, stop sequencing and dispatch for collection fleets",
        "intro": "Plan smarter days. ECOFLOW Routing builds daily route plans from "
                 "service orders, sequences stops with a nearest-neighbour optimiser, "
                 "and assigns vehicles and drivers from Odoo Fleet.",
        "features": [
            ("\U0001F5FA\uFE0F", "Daily route plans", "Assemble routes for each day, depot and zone in a few clicks."),
            ("\U0001F4CD", "Smart stop sequencing", "Order stops automatically with a nearest-neighbour sequencer to cut drive time."),
            ("\U0001F69B", "Fleet &amp; driver assignment", "Attach vehicles and drivers from Odoo Fleet and balance the load."),
            ("\u23F1\uFE0F", "Dispatch-ready", "Hand crews a clear, ordered list of stops linked to live service orders."),
            ("\U0001F4C9", "Efficiency insight", "Feeds route-efficiency scoring and savings estimates in the AI module."),
            ("\U0001F517", "Connected", "Reads directly from ECOFLOW Collection orders \u2014 always in sync."),
        ],
        "highlights": ["Route plans", "Stop sequencing", "Fleet", "Drivers", "Dispatch", "Optimiser"],
    },
    "ecoflow_recycling": {
        "title": "ECOFLOW Recycling",
        "tag": "Weighbridge tickets, MRF processing, recovery &amp; diversion",
        "intro": "Prove your diversion. ECOFLOW Recycling captures weighbridge tickets, "
                 "runs material-recovery process batches, records recovered outputs and "
                 "residuals, and computes diversion and recovery yield automatically.",
        "features": [
            ("\u2696\uFE0F", "Weighbridge tickets", "Record inbound and outbound weights with full traceability."),
            ("\U0001F3ED", "MRF process batches", "Run recovery batches that convert mixed input into clean output streams."),
            ("\U0001F4E6", "Recovery outputs", "Log recovered commodities and residuals by material and mass."),
            ("\U0001F4C8", "Diversion &amp; yield", "Auto-compute diversion rate and recovery yield for every batch."),
            ("\U0001F50D", "Mass-balance ready", "Clean inputs/outputs power AI anomaly detection for mass-balance drift."),
            ("\U0001F517", "Suite-native", "Built on Collection and Fleet \u2014 weights tie back to real service events."),
        ],
        "highlights": ["Weigh tickets", "MRF batches", "Recovery", "Residuals", "Diversion %", "Yield"],
    },
    "ecoflow_compliance": {
        "title": "ECOFLOW Compliance",
        "tag": "Waste codes, electronic manifests and a permit register",
        "intro": "Stay audit-ready. ECOFLOW Compliance gives you a regulatory waste-code "
                 "library, electronic chain-of-custody manifests built from service "
                 "events, and a permit register with expiry tracking.",
        "features": [
            ("\U0001F516", "Waste-code library", "Maintain regulatory waste codes and attach them across the suite."),
            ("\U0001F4DC", "Electronic manifests", "Generate chain-of-custody manifests automatically from collection events."),
            ("\U0001F6E1\uFE0F", "Permit register", "Track permits, authorities and validity with proactive expiry alerts."),
            ("\U0001F9FE", "Manifest lines", "Itemise waste codes, quantities and handlers per movement."),
            ("\u23F0", "Expiry intelligence", "Permit expiries surface as AI insights before they become violations."),
            ("\U0001F517", "Always connected", "Pulls from real service events \u2014 no parallel paperwork."),
        ],
        "highlights": ["Waste codes", "Manifests", "Chain of custody", "Permits", "Expiry alerts"],
    },
    "ecoflow_dashboard": {
        "title": "ECOFLOW Dashboard &amp; Branding",
        "tag": "A SA Systems branded operations cockpit, KPIs and graphical reporting",
        "intro": "See everything at a glance. ECOFLOW Dashboard adds the SA Systems "
                 "branded operations cockpit, KPI tiles, graph &amp; pivot analytics across "
                 "collection, routing, recycling and compliance, plus a central settings "
                 "panel for operational thresholds.",
        "features": [
            ("\U0001F4CA", "Operations cockpit", "A branded, single-screen command view of today\u2019s operation."),
            ("\U0001F522", "Live KPI tiles", "Orders, routes, diversion, permits and more \u2014 always current."),
            ("\U0001F4C8", "Graph &amp; pivot analytics", "Slice collection, routing, recycling and compliance any way you need."),
            ("\u2699\uFE0F", "Central settings", "Tune operational thresholds from one configuration panel."),
            ("\U0001F3A8", "SA Systems identity", "Polished charcoal &amp; red theme that looks great on the big screen."),
            ("\U0001F517", "Whole-suite view", "Aggregates every ECOFLOW module into one cohesive picture."),
        ],
        "highlights": ["Cockpit", "KPI tiles", "Graphs", "Pivots", "Settings", "Branding"],
    },
    "ecoflow_ai": {
        "title": "ECOFLOW AI Intelligence",
        "tag": "On-premise, privacy-first forecasting, prediction, anomaly detection &amp; insights",
        "intro": "Run operations on autopilot. ECOFLOW AI adds an explainable, "
                 "privacy-first intelligence layer: demand forecasting, predictive bin "
                 "fill-levels, route-efficiency scoring, anomaly detection and a plain-"
                 "language insights engine. No data ever leaves your server.",
        "features": [
            ("\U0001F52E", "Demand forecasting", "Forecast volume per zone and waste stream using trend + weekday seasonality."),
            ("\U0001F5D1\uFE0F", "Predictive bin fill", "Predict fill-levels and recommend the smartest time to collect \u2014 before overflow."),
            ("\U0001F6A8", "Anomaly detection", "Flag contamination, mass-balance drift and missed-pickup spikes with robust statistics."),
            ("\U0001F9ED", "Next-best-action", "Plain-language insights ranked by impact, with one-click drill-down."),
            ("\U0001F30D", "Region-aware", "Built-in profiles for EU, UK, US, AU, GCC, India and a global default \u2014 units &amp; frameworks adapt."),
            ("\U0001F512", "Private &amp; explainable", "Pure-Python deterministic models. Nothing leaves your server; every number is auditable."),
        ],
        "highlights": ["Forecasting", "Predictive bins", "Anomaly detection", "AI insights", "Region-aware", "On-premise"],
    },
}

OPL1 = """Odoo Proprietary License v1.0

This software and associated files (the "Software") may only be used (executed,
modified, executed after modifications) if you have purchased a valid license
from the authors, typically via Odoo Apps, or if you have received a written
agreement from the authors of the Software (see the COPYRIGHT file).

You may develop Odoo modules that use the Software as a library (typically
by depending on it, importing it and using its resources), but without copying
any source code or material from the Software. You may distribute those
modules under the license of your choice, provided that this license is
compatible with the terms of the Odoo Proprietary License (For example: LGPL,
MIT, or proprietary licenses similar to this one).

It is forbidden to publish, distribute, sublicense, or sell copies of the
Software or modified copies of the Software.

The above copyright notice and this permission notice must be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

Copyright (c) 2025 SA Systems (https://www.sasystems.solutions)
"""


def feature_card(emoji, head, body):
    return f"""
        <div style="background:#fff;border:1px solid #e7e9eb;border-radius:14px;padding:22px 22px 20px;box-shadow:0 1px 2px rgba(0,0,0,.04);">
          <div style="font-size:30px;line-height:1;margin-bottom:12px;">{emoji}</div>
          <div style="font-size:17px;font-weight:800;color:{INK};margin-bottom:6px;">{head}</div>
          <div style="font-size:14px;line-height:1.55;color:{SLATE};">{body}</div>
        </div>"""


def chip(text):
    return (f'<span style="display:inline-block;background:{CHARCOAL};color:#fff;'
            f'font-size:13px;font-weight:700;padding:7px 13px;border-radius:999px;'
            f'margin:0 8px 8px 0;">{text}</span>')


def build_html(mod):
    m = MODULES[mod]
    feats = "".join(feature_card(*f) for f in m["features"])
    chips = "".join(chip(h) for h in m["highlights"])
    other = [v["title"].replace(" &amp; ", " & ") for k, v in MODULES.items() if k != mod]
    suite = "".join(
        f'<li style="margin:0 0 8px;color:{SLATE};font-size:14px;">'
        f'<span style="color:{RED};font-weight:800;">\u2713</span> {name}</li>'
        for name in other
    )
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>{m['title']} \u2014 SA Systems</title>
</head>
<body style="margin:0;padding:0;background:{SURFACE};font-family:'Segoe UI',Roboto,Helvetica,Arial,sans-serif;-webkit-font-smoothing:antialiased;">
<div style="max-width:1100px;margin:0 auto;background:{SURFACE};">

  <!-- Brand header -->
  <div style="background:{CHARCOAL};border-radius:0 0 18px 18px;padding:18px 28px;display:flex;align-items:center;justify-content:space-between;">
    <img src="sa_logo.png" alt="SA Systems" style="height:46px;width:auto;display:block;"/>
    <div style="color:#aeb4b8;font-size:12px;font-weight:700;letter-spacing:.06em;text-transform:uppercase;">Odoo 18 &amp; 19 \u00b7 Multi-currency \u00b7 Region-aware</div>
  </div>

  <!-- Banner -->
  <div style="border-radius:18px;overflow:hidden;margin-top:14px;">
    <img src="banner.png" alt="{m['title']}" style="display:block;width:100%;height:auto;"/>
  </div>

  <!-- Lede -->
  <div style="padding:38px 40px 8px;">
    <div style="display:inline-block;background:{RED};color:#fff;font-size:12px;font-weight:800;letter-spacing:.08em;padding:6px 12px;border-radius:999px;text-transform:uppercase;">SA Systems \u00b7 ECOFLOW</div>
    <h1 style="font-size:38px;line-height:1.1;color:{INK};margin:16px 0 10px;font-weight:900;letter-spacing:-.02em;">{m['title']}</h1>
    <p style="font-size:19px;line-height:1.5;color:{SLATE};margin:0 0 18px;max-width:760px;">{m['tag']}.</p>
    <p style="font-size:16px;line-height:1.7;color:#3b4045;margin:0 0 6px;max-width:820px;">{m['intro']}</p>
    <div style="margin-top:20px;">{chips}</div>
  </div>

  <!-- Features -->
  <div style="padding:18px 40px 8px;">
    <h2 style="font-size:13px;letter-spacing:.12em;text-transform:uppercase;color:{RED};font-weight:800;margin:18px 0 16px;">What you get</h2>
    <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:16px;">
      {feats}
    </div>
  </div>

  <!-- Why ECOFLOW band -->
  <div style="margin:34px 0 0;background:linear-gradient(135deg,{CHARCOAL_2} 0%,{CHARCOAL} 60%,#3a0c0c 140%);padding:40px;border-radius:18px;">
    <h2 style="color:#fff;font-size:26px;font-weight:900;margin:0 0 8px;letter-spacing:-.01em;">Built for modern waste &amp; recycling operations</h2>
    <p style="color:#c7ccd0;font-size:16px;line-height:1.6;margin:0 0 22px;max-width:780px;">
      Part of the ECOFLOW suite by SA Systems \u2014 a complete, AI-ready platform for collection,
      routing, recovery, compliance and analytics, native to Odoo 18 &amp; 19. Multi-currency as
      standard, with built-in regional profiles for the EU, UK, US, Australia, GCC/MENA and India.
    </p>
    <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(160px,1fr));gap:18px;">
      <div><div style="color:{RED_HI};font-size:30px;font-weight:900;">\u221222%</div><div style="color:#aeb4b8;font-size:13px;">fewer wasted miles</div></div>
      <div><div style="color:{RED_HI};font-size:30px;font-weight:900;">+15%</div><div style="color:#aeb4b8;font-size:13px;">diversion uplift</div></div>
      <div><div style="color:{RED_HI};font-size:30px;font-weight:900;">+10pt</div><div style="color:#aeb4b8;font-size:13px;">on-time collection</div></div>
      <div><div style="color:{RED_HI};font-size:30px;font-weight:900;">Private</div><div style="color:#aeb4b8;font-size:13px;">on-premise AI</div></div>
    </div>
  </div>

  <!-- Suite -->
  <div style="padding:34px 40px 10px;">
    <h2 style="font-size:13px;letter-spacing:.12em;text-transform:uppercase;color:{RED};font-weight:800;margin:0 0 14px;">Completes the suite with</h2>
    <ul style="list-style:none;padding:0;margin:0;columns:2;-webkit-columns:2;">
      {suite}
    </ul>
  </div>

  <!-- CTA / footer -->
  <div style="padding:30px 40px 46px;text-align:center;">
    <div style="background:#fff;border:1px solid #e7e9eb;border-radius:16px;padding:30px;">
      <img src="sa_logo.png" alt="SA Systems" style="height:40px;width:auto;display:inline-block;background:{CHARCOAL};padding:10px 16px;border-radius:10px;"/>
      <div style="font-size:14px;color:{SLATE};margin:14px 0;">Environmental operations software, engineered for clarity.</div>
      <a href="https://sasystems.solutions/custom-web-app-development" style="display:inline-block;background:{RED};color:#fff;text-decoration:none;font-weight:800;font-size:15px;padding:12px 24px;border-radius:999px;">Visit sasystems.solutions</a>
      <div style="font-size:12px;color:#9aa0a5;margin-top:16px;">info@sasystems.solutions \u00b7 Compatible with Odoo 18.0 &amp; 19.0 \u00b7 Multi-currency \u00b7 OPL-1</div>
    </div>
  </div>

</div>
</body>
</html>
"""


if __name__ == "__main__":
    for mod in MODULES:
        desc = os.path.join(ADDONS, mod, "static", "description")
        os.makedirs(desc, exist_ok=True)
        with open(os.path.join(desc, "index.html"), "w") as f:
            f.write(build_html(mod))
        with open(os.path.join(ADDONS, mod, "LICENSE"), "w") as f:
            f.write(OPL1)
        print("description + LICENSE:", mod)
    print("done")
