"""Trigger the ECOFLOW AI pipeline and print a summary (run via odoo shell)."""
ins = env["ecoflow.ai.insight"]
ins._cron_generate()
env.cr.commit()

forecasts = env["ecoflow.ai.forecast"].search_count([])
preds = env["ecoflow.bin.prediction"].search_count([])
insights = env["ecoflow.ai.insight"].search([])
print("=== ECOFLOW AI PIPELINE RESULT ===")
print("forecasts:", forecasts)
print("bin predictions:", preds)
print("insights:", len(insights))
for i in insights:
    print(f"  [{i.severity}] {i.name} | impact={i.impact_label} | conf={i.confidence}%")
print("=== KPIs ===")
kpis = env["ecoflow.dashboard"].get_ai_kpis()
print("critical:", kpis.get("critical"), "warnings:", kpis.get("warnings"),
      "opportunities:", kpis.get("opportunities"), "collect_now:", kpis.get("collect_now"))
print("forecast labels:", kpis.get("charts", {}).get("forecast", {}).get("labels"))
print("DONE")
