# 06 — Roadmap, Delivery & KPIs

## 1. Phased Delivery

```mermaid
gantt
    title ECOFLOW Delivery Roadmap
    dateFormat  YYYY-MM
    section Phase 1 — Foundation
    Customers, Subscriptions, Billing      :p1a, 2026-07, 2M
    Service catalog + bin lifecycle        :p1b, 2026-08, 2M
    section Phase 2 — Field & Routing
    Driver PWA + proof-of-service          :p2a, 2026-10, 2M
    Route optimization + dispatch board    :p2b, 2026-11, 3M
    section Phase 3 — Fleet & Recycling
    Fleet + predictive maintenance         :p3a, 2027-01, 2M
    Weighbridge + MRF + diversion          :p3b, 2027-02, 3M
    section Phase 4 — Compliance & Intelligence
    Manifests + permits + audit            :p4a, 2027-04, 2M
    Forecasting + OEI scorecard + ESG      :p4b, 2027-05, 3M
```

### Phase outcomes
| Phase | Goal | Exit criteria |
|-------|------|---------------|
| **1 — Foundation** | Revenue spine live | Subscriptions billing, services cataloged, bins tracked |
| **2 — Field & Routing** | Operations digitized | Touchless proof-of-service; optimized daily routes |
| **3 — Fleet & Recycling** | Assets + material under control | Predictive maintenance live; diversion measured |
| **4 — Compliance & Intelligence** | Auditable + self-optimizing | Auto-manifests; OEI scorecard; ESG portal |

Each phase is independently valuable — no big-bang cutover.

---

## 2. Delivery Approach

- **MVP per capability**, then deepen — ship the thinnest useful slice first.
- **TDD** for custom modules: unit + integration tests, ≥ 80% coverage target.
- **Staging mirrors production**; field changes validated with real route data.
- **Pilot depot** before fleet-wide rollout; measure OEI delta before scaling.
- **Change management**: driver + dispatcher training built into each phase.

---

## 3. RACI (per capability stream)

| Activity | Ops Architect | Dev Team | Fleet Mgr | Compliance | Finance |
|----------|:---:|:---:|:---:|:---:|:---:|
| Blueprint & data model | A/R | C | C | C | C |
| Module build | C | R | I | I | I |
| Routing tuning | A | R | C | I | I |
| Fleet/maintenance config | C | R | A/R | I | I |
| Compliance rules | C | R | I | A/R | I |
| Billing & subscriptions | C | R | I | I | A/R |
| Go-live sign-off | A | R | C | C | C |

*A=Accountable, R=Responsible, C=Consulted, I=Informed.*

---

## 4. KPI Tree (what success looks like)

```mermaid
flowchart TB
    OEI[Operational Efficiency Index]
    OEI --> A[Service Quality]
    OEI --> B[Asset Productivity]
    OEI --> C[Material Recovery]
    OEI --> D[Cost Control]
    OEI --> E[Revenue Health]

    A --> A1[On-time %]
    A --> A2[Missed collections]
    B --> B1[Route density]
    B --> B2[Vehicle uptime]
    C --> C1[Diversion rate]
    C --> C2[Recovery yield]
    D --> D1[Cost per tonne]
    D --> D2[Fuel per km]
    E --> E1[MRR]
    E --> E2[Churn]
    E --> E3[Invoice leakage]
```

### Target scorecard
| Domain | KPI | Target |
|--------|-----|--------|
| Service | On-time % | ≥ 97% |
| Service | Missed collections | < 0.5% |
| Productivity | Route density | +20% vs baseline |
| Productivity | Vehicle uptime | ≥ 95% |
| Recovery | Diversion rate | +10 pts |
| Recovery | Recovery yield | ≥ 85% of input |
| Cost | Cost per tonne | −15% |
| Compliance | Manifest closure within SLA | ≥ 99% |
| Revenue | Invoice leakage | < 0.2% |
| Revenue | Net revenue retention | ≥ 100% |

---

## 5. Risk Register (top items)

| Risk | Impact | Mitigation |
|------|--------|------------|
| Poor address/geocode data | Bad routes | Geocoding QA + map-matching feedback |
| Driver adoption of PWA | Lost proof data | Simple UX, offline mode, training, incentives |
| Telematics integration gaps | Blind spots | Vendor-agnostic connector + fallback manual capture |
| Regulatory variation by region | Compliance gaps | Configurable waste-code + manifest engine |
| Optimizer over-tightening routes | Driver burnout / SLA misses | Buffered time windows, human-in-the-loop dispatch |
| Commodity price volatility | Margin swings | Inventory buffer + timed selling |

---

## 6. Definition of Done (program level)

- [ ] All 7 capabilities live and integrated end-to-end
- [ ] Single proof-of-service event drives billing + compliance + analytics
- [ ] Mass balance reconciles within tolerance nightly
- [ ] OEI scorecard live with drill-down
- [ ] Customer self-service + ESG portal in production
- [ ] Security checklist passed; DR drill successful
- [ ] Pilot depot shows measurable OEI improvement before scale-out

---

*ECOFLOW — from kerbside to certificate, optimized at every step.*
