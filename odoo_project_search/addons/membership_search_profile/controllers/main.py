from odoo import http
from odoo.http import request

class MembershipController(http.Controller):
    @http.route('/membership', type='http', auth='public', website=True)
    def membership_directory(self, **kwargs):
        return request.render('membership_search_profile.membership_directory_template')