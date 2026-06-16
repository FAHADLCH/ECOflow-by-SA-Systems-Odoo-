"""Merge the 7 ECOFLOW modules into a single Odoo app: ``ecoflow``.

The Odoo Apps Store lists one product per module folder. To sell ECOFLOW as a
single paid application (not seven separate listings) all modules are merged
into one module named ``ecoflow``. Domain sub-packages are used inside the
module so files that share a name across the old modules (e.g.
``service_order.py``, ``res_config_settings.py``) no longer collide.

What this script does:
  * builds ``ecoflow/`` with models/<domain>/, views/<domain>/, data/<domain>/,
    demo/<domain>/ sub-folders
  * concatenates every ``ir.model.access.csv`` into one
  * merges the backend static assets (dashboard + ai)
  * rewrites every cross-module reference: the old module-name prefixes
    (``ecoflow_base.``, ``ecoflow_collection.`` ...) become ``ecoflow.`` in all
    XML / JS / CSV, and the one Python cross-import is made relative
  * generates a single ``__manifest__.py`` with the combined, correctly ordered
    data / demo / assets and the union of external dependencies

The merged module keeps the series ``version`` of the old ``ecoflow_base``
manifest, so running this on each branch yields the right ``<series>.1.0.0``.
"""
import ast
import os
import re
import shutil

ROOT = "/Users/fahad/Desktop/Odoo Apps/Waste Management System "
DEST = os.path.join(ROOT, "ecoflow")

# domain -> old module folder name (also the order things load in)
DOMAINS = [
    ("base", "ecoflow_base"),
    ("collection", "ecoflow_collection"),
    ("routing", "ecoflow_routing"),
    ("recycling", "ecoflow_recycling"),
    ("compliance", "ecoflow_compliance"),
    ("dashboard", "ecoflow_dashboard"),
    ("ai", "ecoflow_ai"),
]
OLD_MODULES = [m for _, m in DOMAINS]

# models/__init__.py import lines, per domain (preserve original order).
MODEL_IMPORTS = {
    "base": ["utils", "waste_stream", "material", "zone", "bin_container", "res_partner"],
    "collection": ["service", "service_order", "service_event"],
    "routing": ["route", "service_order"],
    "recycling": ["weigh_ticket", "process_batch"],
    "compliance": ["waste_code", "manifest", "permit"],
    "dashboard": ["res_config_settings", "dashboard"],
    "ai": ["ai_engine", "ai_forecast", "bin_prediction", "ai_insight",
           "res_config_settings", "dashboard_ai"],
}

# data files (non-demo) in load order, per domain: (subdir, filename)
DATA_FILES = {
    "base": [("data", "ecoflow_base_data.xml"),
             ("views", "waste_stream_views.xml"),
             ("views", "material_views.xml"),
             ("views", "zone_views.xml"),
             ("views", "bin_views.xml"),
             ("views", "partner_views.xml"),
             ("views", "ecoflow_menus.xml")],
    "collection": [("data", "collection_data.xml"),
                   ("views", "service_views.xml"),
                   ("views", "service_order_views.xml"),
                   ("views", "service_event_views.xml"),
                   ("views", "collection_menus.xml")],
    "routing": [("data", "routing_data.xml"),
                ("views", "route_views.xml"),
                ("views", "service_order_views.xml"),
                ("views", "routing_menus.xml")],
    "recycling": [("data", "recycling_data.xml"),
                  ("views", "weigh_ticket_views.xml"),
                  ("views", "process_batch_views.xml"),
                  ("views", "recycling_menus.xml")],
    "compliance": [("data", "compliance_data.xml"),
                   ("views", "waste_code_views.xml"),
                   ("views", "manifest_views.xml"),
                   ("views", "permit_views.xml"),
                   ("views", "compliance_menus.xml")],
    "dashboard": [("data", "branding_data.xml"),
                  ("views", "res_config_settings_views.xml"),
                  ("views", "reporting_views.xml"),
                  ("views", "dashboard_menus.xml")],
    "ai": [("data", "ai_data.xml"),
           ("views", "ai_insight_views.xml"),
           ("views", "ai_forecast_views.xml"),
           ("views", "bin_prediction_views.xml"),
           ("views", "res_config_settings_views.xml"),
           ("views", "ai_center_action.xml"),
           ("views", "ai_menus.xml")],
}

# demo files in load order, per domain: (subdir, filename)
DEMO_FILES = {
    "base": [("demo", "ecoflow_base_demo.xml")],
    "collection": [("demo", "collection_demo.xml")],
    "recycling": [("demo", "recycling_demo.xml")],
    "compliance": [("demo", "compliance_demo.xml")],
    "dashboard": [("demo", "cockpit_demo.xml")],
    "ai": [("demo", "ai_demo.xml")],
}


def rewrite(text):
    """Rewrite old module-name prefixes to the single 'ecoflow' module."""
    for _, mod in DOMAINS:
        # external-id / template / tag prefixes: 'ecoflow_base.' -> 'ecoflow.'
        text = text.replace(mod + ".", "ecoflow.")
        # asset / image URL paths: '/ecoflow_dashboard/static/' -> '/ecoflow/static/'
        text = text.replace("/" + mod + "/", "/ecoflow/")
        # quoted standalone module token (settings <app name="...">, {'module': '...'})
        # safe: filenames like "ecoflow_base_data.xml" keep a trailing char, so
        # the closing quote never immediately follows the bare module name.
        text = text.replace('"' + mod + '"', '"ecoflow"')
        text = text.replace("'" + mod + "'", "'ecoflow'")
    return text


def copy_text(src, dst):
    with open(src, encoding="utf-8") as f:
        data = f.read()
    data = rewrite(data)
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    with open(dst, "w", encoding="utf-8") as f:
        f.write(data)


# ---- fresh start -----------------------------------------------------------
if os.path.isdir(DEST):
    shutil.rmtree(DEST)
os.makedirs(DEST)

# series version from the old base manifest
base_manifest = ast.literal_eval(
    open(os.path.join(ROOT, "ecoflow_base", "__manifest__.py"), encoding="utf-8").read())
VERSION = base_manifest["version"]

# ---- models ----------------------------------------------------------------
for domain, mod in DOMAINS:
    pkg = os.path.join(DEST, "models", domain)
    os.makedirs(pkg, exist_ok=True)
    for name in MODEL_IMPORTS[domain]:
        src = os.path.join(ROOT, mod, "models", name + ".py")
        dst = os.path.join(pkg, name + ".py")
        with open(src, encoding="utf-8") as f:
            code = f.read()
        code = rewrite(code)
        # the only cross-module python import is base/utils -> make it relative
        code = code.replace(
            "from odoo.addons.ecoflow.models.utils import",
            "from ..base.utils import")
        with open(dst, "w", encoding="utf-8") as f:
            f.write(code)
    with open(os.path.join(pkg, "__init__.py"), "w", encoding="utf-8") as f:
        f.write("# -*- coding: utf-8 -*-\n")
        for name in MODEL_IMPORTS[domain]:
            f.write(f"from . import {name}\n")

with open(os.path.join(DEST, "models", "__init__.py"), "w", encoding="utf-8") as f:
    f.write("# -*- coding: utf-8 -*-\n")
    for domain, _ in DOMAINS:
        f.write(f"from . import {domain}\n")

with open(os.path.join(DEST, "__init__.py"), "w", encoding="utf-8") as f:
    f.write("# -*- coding: utf-8 -*-\nfrom . import models\n")

# ---- data / views / demo ---------------------------------------------------
for domain, mod in DOMAINS:
    for subdir, fname in DATA_FILES.get(domain, []) + DEMO_FILES.get(domain, []):
        src = os.path.join(ROOT, mod, subdir, fname)
        dst = os.path.join(DEST, subdir, domain, fname)
        copy_text(src, dst)

# ---- security: merged access csv + base security xml -----------------------
os.makedirs(os.path.join(DEST, "security"), exist_ok=True)
copy_text(os.path.join(ROOT, "ecoflow_base", "security", "ecoflow_security.xml"),
          os.path.join(DEST, "security", "ecoflow_security.xml"))

merged_rows = []
header = None
for _, mod in DOMAINS:
    csv_path = os.path.join(ROOT, mod, "security", "ir.model.access.csv")
    if not os.path.isfile(csv_path):
        continue
    lines = [ln for ln in open(csv_path, encoding="utf-8").read().splitlines() if ln.strip()]
    if not lines:
        continue
    if header is None:
        header = lines[0]
    merged_rows.extend(rewrite(ln) for ln in lines[1:])
with open(os.path.join(DEST, "security", "ir.model.access.csv"), "w", encoding="utf-8") as f:
    f.write(header + "\n" + "\n".join(merged_rows) + "\n")

# ---- static ----------------------------------------------------------------
# description assets from base
shutil.copytree(os.path.join(ROOT, "ecoflow_base", "static", "description"),
                os.path.join(DEST, "static", "description"))
# backend src assets from dashboard, then ai (skip duplicate filenames)
for mod in ("ecoflow_dashboard", "ecoflow_ai"):
    src_root = os.path.join(ROOT, mod, "static", "src")
    for dirpath, _dirs, files in os.walk(src_root):
        rel = os.path.relpath(dirpath, src_root)
        out_dir = os.path.join(DEST, "static", "src", rel)
        os.makedirs(out_dir, exist_ok=True)
        for fn in files:
            out = os.path.join(out_dir, fn)
            if os.path.exists(out):
                continue  # shared asset already copied (e.g. sa_systems_logo.png)
            srcf = os.path.join(dirpath, fn)
            if fn.endswith((".js", ".xml", ".scss", ".css")):
                copy_text(srcf, out)
            else:
                shutil.copy2(srcf, out)

# ---- LICENSE ---------------------------------------------------------------
shutil.copy2(os.path.join(ROOT, "ecoflow_base", "LICENSE"),
             os.path.join(DEST, "LICENSE"))

# ---- manifest --------------------------------------------------------------
data_list = []
for domain, _ in DOMAINS:
    for subdir, fname in DATA_FILES.get(domain, []):
        data_list.append(f"{subdir}/{domain}/{fname}")
demo_list = []
for domain, _ in DOMAINS:
    for subdir, fname in DEMO_FILES.get(domain, []):
        demo_list.append(f"{subdir}/{domain}/{fname}")

# security first
data_block = ["security/ecoflow_security.xml", "security/ir.model.access.csv"] + data_list

assets = [
    "ecoflow/static/src/scss/ecoflow.scss",
    "ecoflow/static/src/js/cockpit.js",
    "ecoflow/static/src/xml/cockpit.xml",
    "ecoflow/static/src/scss/ai_center.scss",
    "ecoflow/static/src/js/ai_center.js",
    "ecoflow/static/src/xml/ai_center.xml",
]

def pyfmt(items, indent=8):
    pad = " " * indent
    return "\n".join(f'{pad}"{i}",' for i in items)

manifest = f'''# -*- coding: utf-8 -*-
{{
    "name": "ECOFLOW Waste Management",
    "version": "{VERSION}",
    "summary": "AI-native ERP for waste collection, routing, recovery and "
               "compliance \u2014 one integrated suite.",
    "description": """
ECOFLOW Waste Management
========================
A complete, AI-native ERP for environmental-services operators, delivered as a
single application. ECOFLOW covers the full operational lifecycle:

* **Masters** \u2014 waste streams, recoverable materials, service zones and a
  bin / container registry, with multi-currency commodity pricing.
* **Collection** \u2014 service catalog (flat / per-lift / per-tonne), service
  orders and proof-of-service capture (RFID + geo + photo).
* **Routing** \u2014 daily route plans, nearest-neighbour stop sequencing and
  vehicle / driver dispatch.
* **Recycling** \u2014 weighbridge tickets, MRF process batches with mass-balance
  checks, recovered outputs and diversion / recovery yield.
* **Compliance** \u2014 regulatory waste-code library, electronic chain-of-custody
  manifests and a permit register with expiry tracking.
* **Cockpit & analytics** \u2014 a branded operations cockpit, KPI tiles and
  graph / pivot reporting across every domain.
* **AI intelligence** \u2014 on-premise, privacy-first demand forecasting,
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
{pyfmt(data_block)}
    ],
    "assets": {{
        "web.assets_backend": [
{pyfmt(assets, 12)}
        ],
    }},
    "demo": [
{pyfmt(demo_list)}
    ],
    "images": ["static/description/banner.png"],
    "application": True,
    "installable": True,
}}
'''
with open(os.path.join(DEST, "__manifest__.py"), "w", encoding="utf-8") as f:
    f.write(manifest)

# validate manifest parses
ast.literal_eval(open(os.path.join(DEST, "__manifest__.py"), encoding="utf-8").read())
print("BUILT ecoflow/ (version", VERSION + ")")
print("data files:", len(data_block), "demo files:", len(demo_list))
