from odoo import http
from odoo.http import request

class WebsitePartner(http.Controller):

    @http.route(['/partners'], type='http', auth='public', website=True)
    def list_partners(self, **kwargs):
        # Loại bỏ domain hoặc điều chỉnh nếu cần hiển thị cả công ty
        domain = []  # Lấy tất cả partner
        # Nếu chỉ muốn cá nhân, dùng: domain = [('is_company', '=', False)]
        partners = request.env['res.partner'].sudo().search(domain)
        if not partners:
            # Hiển thị thông báo trên giao diện nếu không có dữ liệu
            return request.render('custom_partners.website_partner_list', {
                'partners': [],
                'message': 'Hiện tại chưa có hội viên nào trong hệ thống.'
            })
        return request.render('custom_partners.website_partner_list', {
            'partners': partners
        })