{
    'name': 'Membership Search Profile',
    'version': '1.0',
    'category': 'Membership',
    'summary': 'A module to display membership directory',
    'depends': ['base', 'web', 'website', 'membership'],
    'data': [
        'views/membership_templates.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            'membership_search_profile/static/src/components/MembershipDirectory.js',
            'membership_search_profile/static/src/css/membership.css',
            'membership_search_profile/static/src/xml/membership_templates.xml',
        ],
    },
    'installable': True,
    'auto_install': False,
    'application': True,
}