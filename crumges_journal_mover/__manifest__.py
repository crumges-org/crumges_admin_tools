{
    'name': 'Crumges Journal Mover',
    'version': '18.0.1.0.0',
    'category': 'Accounting',
    'summary': 'Forzar el traslado de asientos entre diarios contables',
    'description': """
        Herramienta avanzada para administradores que permite mover múltiples asientos
        (facturas, transferencias, recibos) de un diario a otro, resecuenciando y
        actualizando las cuentas predeterminadas de liquidez automáticamente a nivel de base de datos.
    """,
    'author': 'Crumges',
    'website': 'https://crumges.com',
    'depends': ['account', 'l10n_ar'],
    'data': [
        'wizard/journal_move_wizard_views.xml',
        'security/ir.model.access.csv',
    ],
    'installable': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
