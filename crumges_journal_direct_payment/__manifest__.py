{
    'name': 'Journal Direct Payment',
    'version': '18.0.1.0.0',
    'category': 'Accounting',
    'summary': 'Permite configurar diarios para que los pagos vayan directos a su cuenta, omitiendo la cuenta puente.',
    'description': """
Journal Direct Payment
======================
Agrega una opción a los diarios contables (especialmente de Efectivo) para omitir las cuentas puente
de los métodos de pago, sincronizando automáticamente todas las líneas de pago entrante y saliente
con la cuenta predeterminada del diario.
    """,
    'author': 'Crumges',
    'website': 'https://crumges.com',
    'depends': ['account'],
    'data': [
        'views/account_journal_views.xml',
    ],
    'installable': True,
    'application': False,
    'license': 'AGPL-3',
}
