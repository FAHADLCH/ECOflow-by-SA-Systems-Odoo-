# ECOFLOW Base

> Shared foundation for the ECOFLOW environmental operations ERP

Part of the **ECOFLOW by SA Systems** environmental-operations suite for Odoo.

![banner](static/description/banner.png)

## Features

- Waste-stream and recoverable-material masters (with market price / tonne)
- Service zones and bin / container registry
- Partner (service-site) extensions
- Multi-currency commodity pricing

## Compatibility

- **Odoo 18.0 and 19.0** (Community & Enterprise) from a single codebase.
- Series-agnostic `version` (`1.0.0`) — Odoo prefixes the running series automatically.
- No external Python dependencies.

## Dependencies

`base`, `mail`, `stock`

## Installation

This module is part of the ECOFLOW suite. Install **ECOFLOW** from the Apps menu
(the Dashboard app pulls in its dependencies), or install this module directly:

```bash
odoo -d ecoflow -i ecoflow_base --stop-after-init
```

## License & Support

Published by **SA Systems** under the **OPL-1** license — a paid Odoo
App Store app ($5.00 USD).

- Web: https://sasystems.solutions/custom-web-app-development
- Support: info@sasystems.solutions
