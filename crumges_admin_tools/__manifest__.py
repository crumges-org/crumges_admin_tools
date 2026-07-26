{
    'name': 'Crumges Admin Tools (Herramientas Avanzadas)',
    'version': '18.0.1.0.0',
    'category': 'Administration',
    'summary': 'Panel de control centralizado para herramientas de implementación',
    'description': """
        Módulo base que inyecta un panel de control en los Ajustes Generales de Odoo.
        Permite instalar o desinstalar de forma dinámica los submódulos de herramientas 
        destructivas (Resecuenciador, Movedor de Diarios, etc.) únicamente si eres Superusuario.
    """,
    'author': 'Crumges',
    'website': 'https://crumges.com',
    'depends': ['base_setup', 'account'],
    'data': [
        'views/res_config_settings_views.xml',
    ],
    'installable': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
