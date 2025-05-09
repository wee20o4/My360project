from odoo import http
from odoo.http import request
from werkzeug.exceptions import NotFound

class MembershipProfileSearchController(http.Controller):
    @http.route('/membership', type='http', auth='public', website=True)
    def list_members(self, **kwargs):
        members = request.env['res.partner'].sudo().search([
            ('membership_state', '!=', 'none'),
            ('website_published', '=', True),
        ])
        for member in members:
            if not member.company_name and member.parent_id:
                member.company_name = member.parent_id.name or ''
        return request.render('membership_profile_search.membership_profile_search_list_template', {
            'members': members,
            'search': kwargs.get('search', '')
        })

    @http.route('/partners/<model("res.partner"):partner>', type='http', auth='public', website=True)
    def member_detail(self, partner, **kwargs):
        # Check if the user has internal permissions (e.g., base.group_user)
        is_authorized = request.env.user.has_group('base.group_user')
<<<<<<< HEAD
=======
        
        # Restrict access for public users to published profiles with active membership
>>>>>>> parent of 5fd2722 (Noting)
        if not is_authorized and (not partner.website_published or partner.membership_state == 'none'):
            raise NotFound()
        values = {
            'partner': partner,
            'main_object': partner,
        }
        return request.render("website_partner.partner_page", values)