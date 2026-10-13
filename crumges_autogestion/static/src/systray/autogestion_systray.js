/** @odoo-module **/
import { Component, onWillStart, onWillUnmount, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { browser } from "@web/core/browser/browser";
import { Dropdown } from "@web/core/dropdown/dropdown";
import { useDropdownState } from "@web/core/dropdown/dropdown_hooks";
import { autogestionConfig } from "../autogestion_service";

const LABELS = { cpu: "CPU", ram: "RAM", disk: "Disco" };
const REFRESH_MS = 60000;

function ago(iso) {
    if (!iso) {
        return "";
    }
    const s = Math.max(0, (Date.now() - new Date(iso).getTime()) / 1000);
    if (s < 3600) {
        return `hace ${Math.max(1, Math.round(s / 60))} min`;
    }
    if (s < 86400) {
        return `hace ${Math.round(s / 3600)} h`;
    }
    return `hace ${Math.round(s / 86400)} d`;
}

function untilText(iso) {
    const m = Math.round((new Date(iso).getTime() - Date.now()) / 60000);
    if (m <= 0) {
        return "se apaga en instantes";
    }
    return m < 60 ? `se apaga en ${m} min` : `se apaga en ${Math.floor(m / 60)} h ${m % 60} min`;
}

export class AutogestionSystray extends Component {
    static template = "crumges_autogestion.Systray";
    static components = { Dropdown };
    static props = {};

    setup() {
        this.cfg = autogestionConfig();
        this.dropdown = useDropdownState();
        this.state = useState({ data: null, error: null, loading: false });
        this.LABELS = LABELS;
        onWillStart(() => this.load());
        if (this.cfg.showStatus) {
            this.timer = browser.setInterval(() => this.load(), REFRESH_MS);
            onWillUnmount(() => browser.clearInterval(this.timer));
        }
    }

    async load() {
        if (!this.cfg.showStatus) {
            return;
        }
        this.state.loading = true;
        try {
            const res = await browser.fetch(`${this.cfg.url}api/summary/`, { credentials: "include" });
            if (!res.ok) {
                throw new Error(String(res.status));
            }
            this.state.data = await res.json();
            this.state.error = null;
        } catch {
            this.state.error = "No se pudo leer el estado de Autogestión.";
        } finally {
            this.state.loading = false;
        }
    }

    get status() {
        if (!this.cfg.showStatus) {
            return "none";
        }
        if (this.state.error) {
            return "unknown";
        }
        return this.state.data?.status || "unknown";
    }

    get statusTitle() {
        const d = this.state.data;
        if (this.state.error) {
            return this.state.error;
        }
        if (!d) {
            return "Autogestión";
        }
        return d.reasons?.length ? `Autogestión: ${d.reasons.join(", ")}` : "Autogestión: todo en orden";
    }

    get resources() {
        const r = this.state.data?.resources || {};
        return ["cpu", "ram", "disk"].filter((k) => r[k]).map((k) => ({ key: k, label: LABELS[k], ...r[k] }));
    }

    instanceDetail(i) {
        if (!i.online) {
            return "apagado";
        }
        if (i.shutdown_at) {
            return untilText(i.shutdown_at);
        }
        if (i.production && this.state.data?.last_backup) {
            return `respaldo ${ago(this.state.data.last_backup.time)}`;
        }
        return "en línea";
    }

    ago(iso) {
        return ago(iso);
    }

    onToggle() {
        this.load();
    }

    open() {
        browser.open(this.cfg.url, "_blank");
        this.dropdown.close();
    }
}

registry.category("systray").add(
    "crumges_autogestion.systray",
    {
        Component: AutogestionSystray,
        isDisplayed: () => autogestionConfig().show,
    },
    { sequence: 30 }
);
