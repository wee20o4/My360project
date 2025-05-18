# extra-addons/membership_profile_search/controllers/main.py

from odoo import http
from odoo.http import request
from werkzeug.exceptions import NotFound
import unicodedata
import re
import traceback

def remove_diacritics(text):
    """Chuẩn hóa chuỗi không dấu."""
    text = unicodedata.normalize('NFD', text)
    text = re.sub(r'[\u0300-\u036f]', '', text)
    text = text.replace('đ', 'd').replace('Đ', 'D')
    return text

class MembershipProfileSearchController(http.Controller):
    @http.route('/membership', type='http', auth='public', website=True)
    def list_members(self, **kwargs):
        try:
            search_term = kwargs.get('search', '').strip()
            domain = [
                ('membership_state', '!=', 'none'),
                ('website_published', '=', True),
            ]

            if search_term:
                # Chuẩn hóa từ khóa tìm kiếm
                normalized_search = remove_diacritics(search_term).lower()
                # Tìm kiếm không dấu trên các trường
                domain += ['|', '|', '|',
                          ('name', 'ilike', search_term),
                          ('company_name', 'ilike', search_term),
                          ('industry_id.name', 'ilike', search_term),
                          ('street', 'ilike', search_term)]

            members = request.env['res.partner'].sudo().search(domain)
            for member in members:
                if not member.company_name and member.parent_id:
                    member.company_name = member.parent_id.name or ''
            return request.render('membership_profile_search.membership_profile_search_list_template', {
                'members': members,
                'search': search_term
            })
        except Exception as e:
            # Ghi log chi tiết hơn
            error_trace = traceback.format_exc()
            request.env['ir.logging'].sudo().create({
                'name': 'MembershipProfileSearch',
                'type': 'server',
                'level': 'ERROR',
                'message': f"Error: {str(e)}\nTraceback: {error_trace}",
                'path': '/membership',
                'func': 'list_members',
                'line': 1,
            })
            return request.render('website.page_404', {'error': 'Đã xảy ra lỗi khi tải danh sách hội viên.'})

    @http.route('/partners/<model("res.partner"):partner>', type='http', auth='public', website=True)
    def member_detail(self, partner, **kwargs):
        is_authorized = request.env.user.has_group('base.group_user')
        if not is_authorized and (not partner.website_published or partner.membership_state == 'none'):
            raise NotFound()
        values = {
            'partner': partner,
            'main_object': partner,
        }
        return request.render("website_partner.partner_page", values)