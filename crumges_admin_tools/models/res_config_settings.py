from odoo import models, fields, api
from odoo.exceptions import AccessError

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    @api.model
    def default_get(self, fields):
        res = super(ResConfigSettings, self).default_get(fields)
        if self.env.context.get('module') == 'crumges_admin_tools':
            if not self.env.su and self.env.uid != 1:
                raise AccessError("Acceso Denegado: Solo el Superusuario (OdooBot) tiene permiso para ver y utilizar el panel de Herramientas Avanzadas de Crumges.")
        return res

    # Checkboxes Mágicos (El nombre debe coincidir exactamente con el nombre técnico del módulo)
    module_crumges_journal_mover = fields.Boolean("Mover Asientos")
    module_crumges_journal_resequencer = fields.Boolean("Resecuenciar Diarios")
    module_crumges_product_replacer = fields.Boolean("Reemplazo de Productos")
