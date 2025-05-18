{
    'name': 'Membership Profile Search',
    'version': '16.0.2.0',
    'summary': 'Mô-đun Membership Profile Search cung cấp chức năng quản lý và hiển thị danh sách hội viên công khai trên website Odoo',
    'description': """
    Mô-đun Membership Profile Search cung cấp chức năng quản lý và hiển thị danh sách hội viên công khai trên website Odoo. Các tính năng chính bao gồm:
    - Tìm kiếm hội viên theo tên, công ty, ngành nghề hoặc địa chỉ (hỗ trợ tìm kiếm không dấu).
    - Lọc hội viên theo ngành nghề.
    - Hiển thị chi tiết hội viên với thông tin như ảnh đại diện, tên công ty, ngành nghề và địa chỉ.
    - Giao diện responsive, thân thiện với người dùng trên cả desktop và mobile.
    - Bảo mật với phân quyền truy cập công khai và nội bộ.
    """,
    'category': 'Tools',
    'author': 'Nhóm 1 - VINA',
    'depends': ['base', 'website', 'membership', 'website_partner', 'web_editor', 'website_sale', 'im_livechat', 'web'],
    'data': [
        'security/ir.model.access.csv',
        'views/membership_profile_search_templates.xml',
    ],
    'test': [
        'tests/test_membership_profile_search.py',
    ],
    'assets': {
        'web.assets_frontend': [
            'membership_profile_search/static/src/js/membership_search.js',
            'membership_profile_search/static/src/components/*.js',
            'membership_profile_search/static/src/css/*.css',
            'membership_profile_search/static/src/xml/*.xml',
            'membership_profile_search/static/img/placeholder.png',
        ],
    },
    'images': [
        'static/description/search.png',
        'static/description/nobita.jpg',
        'static/description/shin.jpg',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
    'post_init_hook': 'clear_asset_cache',
}