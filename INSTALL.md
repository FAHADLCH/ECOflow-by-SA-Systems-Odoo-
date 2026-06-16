# ECOFLOW — Install & Local Test Guide

Installable Odoo modules for the ECOFLOW environmental-operations ERP.
**Compatible with Odoo 18.0 and 19.0** (Community).

> Note on versions: the views use the modern `<list>` tag and `view_mode="list,form"`,
> which is required by Odoo 18 and 19. Odoo 17 (which still used `<tree>`) is **not**
> targeted by this build, matching the requested 18/19 scope.

---

## 1. The app

ECOFLOW is a **single module** (`ecoflow`) that bundles every capability:

| Capability area | Provides |
|-----------------|----------|
| Base masters | Waste streams, materials, zones, bins, service sites |
| Collection | Services, service orders, proof-of-service events |
| Routing | Routes, stop sequencing (nearest-neighbour optimizer), dispatch |
| Recycling | Weigh tickets, MRF process batches, recovery, mass balance |
| Compliance | Waste codes, electronic manifests, permit register + expiry cron |
| Cockpit & AI | Branded operations cockpit, KPIs and on-premise AI insights |

Everything installs from one app — no separate dependencies to enable.

---

## 2. Fastest path — Docker (recommended)

Prerequisites: Docker Desktop (or Docker Engine + Compose v2).

```bash
cd "Waste Management System"

# Option A — one command, initializes DB + installs everything with demo data
make init        # uses Odoo 18 by default
make up

# Then open the app:
#   http://localhost:8070
```

### 🔗 Local test link

After `make up`, open: **http://localhost:8070**

- Database name: `ecoflow`
- Login: `admin`
- Password: `admin`

The **ECOFLOW** app appears in the top-left apps menu, with **Recycling** and
**Compliance** as sibling top-level menus.

### Run on Odoo 19 instead

```bash
make clean              # only if you initialized 18 already (deletes data)
make init TAG=19
make up TAG=19
```

---

## 3. Manual Docker (without make)

```bash
cd "Waste Management System"

# Initialize DB + install the app (demo data included)
ODOO_TAG=18 docker compose run --rm odoo odoo \
  --config=/etc/odoo/odoo.conf \
  -d ecoflow \
  -i ecoflow \
  --stop-after-init

# Start the server
ODOO_TAG=18 docker compose up -d
# -> http://localhost:8070   (db: ecoflow, user: admin, pass: admin)
```

Swap `ODOO_TAG=18` for `ODOO_TAG=19` to test on Odoo 19.

---

## 4. Install into an existing Odoo (no Docker)

1. Copy the `ecoflow/` module folder from the repository root into your Odoo
   `addons_path` (or add this repository directory to `addons_path` in your
   `odoo.conf`).
2. Restart Odoo and **Update Apps List** (developer mode).
3. Install **ECOFLOW** — it contains every capability (base, collection, routing,
   recycling, compliance, cockpit and AI) in one app.

```bash
# Example: install the app
./odoo-bin -c odoo.conf -d ecoflow \
  -i ecoflow \
  --stop-after-init
```

---

## 5. Five-minute test script (operational flow)

Once logged in at http://localhost:8070 with demo data:

1. **Bins** — `ECOFLOW ▸ Assets ▸ Bins & Containers`: 3 demo bins across two sites.
2. **Service Orders** — `ECOFLOW ▸ Operations ▸ Service Orders`: 3 scheduled orders.
3. **Routing**:
   - Open `ECOFLOW ▸ Operations ▸ Routes`, create a route, set **Zone = North Metro**,
     **Date = today**.
   - Click **Load Orders** → scheduled North-zone orders attach as stops.
   - Click **Optimize Sequence** → stops are ordered by nearest-neighbour and leg
     distances are computed.
   - Click **Dispatch**, then on a stop row click the **Serviced** check → a
     proof-of-service event is created and the bin's *last serviced* updates.
4. **Recycling**:
   - `ECOFLOW ▸ Recycling ▸ Process Batches`: the demo batch shows
     input 10,000 kg, recovered 8,500 kg, residual 1,500 kg, **Mass Balance OK = ✓**,
     recovery rate 85%.
   - Try editing residual to break the ±2% balance — **Mark Done** will be blocked.
   - `ECOFLOW ▸ Recycling ▸ Weigh Tickets`: create a ticket, set gross/tare → net
     computes; **Post** it.
5. **Compliance**:
   - `ECOFLOW ▸ Compliance ▸ Manifests`: open the demo manifest, walk the signature
     chain (Generator → Transporter → Facility → Close).
   - `ECOFLOW ▸ Compliance ▸ Permits`: the transport permit shows as **Expiring Soon**;
     the daily cron posts reminders.

---

## 6. Useful commands

```bash
make logs            # tail Odoo logs
make update          # upgrade all ECOFLOW modules after code changes
make update TAG=19   # same, on Odoo 19
make shell           # Odoo shell on the ecoflow DB
make psql            # psql into Postgres
make down            # stop containers (keeps data)
make clean           # stop + delete volumes (fresh start)
```

`--dev=reload,qweb,xml` is enabled, so Python/XML edits hot-reload during development.

---

## 7. Troubleshooting

| Symptom | Fix |
|---------|-----|
| Port 8070 in use | Stop other Odoo, or change the host port in `docker-compose.yml` |
| Modules not listed | Developer mode ▸ Apps ▸ **Update Apps List** |
| Changed a model field | `make update` (schema changes need a module upgrade) |
| Want a clean slate | `make clean && make init` |
| Switching 18 ↔ 19 | Use a fresh DB (`make clean`) to avoid cross-version schema drift |
