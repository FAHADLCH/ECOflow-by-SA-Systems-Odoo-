/** @odoo-module **/
import { Component, onWillStart, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { _t } from "@web/core/l10n/translation";

export class EcoflowCockpit extends Component {
    static template = "ecoflow.Cockpit";
    static props = ["*"];

    setup() {
        this.orm = useService("orm");
        this.action = useService("action");
        this.state = useState({ kpis: {}, loading: true });
        this.logoUrl = "/ecoflow/static/src/img/sa_systems_logo.png";

        onWillStart(async () => {
            await this.loadKpis();
        });
    }

    async loadKpis() {
        this.state.loading = true;
        const kpis = await this.orm.call("ecoflow.dashboard", "get_kpis", []);
        this.state.kpis = kpis;
        this.state.loading = false;
    }

    get diversionPct() {
        const k = this.state.kpis;
        const target = k.target_diversion || 100;
        return Math.min(100, Math.round(((k.diversion_rate || 0) / target) * 100));
    }

    get completionPct() {
        return Math.min(100, Math.round(this.state.kpis.completion_rate || 0));
    }

    openAction(xmlId) {
        this.action.doAction(xmlId);
    }
}

registry.category("actions").add("ecoflow.cockpit", EcoflowCockpit);
