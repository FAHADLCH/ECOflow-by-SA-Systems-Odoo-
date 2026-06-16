"""Patch all ECOFLOW manifests to the SA Systems convention + multi-version."""
import os
import re

ADDONS = "/Users/fahad/Desktop/Odoo Apps/Waste Management System /addons"
MODULES = ["ecoflow_base", "ecoflow_collection", "ecoflow_routing",
           "ecoflow_recycling", "ecoflow_compliance", "ecoflow_dashboard",
           "ecoflow_ai"]

VERSION_BLOCK = (
    '    # Series-agnostic version so the module installs on Odoo 18 and 19\n'
    '    # alike (a "19.0.x" string is rejected by Odoo 18, and vice-versa).\n'
    '    # Odoo prefixes the running series automatically, so this reports as\n'
    '    # 1.0 on whichever series is running.\n'
    '    "version": "1.0.0",'
)

REPLACEMENTS = [
    ('    "version": "18.0.1.0.0",', VERSION_BLOCK),
    ('    "author": "Sa Systems",',
     '    "author": "SA Systems",\n    "maintainer": "SA Systems",'),
    ('    "website": "https://www.sasystems.solutions",',
     '    "website": "https://sasystems.solutions/custom-web-app-development",'),
    ('    "support": "support@sasystems.solutions",',
     '    "support": "info@sasystems.solutions",'),
]

for mod in MODULES:
    path = os.path.join(ADDONS, mod, "__manifest__.py")
    with open(path, encoding="utf-8") as f:
        txt = f.read()
    for old, new in REPLACEMENTS:
        if old not in txt:
            print("  !! missing in", mod, "->", old[:40])
        txt = txt.replace(old, new)
    with open(path, "w", encoding="utf-8") as f:
        f.write(txt)
    print("patched", mod)
print("DONE")
