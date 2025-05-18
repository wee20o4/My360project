# extra-addons/membership_profile_search/controllers/main.py

from odoo import http # type: ignore
from odoo.http import request # type: ignore
from werkzeug.exceptions import NotFound # type: ignore
import unicodedata
import re
import traceback

def remove_diacritics(text):
    """
    Hàm chuẩn hóa chuỗi văn bản, loại bỏ dấu tiếng Việt để hỗ trợ tìm kiếm không dấu.
    Args:
        text (str): Chuỗi văn bản đầu vào cần chuẩn hóa.
    Returns:
        str: Chuỗi văn bản đã được loại bỏ dấu và thay thế các ký tự đặc biệt như 'đ', 'Đ'.
    """
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
                normalized_search = remove_diacritics(search_term).lower()
                domain += ['|', '|', '|',
                    ('name', 'ilike', search_term),
                    ('company_name', 'ilike', search_term),
                    ('industry_id.name', 'ilike', search_term),
                    ('street', 'ilike', search_term)]

            members = request.env['res.partner'].search(domain)
            for member in members:
                if not member.company_name and member.parent_id:
                    member.company_name = member.parent_id.name or ''
                elif not member.company_name:
                    member.company_name = member.name if member.is_company else ''

            return request.render('membership_profile_search.membership_profile_search_list_template', {
                'members': members,
                'search': search_term
            })
        except Exception as e:
            error_trace = traceback.format_exc()
            request.env['ir.logging'].create({
                'name': 'MembershipProfileSearch',
                'type': 'server',
                'level': 'ERROR',
                'message': f"Error: {str(e)}\nTraceback: {error_trace}",
                'path': '/membership',
                'func': 'list_members',
                'line': 1,
            })
            return request.render('website.page_404', {'error': 'Không thể tải danh sách hội viên. Vui lòng thử lại sau.'}, status=500)

    @http.route('/partners/<model("res.partner"):partner>', type='http', auth='public', website=True)
    def member_detail(self, partner, **kwargs):
        if not partner.website_published or partner.membership_state == 'none':
            if not request.env.user.has_group('base.group_user'):
                raise NotFound()
        values = {
            'partner': partner,
            'main_object': partner,
        }
        return request.render("website_partner.partner_page", values)