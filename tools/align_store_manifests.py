"""One-off: align all ECOFLOW manifests to Odoo Apps Store rules.

- version -> 18.0.1.0.0 (series-prefixed, major.minor.bugfix)
- price   -> 10.00 USD (>= 9 EUR store minimum)
- drop the obsolete "series-agnostic" comment block
- shorten over-length app names to <= 25 chars
"""
import os
import re

ROOT = "/Users/fahad/Desktop/Odoo Apps/Waste Management System "
MODULES = ["ecoflow_base", "ecoflow_collection", "ecoflow_routing",
           "ecoflow_recycling", "ecoflow_compliance", "ecoflow_dashboard",
           "ecoflow_ai"]
VERSION = "18.0.1.0.0"
NAME_FIX = {"ECOFLOW Dashboard & Branding": "ECOFLOW Dashboard"}

for mod in MODULES:
    path = os.path.join(ROOT, mod, "__manifest__.py")
    src = open(path, encoding="utf-8").read()

    # Remove the multi-line series-agnostic comment block above version.
    src = re.sub(r"[ \t]*# Series-agnostic version.*?series is running\.\n",
                 "", src, flags=re.DOTALL)

    # Version + price.
    src = re.sub(r'"version":\s*"[^"]+"', f'"version": "{VERSION}"', src)
    src = re.sub(r'"price":\s*[0-9.]+', '"price": 10.00', src)

    # Name length compliance.
    for old, new in NAME_FIX.items():
        src = src.replace(f'"name": "{old}"', f'"name": "{new}"')

    open(path, "w", encoding="utf-8").write(src)
    print("patched", mod)
print("DONE")
