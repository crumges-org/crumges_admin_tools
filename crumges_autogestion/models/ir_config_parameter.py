from odoo import api, models

from .ir_http import PROD_URL_PARAM, absolute_panel_url, is_neutralized

WATCHED = ("web.base.url", "crumges_autogestion.url")


class IrConfigParameter(models.Model):
    _inherit = "ir.config_parameter"

    def _crumges_sync_prod_url(self):
        """En Producción guarda la dirección completa del panel; las copias de ensayos la heredan."""
        icp = self.sudo()
        if is_neutralized(icp):
            return
        url = absolute_panel_url(icp)
        if url.startswith("http") and icp.get_param(PROD_URL_PARAM) != url:
            super(IrConfigParameter, icp).set_param(PROD_URL_PARAM, url)

    @api.model
    def set_param(self, key, value):
        res = super().set_param(key, value)
        if key in WATCHED:
            self._crumges_sync_prod_url()
        return res

    def _register_hook(self):
        super()._register_hook()
        try:
            self._crumges_sync_prod_url()
        except Exception:  # nunca impedir que Odoo arranque por esto
            pass
