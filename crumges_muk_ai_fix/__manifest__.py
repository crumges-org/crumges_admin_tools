{
    'name': 'Crumges MuK AI Fix',
    'version': '18.0.1.0.0',
    'category': 'Hidden',
    'depends': ['muk_ai'],
    'assets': {
        'web.assets_backend': [
            ('remove', 'muk_ai/static/src/core/commands/command_setup.js'),
            ('remove', 'muk_ai/static/src/core/commands/command_providers.js'),
            'crumges_muk_ai_fix/static/src/core/commands/command_setup.js',
            'crumges_muk_ai_fix/static/src/core/commands/command_providers.js',
        ],
    },
    'installable': True,
    'auto_install': False,
}
