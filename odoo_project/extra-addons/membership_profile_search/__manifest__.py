{
    'name': 'Membership Profile Search',
    'version': '1.0',
    'summary': 'Manage members and display public list with search functionality',
    'depends': ['base', 'website', 'membership', 'website_partner', 'web_editor'],
    'data': [
        'security/ir.model.access.csv',
        'views/membership_profile_search_templates.xml',
        'views/membership_profile_search_views.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            'membership_profile_search/static/img/placeholder.png',
            'membership_profile_search/static/src/js/membership_search.js',
            'membership_profile_search/static/src/css/membership_search.css',
    ],
},
    'installable': True,
    'application': True,
}