from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    crumges_autogestion_url = fields.Char(
        string="Dirección de Autogestión",
        config_parameter="crumges_autogestion.url",
        default="/autogestion/",
        help="Dirección del panel. Si está en el mismo dominio que este Odoo basta con /autogestion/.",
    )
    crumges_autogestion_show_status = fields.Boolean(
        string="Mostrar estado del servidor",
        config_parameter="crumges_autogestion.show_status",
        default=True,
        help="El ícono de la barra consulta el estado del servidor (recursos, instancias, respaldos). "
        "Requiere que Autogestión esté en el mismo dominio que este Odoo.",
    )
