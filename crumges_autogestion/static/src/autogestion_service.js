/** @odoo-module **/
import { registry } from "@web/core/registry";
import { session } from "@web/session";
import { browser } from "@web/core/browser/browser";
import { _t } from "@web/core/l10n/translation";

// Opciones del menú del avatar que no aplican a los clientes de Crumges
const REMOVED_USER_ITEMS = ["support", "odoo_account", "install_pwa"];

export function autogestionConfig() {
    const cfg = session.crumges_autogestion || {};
    let url = cfg.url || "/autogestion/";
    if (!url.endsWith("/")) {
        url += "/";
    }
    return { show: Boolean(cfg.show), url, showStatus: cfg.show_status !== false };
}

export const autogestionService = {
    start() {
        const items = registry.category("user_menuitems");
        for (const key of REMOVED_USER_ITEMS) {
            if (items.contains(key)) {
                items.remove(key);
            }
        }
        const cfg = autogestionConfig();
        if (cfg.show && !items.contains("crumges_autogestion")) {
            items.add("crumges_autogestion", () => ({
                type: "item",
                id: "crumges_autogestion",
                description: _t("Autogestión"),
                href: cfg.url,
                callback: () => browser.open(cfg.url, "_blank"),
                sequence: 45,
            }));
        }
        return cfg;
    },
};

registry.category("services").add("crumges_autogestion", autogestionService);
