# ECOFLOW Collection

> Service catalog, service orders and proof-of-service capture

Part of the **ECOFLOW by SA Systems** environmental-operations suite for Odoo.

![banner](static/description/banner.png)

## Features

- Collection service catalog (flat / per-lift / per-tonne billing)
- Service orders that model collection demand
- Proof-of-service capture (RFID + geo + photo)
- Multi-currency service rates

## Compatibility

- **Odoo 18.0 and 19.0** (Community & Enterprise) from a single codebase.
- Series-agnostic `version` (`1.0.0`) — Odoo prefixes the running series automatically.
- No external Python dependencies.

## Dependencies

`ecoflow_base`

## Installation

This module is part of the ECOFLOW suite. Install **ECOFLOW** from the Apps menu
(the Dashboard app pulls in its dependencies), or install this module directly:

```bash
odoo -d ecoflow -i ecoflow_collection --stop-after-init
```

## License & Support

Published by **SA Systems** under the **OPL-1** license — a paid Odoo
App Store app ($5.00 USD).

- Web: https://sasystems.solutions/custom-web-app-development
- Support: info@sasystems.solutions
