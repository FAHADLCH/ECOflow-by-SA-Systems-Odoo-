# ECOFLOW Recycling

> Weighbridge tickets, MRF processing, recovery and diversion

Part of the **ECOFLOW by SA Systems** environmental-operations suite for Odoo.

![banner](static/description/banner.png)

## Features

- Weighbridge tickets (gross / tare / net)
- MRF process batches with mass-balance checks
- Recovered outputs and residuals with estimated value (multi-currency)
- Diversion / recovery-yield computation

## Compatibility

- **Odoo 18.0** (Community & Enterprise).
- Manifest version `18.0.1.0.0` matches the `18.0` series branch.
- No external Python dependencies.

## Dependencies

`ecoflow_collection`, `fleet`

## Installation

This module is part of the ECOFLOW suite. Install **ECOFLOW** from the Apps menu
(the Dashboard app pulls in its dependencies), or install this module directly:

```bash
odoo -d ecoflow -i ecoflow_recycling --stop-after-init
```

## License & Support

Published by **SA Systems** under the **OPL-1** license as a **free add-on** to the ECOFLOW suite — unlocked by the one paid app, **ECOFLOW Base**.

- Web: https://sasystems.solutions/custom-web-app-development
- Support: info@sasystems.solutions
