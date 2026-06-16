"""Align all ECOFLOW manifests to the Odoo Apps Store single-product model.

The suite is sold as ONE paid product, not seven. ``ecoflow_base`` is the
foundational module every other module depends on, so it carries the price and
acts as the paywall for the whole suite. The remaining six modules are free
add-ons: a single purchase of ECOFLOW Base unlocks the complete platform.

- ``ecoflow_base``  -> paid (SUITE_PRICE, USD)
- all other modules -> free (price 0.00)
- drop the obsolete "series-agnostic" comment block
- shorten over-length app names to <= 25 chars

The module ``version`` is intentionally left untouched so each series branch
keeps its own ``<series>.1.0.0`` value (18.0.1.0.0, 19.0.1.0.0, ...).
"""
import os
import re

ROOT = "/Users/fahad/Desktop/Odoo Apps/Waste Management System "
PAID_MODULE = "ecoflow_base"
SUITE_PRICE = 299.00
MODULES = ["ecoflow_base", "ecoflow_collection", "ecoflow_routing",
           "ecoflow_recycling", "ecoflow_compliance", "ecoflow_dashboard",
           "ecoflow_ai"]
NAME_FIX = {"ECOFLOW Dashboard & Branding": "ECOFLOW Dashboard"}

for mod in MODULES:
    path = os.path.join(ROOT, mod, "__manifest__.py")
    src = open(path, encoding="utf-8").read()

    # Remove the multi-line series-agnostic comment block above version.
    src = re.sub(r"[ \t]*# Series-agnostic version.*?series is running\.\n",
                 "", src, flags=re.DOTALL)

    # Single-product pricing: only the base module is paid.
    price = SUITE_PRICE if mod == PAID_MODULE else 0.00
    src = re.sub(r'"price":\s*[0-9.]+', f'"price": {price:.2f}', src)

    # Name length compliance.
    for old, new in NAME_FIX.items():
        src = src.replace(f'"name": "{old}"', f'"name": "{new}"')

    open(path, "w", encoding="utf-8").write(src)
    print(f"patched {mod} (price {price:.2f})")
print("DONE")
