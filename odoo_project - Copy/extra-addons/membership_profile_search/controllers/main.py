# extra-addons/membership_profile_search/controllers/main.py
from odoo import http
from odoo.http import request
from werkzeug.exceptions import NotFound
from .. import utils
import traceback
import json

class MembershipProfileSearchController(http.Controller):
    @http.route('/membership', type='http', auth='public', website=True)
    def list_members(self, **kwargs):
        try:
            search_term = ' '.join(kwargs.get('search', '').strip().split())
            industry = ' '.join(kwargs.get('industry', '').strip().split())
            domain = [
                ('membership_state', '!=', 'none'),
                ('website_published', '=', True),
            ]

            if search_term:
                normalized_search = utils.remove_diacritics(search_term).lower()
                domain += ['|', '|', '|',
                    ('name_no_diacritics', 'ilike', normalized_search),
                    ('company_name_no_diacritics', 'ilike', normalized_search),
                    ('industry_id.name', 'ilike', normalized_search),
                    ('street_no_diacritics', 'ilike', normalized_search)]

            if industry:
                normalized_industry = utils.remove_diacritics(industry).lower()
                domain += [('industry_id.name', 'ilike', normalized_industry)]

            members = request.env['res.partner'].sudo().search(domain)
            return request.render('membership_profile_search.membership_profile_search_list_template', {
                'members': members,
                'search': search_term,
                'industry': industry
            })
        except Exception as e:
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
            return request.render('website.page_404', {'error': 'Không thể tải danh sách hội viên. Vui lòng thử lại sau.'}, status=500)

    @http.route('/membership/data', type='json', auth='public', website=True)
    def get_members_data(self, **kwargs):
        try:
            search_term = ' '.join(kwargs.get('search', '').strip().split())
            industry = ' '.join(kwargs.get('industry', '').strip().split())
            page = int(kwargs.get('page', 1))
            limit = int(kwargs.get('limit', 12))
            offset = (page - 1) * limit

            domain = [
                ('membership_state', '!=', 'none'),
                ('website_published', '=', True),
            ]

            if search_term:
                normalized_search = utils.remove_diacritics(search_term).lower()
                domain += ['|', '|', '|',
                    ('name_no_diacritics', 'ilike', normalized_search),
                    ('company_name_no_diacritics', 'ilike', normalized_search),
                    ('industry_id.name', 'ilike', normalized_search),
                    ('street_no_diacritics', 'ilike', normalized_search)]

            if industry:
                normalized_industry = utils.remove_diacritics(industry).lower()
                domain += [('industry_id.name', 'ilike', normalized_industry)]

            members = request.env['res.partner'].sudo().search(domain, offset=offset, limit=limit)
            total = request.env['res.partner'].sudo().search_count(domain)
            members_data = [{
                'id': member.id,
                'name': member.name or '',
                'company_name': member.company_name or '',
                'industry_id': {'name': member.industry_id.name or ''},
                'street': member.street or '',
                'city': member.city or '',
                'state_id': {'name': member.state_id.name or ''},
                'country_id': {'name': member.country_id.name or ''},
                'image_1920': member.image_1920 or ''
            } for member in members]
            return {'members': members_data, 'total': total, 'limit': limit}
        except Exception as e:
            error_trace = traceback.format_exc()
            request.env['ir.logging'].sudo().create({
                'name': 'MembershipProfileSearch',
                'type': 'server',
                'level': 'ERROR',
                'message': f"Error: {str(e)}\nTraceback: {error_trace}",
                'path': '/membership/data',
                'func': 'get_members_data',
                'line': 1,
            })
            return {'members': [], 'total': 0, 'limit': 12}