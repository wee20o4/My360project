# extra-addons/membership_profile_search/controllers/main.py

from xml.dom import ValidationErr
from odoo import http
from odoo.http import request
from werkzeug.exceptions import NotFound
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
    """
    Class controller xử lý các yêu cầu HTTP liên quan đến tìm kiếm và hiển thị thông tin hội viên trên website.
    Cung cấp các route để liệt kê danh sách hội viên và hiển thị chi tiết hội viên.
    """

    @http.route('/membership', type='http', auth='public', website=True)
    def list_members(self, **kwargs):
        """
        Hàm xử lý yêu cầu HTTP để hiển thị danh sách hội viên trên website.
        Hỗ trợ tìm kiếm hội viên dựa trên từ khóa và lọc theo các tiêu chí như tên, công ty, ngành nghề, địa chỉ.
        
        Args:
            **kwargs: Các tham số GET từ request, bao gồm 'search' (từ khóa tìm kiếm).
        
        Returns:
            template: Render template danh sách hội viên hoặc thông báo lỗi nếu có vấn đề.
        """
        try:
            search_term = kwargs.get('search', '').strip()
            domain = [
                ('membership_state', '!=', 'none'),
                ('website_published', '=', True),
            ]

            if search_term:
                # Chuẩn hóa từ khóa tìm kiếm để hỗ trợ tìm kiếm không dấu
                normalized_search = remove_diacritics(search_term).lower()
                # Tìm kiếm trên các trường tên, công ty, ngành nghề, địa chỉ
                domain += ['|', '|', '|',
                          ('name', 'ilike', search_term),
                          ('company_name', 'ilike', search_term),
                          ('industry_id.name', 'ilike', search_term),
                          ('street', 'ilike', search_term)]

            # Tìm kiếm hội viên theo domain
            members = request.env['res.partner'].sudo().search(domain)
            for member in members:
                if not member.company_name and member.parent_id:
                    member.company_name = member.parent_id.name or ''
            
            # Render template với danh sách hội viên và từ khóa tìm kiếm
            return request.render('membership_profile_search.membership_profile_search_list_template', {
                'members': members,
                'search': search_term
            })
        except Exception as e:
            # Ghi log lỗi hệ thống nếu có ngoại lệ xảy ra
            error_trace = traceback.format_exc()
            message = "Lỗi hệ thống. Vui lòng thử lại sau."
            if isinstance(e, ValidationErr):
                message = str(e)
            request.env['ir.logging'].sudo().create({
                'name': 'MembershipProfileSearch',
                'type': 'server',
                'level': 'ERROR',
                'message': f"Error: {str(e)}\nTraceback: {error_trace}",
                'path': '/membership',
                'func': 'list_members',
                'line': 1,
            })
            # Render template lỗi với thông báo
            return request.render('website.error', {'error': message}, status=500)

    @http.route('/partners/<model("res.partner"):partner>', type='http', auth='public', website=True)
    def member_detail(self, partner, **kwargs):
        """
        Hàm xử lý yêu cầu HTTP để hiển thị trang chi tiết của một hội viên.
        Kiểm tra quyền truy cập và trạng thái công khai của hội viên trước khi hiển thị.
        
        Args:
            partner (res.partner): Đối tượng hội viên cần hiển thị.
            **kwargs: Các tham số bổ sung từ request.
        
        Returns:
            template: Render template chi tiết hội viên hoặc raise NotFound nếu không đủ quyền.
        """
        is_authorized = request.env.user.has_group('base.group_user')
        if not is_authorized and (not partner.website_published or partner.membership_state == 'none'):
            raise NotFound()
        values = {
            'partner': partner,
            'main_object': partner,
        }
        # Render template chi tiết hội viên
        return request.render("website_partner.partner_page", values)