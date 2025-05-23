# -*- coding: utf-8 -*-
import math
import logging
from datetime import datetime

from werkzeug.exceptions import Forbidden, NotFound
from odoo import http
from odoo.addons.http_routing.models.ir_http import unslug, slug
from odoo.http import request
from odoo.osv import expression

_logger = logging.getLogger(__name__)

class WebsitePartnerPublicPage(http.Controller):
    _partner_per_page = 30

    def _prepare_all_partners_values(self, partners):
        partner_values = []
        for partner in partners:
            socials = partner.social_ids
            vcard = partner._get_vcard()
            data = {
                'id': partner.id,
                'slug': slug(partner),
                'name': partner.name,
                'phone': partner.phone,
                'email': partner.email,
                'title': partner.title.shortcut,
                'function': partner.function,
                'registered_business': partner.registered_business,
                'company_name': partner.company_id.name,
                'badge_count': 1,  # len(user.badge_ids),
                'website': partner.website,
                'website_published': partner.website_published,
                'vcard': vcard,
                'address': partner._partner_full_address(),
            }
            if not partner.website_qr:
                partner._compute_website_qr_code()
            data.update({'website_qr': partner.website_qr.decode('utf-8')})
            if partner.parent_id:
                data['parent'] = {'id': partner.parent_id.id, 'name': partner.parent_id.name}
            if not partner.specific_business:
                data['registered_business'] = partner.parent_id.registered_business
            else:
                data['parent'] = dict()
            if socials:
                socials_list = []
                for social in socials:
                    socials_list.append({'type': social.social_type, 'link': social.link})
                data['socials'] = socials_list
            else:
                data['socials'] = []
            partner_values.append(data)
        return partner_values

    @http.route(['/partners/members', '/partners/members/page/<int:page>'], type='http', auth="user", website=True, csrf=False)
    def view_all_partners_page(self, page=1, **kwargs):
        render_values = self.partners_page(page=page, **kwargs)
        return request.render("membership_profile.partner_member_page", render_values)

    @http.route(['/snippets/partners/members', '/snippets/partners/members/page/<int:page>'],
                type='json', auth="public", website=True)
    def snippet_partner(self, page=1, **kwargs):
        render_values = self.partners_page(page=page, filter_title=False, **kwargs)
        return render_values

    def partners_page(self, page=1, **kwargs):
        Partner = request.env['res.partner']
        dom = [
            ('website_published', '=', True),
            ('membership_state', 'in', ['paid', 'free', 'invoiced']),
            ('parent_id', '!=', False),
        ]
        current_time = datetime.now()
        dom = expression.AND([['&', ('membership_start', '<=', current_time), ('membership_stop', '>=', current_time)], dom])
        current_website = request.env['website'].get_current_website()
        if kwargs.get("filter_title", True):
            if current_website.value_field_filter_member != 'all':
                cond = ('title.shortcut', 'ilike', current_website.value_field_filter_member)
                dom.append(cond)
        categories = kwargs.get('category_id')
        if categories:
            dom.extend(categories)
        search_term = kwargs.get('search')
        group_by = kwargs.get('group_by', False)
        render_values = {
            'search': search_term,
            'group_by': group_by or 'all',
        }
        if search_term:
            normalized_search = Partner._normalize_search_term(search_term)
            dom = expression.AND([[
                '|', '|', '|', '|', '|', '|', '|', '|',
                ('normalized_name', 'ilike', f'%{normalized_search}%'),
                ('normalized_function', 'ilike', f'%{normalized_search}%'),
                ('normalized_registered_business', 'ilike', f'%{normalized_search}%'),
                ('normalized_commercial_company_name', 'ilike', f'%{normalized_search}%'),
                ('normalized_street', 'ilike', f'%{normalized_search}%'),
                ('normalized_city', 'ilike', f'%{normalized_search}%'),
                ('normalized_zip', 'ilike', f'%{normalized_search}%'),
                ('normalized_parent_registered_business', 'ilike', f'%{normalized_search}%'),
                ('normalized_country_name', 'ilike', f'%{normalized_search}%'),
            ], dom])

        partner_count = Partner.sudo().search_count(dom)
        if partner_count:
            page_count = math.ceil(partner_count / self._partner_per_page)
            pager = request.website.pager(
                url="/partners/members",
                total=partner_count,
                page=page,
                step=self._partner_per_page,
                scope=page_count
            )
            partners = Partner.sudo().search(dom, limit=self._partner_per_page, offset=pager['offset'])
            partner_values = self._prepare_all_partners_values(partners)
        else:
            partner_values = []
            pager = {'page_count': 0}

        dict_title_filter = dict(Partner.sudo()._get_member_member_title_filter())

        render_values.update({
            'partners': partner_values,
            'pager': pager,
            'search_count': partner_count,
        })
        if kwargs.get('filter_title', True):
            render_values.update({
                'current_website_filter_member': dict_title_filter.get(current_website.value_field_filter_member, '/'),
                'current_website_filter_member_key': current_website.value_field_filter_member,
            })
        return render_values

    @http.route(['/partners/members/<partner_id>'], type='http', auth="public", website=True)
    def partners_detail(self, partner_id, **post):
        back_url = post.get('back_url', None)
        _, partner_id = unslug(partner_id)
        if partner_id:
            partner_sudo = request.env['res.partner'].sudo().browse(partner_id)
            is_website_restricted_editor = request.env['res.users'].has_group('website.group_website_restricted_editor')
            if partner_sudo.exists() and (partner_sudo.website_published or is_website_restricted_editor):
                values = {
                    'main_object': partner_sudo,
                    'partner': partner_sudo,
                    'edit_page': False,
                    'address': partner_sudo._partner_full_address(),
                    'back_path': back_url,
                }
                return request.render("membership_profile.partner_page", values)
        return request.not_found()

    @http.route(['/website/set-value-filter-member'], type='json', auth='user', website=True)
    def set_value_filter_member(self, **post):
        if not request.env.user.has_group('website.group_website_restricted_editor'):
            raise NotFound()
        website = request.env['website'].get_current_website()
        if 'value_field_filter_member' in post:
            website.write({'value_field_filter_member': post['value_field_filter_member']})

    @http.route(['/website/set-show-committee'], type='json', auth='user', website=True)
    def set_show_committee(self, **post):
        if not request.env.user.has_group('website.group_website_restricted_editor'):
            raise NotFound()
        Partner = request.env['res.partner'].sudo()
        if 'partner_id' in post:
            partner = Partner.browse((int(post['partner_id'])))
            partner.set_show_committee()

    @http.route(['/snippet/member_committee/', '/snippet/member_committee/<committee_id>/'], type='json', auth="public", website=True)
    def snippet_member_committee(self, committee_id=None, **kwargs):
        if not committee_id:
            committee = request.env['membership.committee'].sudo().search([])
            if len(committee) > 0:
                committee_id = committee[0].id
            else:
                return list()

        PartnerCommittee = request.env['membership.partner.committee'].sudo()
        CommitteeType = request.env['membership.committee.tmp.type'].sudo()
        committee = request.env['membership.committee'].sudo().browse(int(committee_id))

        committee_types = CommitteeType.search([('visible', '=', True)])
        committee_result = list()
        for cmm_type in committee_types:
            member_committee_type = PartnerCommittee.search(['&', ('committee_id', '=', int(committee_id)), ('committee_tmp_id.tmp_type_id', '=', cmm_type.id)])
            committee_result.append({
                'partners': self.partner_committee_data(member_committee_type),
                'template_name': cmm_type.name,
                'template_specific': cmm_type.specific_type,
            })

        result = dict()
        result['data'] = committee_result
        result['committee_name'] = committee.name
        result['committee_data_start'] = committee.date_start.strftime("%d/%m/%Y")
        result['committee_data_end'] = committee.date_end.strftime("%d/%m/%Y")
        return result

    def partner_committee_data(self, partner_committees):
        position_raise = 2
        result = list()
        len_committee = len(partner_committees)
        for e, record in enumerate(partner_committees):
            partner = record.partner_id
            partner_data = self._prepare_all_partners_values([partner])[0]
            raise_tmp = record.committee_tmp_id.raise_in_template
            partner_data['committee'] = {
                'name': record.committee_tmp_id.name,
                'description': record.committee_tmp_id.description,
                'raise_in_tmp': raise_tmp,
            }
            if not raise_tmp:
                partner_data['committee'].update({
                    'order': 1 if len_committee == 1 else e if e != position_raise else e + 1,
                })
            else:
                partner_data['committee']['order'] = position_raise
            result.append(partner_data)
        return result