/** @odoo-module **/
import { Component, onWillStart, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";

/**
 * ECOFLOW AI Command Center.
 *
 * A graphical, dynamic operations cockpit that combines the core KPIs with
 * the AI intelligence layer (insights, demand forecast, recovery mix). Charts
 * are rendered as dependency-free inline SVG so the dashboard works on Odoo
 * 18 and 19 without any external charting library.
 */
export class EcoflowAiCenter extends Component {
    static template = "ecoflow.Center";
    static props = ["*"];

    setup() {
        this.orm = useService("orm");
        this.action = useService("action");
        this.notification = useService("notification");
        this.logoUrl = "/ecoflow_dashboard/static/src/img/sa_systems_logo.png";
        this.state = useState({
            kpis: {},
            ai: { insights: [], charts: {} },
            region: "global",
            framework: "",
            loading: true,
            refreshing: false,
        });

        onWillStart(async () => {
            await this.loadAll();
        });
    }

    async loadAll() {
        this.state.loading = true;
        const [kpis, ai, params] = await Promise.all([
            this.orm.call("ecoflow.dashboard", "get_kpis", []),
            this.orm.call("ecoflow.dashboard", "get_ai_kpis", []),
            this.orm.call("ir.config_parameter", "get_param", ["ecoflow.region", "global"]),
        ]);
        this.state.kpis = kpis;
        this.state.ai = ai;
        this.state.region = params || "global";
        this.state.framework = this.regionLabel(params || "global");
        this.state.loading = false;
    }

    regionLabel(code) {
        const map = {
            global: "Global / Generic (ISO)",
            eu: "European Union (EWC)",
            uk: "United Kingdom (EWC)",
            us: "United States (EPA / RCRA)",
            au: "Australia (NEPM / EPA)",
            gcc: "GCC / Middle East",
            in: "India (CPCB / SWM)",
        };
        return map[code] || "Global";
    }

    async refresh() {
        this.state.refreshing = true;
        try {
            await this.orm.call("ecoflow.ai.insight", "_cron_generate", []);
            await this.loadAll();
            this.notification.add("AI intelligence refreshed.", {
                type: "success",
            });
        } catch (e) {
            this.notification.add("Could not refresh AI data.", {
                type: "danger",
            });
        } finally {
            this.state.refreshing = false;
        }
    }

    // ---- KPI getters -------------------------------------------------
    get diversionPct() {
        const k = this.state.kpis;
        const target = k.target_diversion || 100;
        return Math.min(100, Math.round(((k.diversion_rate || 0) / target) * 100));
    }
    get completionPct() {
        return Math.min(100, Math.round(this.state.kpis.completion_rate || 0));
    }

    // ---- Chart geometry helpers (inline SVG) -------------------------
    /** Build an SVG path + area for the actual-vs-forecast line chart. */
    get trendChart() {
        const a = this.state.ai.charts?.actual || {};
        const f = this.state.ai.charts?.forecast || {};
        const done = a.done || [];
        const missed = a.missed || [];
        const fc = f.data || [];
        const W = 760, H = 220, P = 28;
        const allVals = [...done, ...missed, ...fc, 1];
        const max = Math.max(...allVals);
        const n = Math.max(done.length, 1);
        const stepX = (W - 2 * P) / Math.max(n - 1, 1);
        const y = (v) => H - P - (v / max) * (H - 2 * P);
        const x = (i) => P + i * stepX;

        const toLine = (arr) =>
            arr.map((v, i) => `${i === 0 ? "M" : "L"} ${x(i).toFixed(1)} ${y(v).toFixed(1)}`).join(" ");
        const toArea = (arr) => {
            if (!arr.length) return "";
            return (
                `M ${x(0)} ${y(0)} ` +
                arr.map((v, i) => `L ${x(i).toFixed(1)} ${y(v).toFixed(1)}`).join(" ") +
                ` L ${x(arr.length - 1)} ${y(0)} Z`
            );
        };

        // forecast continues from the end of actuals
        const fcOffset = done.length;
        const fcStartX = P + (fcOffset - 1) * stepX;
        const fcStepX = (W - P - fcStartX) / Math.max(fc.length, 1);
        const fx = (i) => fcStartX + (i + 1) * fcStepX;
        const fcLine = fc
            .map((v, i) => `${i === 0 ? "M " + fcStartX.toFixed(1) + " " + y(done[done.length - 1] || 0).toFixed(1) + " L" : "L"} ${fx(i).toFixed(1)} ${y(v).toFixed(1)}`)
            .join(" ");

        return {
            W, H,
            doneArea: toArea(done),
            doneLine: toLine(done),
            missedLine: toLine(missed),
            forecastLine: fcLine,
            max: Math.round(max),
            labels: (a.labels || []).map((l, i) => ({
                x: x(i), show: i % 2 === 0, text: l.slice(5),
            })),
            hasData: done.length > 0,
        };
    }

    /** Build doughnut segments for the recovery mix chart. */
    get recoveryMix() {
        const mix = this.state.ai.charts?.recovery_mix || {};
        const labels = mix.labels || [];
        const data = mix.data || [];
        const total = data.reduce((s, v) => s + v, 0) || 1;
        const palette = ["#CC0000", "#1E2629", "#E8482C", "#6b7280", "#9ca3af", "#f59e0b"];
        const R = 70, C = 90, SW = 26;
        const circ = 2 * Math.PI * R;
        let offset = 0;
        const segments = data.map((v, i) => {
            const frac = v / total;
            const seg = {
                color: palette[i % palette.length],
                dash: `${(frac * circ).toFixed(2)} ${(circ - frac * circ).toFixed(2)}`,
                offset: (-offset * circ).toFixed(2),
                label: labels[i],
                value: Math.round(v),
                pct: Math.round(frac * 100),
            };
            offset += frac;
            return seg;
        });
        return { R, C, SW, circ, segments, total: Math.round(total), hasData: data.length > 0 };
    }

    severityClass(sev) {
        return "o_ai_insight sev_" + sev;
    }

    openAction(xmlId) {
        if (!xmlId) return;
        this.action.doAction(xmlId);
    }

    openInsight(insight) {
        if (insight.action_xmlid) {
            this.action.doAction(insight.action_xmlid);
        }
    }
}

registry.category("actions").add("ecoflow.center", EcoflowAiCenter);
