from odoo import models

DEFAULT_URL = "/autogestion/"
PROD_URL_PARAM = "crumges_autogestion.prod_url"


def is_neutralized(icp):
    """Base de ensayos: Odoo la marca al neutralizarla (click-odoo-restoredb --neutralize)."""
    return icp.get_param("database.is_neutralized") == "True"


def absolute_panel_url(icp):
    """Dirección completa del panel según este Odoo (para que las copias de ensayos apunten a Producción)."""
    url = icp.get_param("crumges_autogestion.url") or DEFAULT_URL
    if url.startswith("http"):
        return url
    base = (icp.get_param("web.base.url") or "").rstrip("/")
    return f"{base}/{url.lstrip('/')}" if base else url


class IrHttp(models.AbstractModel):
    _inherit = "ir.http"

    def session_info(self):
        """Le dice al cliente web si mostrar el acceso a Autogestión y a qué dirección apunta."""
        info = super().session_info()
        user = self.env.user
        if user and user._is_internal():
            icp = self.env["ir.config_parameter"].sudo()
            neutralized = is_neutralized(icp)
            url = icp.get_param("crumges_autogestion.url") or DEFAULT_URL
            if neutralized:
                # En ensayos se entra a Autogestión desde Producción (ahí está la sesión que vale)
                url = icp.get_param(PROD_URL_PARAM) or url
            info["crumges_autogestion"] = {
                "show": user.has_group("crumges_autogestion.group_autogestion_user"),
                "url": url,
                "show_status": not neutralized and icp.get_param("crumges_autogestion.show_status", "True") == "True",
                "neutralized": neutralized,
            }
        return info
