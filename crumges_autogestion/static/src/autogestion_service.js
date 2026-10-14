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
    // ?from=odoo: si no hay sesión en el Odoo de Producción, Autogestión manda a ingresar ahí y vuelve sola
    return {
        show: Boolean(cfg.show),
        url,
        openUrl: `${url}?from=odoo`,
        showStatus: cfg.show_status !== false,
        neutralized: Boolean(cfg.neutralized),
    };
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
                href: cfg.openUrl,
                callback: () => browser.open(cfg.openUrl, "_blank"),
                sequence: 45,
            }));
        }
        return cfg;
    },
};

registry.category("services").add("crumges_autogestion", autogestionService);
