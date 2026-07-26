{
    'name': 'Crumges Product Replacer',
    'version': '18.0.1.0.0',
    'category': 'Inventory/Administration',
    'summary': 'Fusión Quirúrgica y Reemplazo de Productos',
    'description': """
        Herramienta avanzada (Bisturí SQL) para administradores.
        Permite reemplazar un producto dañado o mal configurado por uno nuevo,
        migrando todo su historial (Ventas, Compras, Contabilidad, Stock) 
        mediante sentencias SQL crudas sin disparar recálculos.
    """,
    'author': 'Crumges',
    'website': 'https://crumges.com',
    'depends': ['stock', 'sale', 'purchase', 'account'],
    'data': [
        'security/ir.model.access.csv',
        'wizard/product_replace_wizard_views.xml',
    ],
    'installable': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
