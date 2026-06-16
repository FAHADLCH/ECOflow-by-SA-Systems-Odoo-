"""Generate a per-module README.md for each ECOFLOW module (SA Systems)."""
import ast
import os

ADDONS = "/Users/fahad/Desktop/Odoo Apps/Waste Management System "

FEATURES = {
    "ecoflow_base": [
        "Waste-stream and recoverable-material masters (with market price / tonne)",
        "Service zones and bin / container registry",
        "Partner (service-site) extensions",
        "Multi-currency commodity pricing",
    ],
    "ecoflow_collection": [
        "Collection service catalog (flat / per-lift / per-tonne billing)",
        "Service orders that model collection demand",
        "Proof-of-service capture (RFID + geo + photo)",
        "Multi-currency service rates",
    ],
    "ecoflow_routing": [
        "Daily route plans with ordered stops",
        "Vehicle / driver assignment (Fleet)",
        "Nearest-neighbour stop sequencer",
        "Service-order to route linkage",
    ],
    "ecoflow_recycling": [
        "Weighbridge tickets (gross / tare / net)",
        "MRF process batches with mass-balance checks",
        "Recovered outputs and residuals with estimated value (multi-currency)",
        "Diversion / recovery-yield computation",
    ],
    "ecoflow_compliance": [
        "Regulatory waste-code library",
        "Electronic chain-of-custody manifests from service events",
        "Permit register with expiry tracking",
    ],
    "ecoflow_dashboard": [
        "SA Systems branded operations cockpit",
        "KPI tiles across collection, routing, recycling and compliance",
        "Graph + pivot analysis",
        "Central ECOFLOW settings panel",
    ],
    "ecoflow_ai": [
        "Demand forecasting per zone & waste stream (trend + seasonality)",
        "Predictive bin fill-levels and smart collection recommendations",
        "Route efficiency scoring and savings estimation",
        "Anomaly detection (contamination, mass-balance drift, missed pickups)",
        "Plain-language AI insights engine",
        "Region-aware intelligence (framework, units & default currency)",
    ],
}

for mod, feats in FEATURES.items():
    man_path = os.path.join(ADDONS, mod, "__manifest__.py")
    man = ast.literal_eval(open(man_path, encoding="utf-8").read())
    name = man["name"]
    summary = man.get("summary", "").strip()
    depends = ", ".join("`%s`" % d for d in man.get("depends", []))
    feat_md = "\n".join("- %s" % f for f in feats)
    version = man.get("version", "")
    series = ".".join(version.split(".")[:2]) if version.count(".") >= 1 else version
    price = float(man.get("price", 0) or 0)
    if price > 0:
        license_blurb = (
            f"Published by **SA Systems** under the **{man.get('license')}** license. "
            f"This is the **single paid app** for the entire ECOFLOW suite "
            f"(${price:.2f} {man.get('currency')}). Purchasing it unlocks every other "
            f"ECOFLOW module as a free add-on."
        )
    else:
        license_blurb = (
            f"Published by **SA Systems** under the **{man.get('license')}** license as a "
            f"**free add-on** to the ECOFLOW suite — unlocked by the one paid app, "
            f"**ECOFLOW Base**."
        )
    readme = f"""# {name}

> {summary}

Part of the **ECOFLOW by SA Systems** environmental-operations suite for Odoo.

![banner](static/description/banner.png)

## Features

{feat_md}

## Compatibility

- **Odoo {series}** (Community & Enterprise).
- Manifest version `{man.get('version')}` matches the `{series}` series branch.
- No external Python dependencies.

## Dependencies

{depends}

## Installation

This module is part of the ECOFLOW suite. Install **ECOFLOW** from the Apps menu
(the Dashboard app pulls in its dependencies), or install this module directly:

```bash
odoo -d ecoflow -i {mod} --stop-after-init
```

## License & Support

{license_blurb}

- Web: https://sasystems.solutions/custom-web-app-development
- Support: info@sasystems.solutions
"""
    out = os.path.join(ADDONS, mod, "README.md")
    with open(out, "w", encoding="utf-8") as f:
        f.write(readme)
    print("README:", mod)
print("DONE")
