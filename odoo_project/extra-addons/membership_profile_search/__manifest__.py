{
    'name': 'Membership Profile Search',
    'version': '1.0',
    'summary': 'Manage members and display public list with search functionality',
    'depends': ['base', 'website', 'membership', 'website_partner'],
    'data': [
        'security/ir.model.access.csv',
        'views/membership_profile_search_templates.xml',
        'views/membership_profile_search_views.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            'membership_profile_search/static/img/placeholder.png',
        ],
    },
    'installable': True,
    'application': True,
}