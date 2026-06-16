"""Generate ai_demo.xml: 60 days of historical service orders + bin fills.

Creates a realistic backlog of completed service orders across the two demo
zones/streams so the forecaster has signal, plus sets fill levels on demo bins
so the predictor produces a spread of recommendations. Written as static XML
with eval-based dates (relativedelta) so it is reproducible at any run date.
"""
import os
import random

WS = "/Users/fahad/Desktop/Odoo Apps/Waste Management System "
OUT = os.path.join(WS, "addons", "ecoflow_ai", "demo", "ai_demo.xml")
os.makedirs(os.path.dirname(OUT), exist_ok=True)

random.seed(42)

# (site_ref, service_ref) pairs from base/collection demo data
COMBOS = [
    ("ecoflow_base.site_acme", "ecoflow_collection.service_msw_fel"),
    ("ecoflow_base.site_acme", "ecoflow_collection.service_rec_fel"),
    ("ecoflow_base.site_riverside", "ecoflow_collection.service_org_wheelie"),
]

lines = []
lines.append('<?xml version="1.0" encoding="utf-8"?>')
lines.append("<odoo>")
lines.append('    <data noupdate="0">')
lines.append("        <!-- Historical collections (auto-generated, 60 days) -->")

rid = 0
# generate completed orders for the trailing 60..1 days, weekday-weighted
for days_ago in range(60, 0, -1):
    # base volume with weekly seasonality and slight upward trend
    trend = (60 - days_ago) * 0.02
    for site_ref, service_ref in COMBOS:
        # weekday effect: more on Mon/Thu
        base = 1.0 + trend
        n = max(0, int(round(base + random.uniform(-0.6, 1.2))))
        for _ in range(n):
            rid += 1
            lines.append(
                '        <record id="ai_hist_%d" model="ecoflow.service.order">' % rid)
            lines.append('            <field name="site_id" ref="%s"/>' % site_ref)
            lines.append('            <field name="service_id" ref="%s"/>' % service_ref)
            lines.append(
                '            <field name="scheduled_date" '
                'eval="(datetime.now() - relativedelta(days=%d)).strftime(\'%%Y-%%m-%%d\')"/>'
                % days_ago)
            # ~10% missed, rest done
            state = "missed" if random.random() < 0.1 else "done"
            lines.append('            <field name="state">%s</field>' % state)
            lines.append("        </record>")

# set fill levels on demo bins to drive a spread of predictions
lines.append("        <!-- Bin fill levels for predictive demo -->")
bin_fills = [
    ("ecoflow_base.bin_1", 94.0),   # collect now
    ("ecoflow_base.bin_2", 72.0),   # schedule soon
    ("ecoflow_base.bin_3", 38.0),   # monitor
]
for bin_ref, fill in bin_fills:
    lines.append('        <record id="%s" model="ecoflow.bin">' % bin_ref.split(".")[-1])
    # NOTE: re-reference existing demo bins by their full xml id
    lines[-1] = '        <function model="ecoflow.bin" name="write">'
    lines.append('            <value eval="[ref(\'%s\')]"/>' % bin_ref)
    lines.append('            <value eval="{\'fill_level\': %s, \'status\': \'in_service\'}"/>' % fill)
    lines.append("        </function>")

lines.append("    </data>")
lines.append("</odoo>")

with open(OUT, "w") as f:
    f.write("\n".join(lines) + "\n")

print("Wrote", OUT, "with", rid, "historical orders")
