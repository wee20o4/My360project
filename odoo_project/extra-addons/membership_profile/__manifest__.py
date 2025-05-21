# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Publishing Members',
    'summary': 'Publishing Members to Public',
    'description': '''
        Show all partner are member, with condition available of membership
    ''',
    'category': 'Hidden',
    'depends': ['website_sale', 'membership', 'website_crm_partner_assign', 'hr_skills'],
    'version': '16.0.0.0.4',
    'data': [
        # Security
        'security/ir.model.access.csv',
        # Data
        'data/committee_data.xml',
        'data/membership_resume_type.xml',
        # Views
        # Views Snippet
        'views/snippets/snippets.xml',
        'views/snippets/s_dynamic_snippet_members.xml',
        # View backend
        'views/product_views.xml',
        'views/partner_view.xml',
        # Views Website
        'views/website_partner_detail_templates.xml',
        'views/website_partner_member_templates.xml',
    ],
    'assets': {
        'website.assets_wysiwyg': [
            '/membership_profile/static/src/snippets/s_public_member/options.js',
            '/membership_profile/static/src/snippets/s_public_member/000.xml',
            '/membership_profile/static/src/snippets/public_member/options.js',
        ],
        'web.assets_frontend': [
            "/membership_profile/static/src/css/style.scss",
            "/membership_profile/static/src/js/vcard.js",
            "/membership_profile/static/src/js/zoom.js",
            "/membership_profile/static/src/snippets/s_public_member/000.js",
        ],
    },
    'installable': True,
    'auto_install': False,
    'application': True,
    'license': 'LGPL-3',
}
