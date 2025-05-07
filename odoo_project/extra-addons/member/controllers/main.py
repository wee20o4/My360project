from odoo import http
from odoo.http import request
from werkzeug.exceptions import NotFound

class MemberController(http.Controller):
    @http.route('/members', type='http', auth='public', website=True)
    def list_members(self, **kwargs):
        members = request.env['res.partner'].sudo().search([
            ('membership_state', '!=', 'none'),
        ])

        # Đảm bảo tất cả thông tin được tải
        for member in members:
            if not member.company_name and member.parent_id:
                member.company_name = member.parent_id.name

        return request.render('member.member_list_template', {'members': members})
        
    @http.route('/partners/<model("res.partner"):partner>', type='http', auth='public', website=True)
    def member_detail(self, partner, **kwargs):
        values = {
            'partner': partner,
            'main_object': partner,
        }
        return request.render("website_partner.partner_page", values)