from odoo import http
from odoo.http import request

class MemberController(http.Controller):
    @http.route('/members', type='http', auth='public', website=True)
    def list_members(self, **kwargs):
        members = request.env['res.partner'].sudo().search([
            ('membership_state', '!=', 'none'),
        ])
        return request.render('member.member_list_template', {'members': members})