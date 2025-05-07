{
    'name': 'Member Management',
    'version': '1.0',
    'summary': 'Manage members and display public list',
    'depends': ['base', 'website', 'membership'],
    'data': [
        'security/ir.model.access.csv',
        'views/member_templates.xml',
        'views/member_views.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            'member/static/img/placeholder.png',
        ],
    },
    'installable': True,
    'application': True,
}