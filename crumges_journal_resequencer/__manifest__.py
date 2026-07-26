{
    'name': 'Crumges Journal Resequencer',
    'version': '18.0.1.0.0',
    'category': 'Accounting',
    'summary': 'Forzar cambio de código corto de diarios y resecuenciar asientos',
    'description': """
        Herramienta avanzada para administradores que permite cambiar el código corto
        (prefijo) de un diario contable, saltándose las restricciones de Odoo, y
        actualizando retroactivamente todos los asientos existentes a nivel de base de datos.
    """,
    'author': 'Crumges',
    'website': 'https://crumges.com',
    'depends': ['account'],
    'data': [
        'wizard/journal_resequence_wizard_views.xml',
        'security/ir.model.access.csv',
    ],
    'installable': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
