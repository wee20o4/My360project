{
    'name': 'Member Management',
    'version': '1.0',
    'summary': 'Manage members and display public list',
    'depends': ['base', 'website'],
    'data': [
        'security/ir.model.access.csv',
        'views/member_templates.xml',
        'views/member_views.xml',
    ],
    'installable': True,
    'application': True,
}