from odoo import http
from odoo.http import request

class MemberController(http.Controller):
    @http.route('/members', type='http', auth='public', website=True)
    def list_members(self, **kwargs):
        partners = request.env['res.partner'].sudo().search([])
        return request.render('member.member_list_template', {'members': partners})