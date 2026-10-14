{
    "name": "Crumges Autogestión",
    "summary": "Acceso a Crumges Autogestión desde Odoo: ícono con el estado del servidor y menú del avatar más limpio",
    "version": "18.0.1.1.0",
    "category": "Hidden/Tools",
    "website": "https://crumges.com",
    "author": "CRUMGES",
    "license": "LGPL-3",
    "depends": ["web", "base_setup"],
    "data": [
        "security/crumges_autogestion_groups.xml",
        "data/ir_config_parameter.xml",
        "views/res_config_settings_views.xml",
    ],
    "assets": {
        "web.assets_backend": [
            "crumges_autogestion/static/src/**/*",
        ],
    },
    "installable": True,
    "application": False,
}
