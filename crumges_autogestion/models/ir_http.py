from odoo import models

DEFAULT_URL = "/autogestion/"


class IrHttp(models.AbstractModel):
    _inherit = "ir.http"

    def session_info(self):
        """Le dice al cliente web si mostrar el acceso a Autogestión y a qué dirección apunta."""
        info = super().session_info()
        user = self.env.user
        if user and user._is_internal():
            icp = self.env["ir.config_parameter"].sudo()
            info["crumges_autogestion"] = {
                "show": user.has_group("crumges_autogestion.group_autogestion_user"),
                "url": icp.get_param("crumges_autogestion.url") or DEFAULT_URL,
                "show_status": icp.get_param("crumges_autogestion.show_status", "True") == "True",
            }
        return info
