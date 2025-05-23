# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
from odoo.addons.http_routing.models.ir_http import slug

import re
import logging
import base64
import io
import qrcode
from unidecode import unidecode
from werkzeug import urls

_logger = logging.getLogger(__name__)

try:
    import vobject
except ImportError:
    _logger.warning("`vobject` Python module not found, iCal file generation disabled. Consider installing this module if you want to generate iCal files")
    vobject = None

VCARD_FORMAT = '''
BEGIN:VCARD
VERSION:4.0
N:{name};
TEL;TYPE=work;Phone=voice:{mobile_phone}
TEL;TYPE=home;Home=voice:{home_phone}
EMAIL:{email}
ORG:{company_name}
TITLE:{function}
ADR;TYPE=WORK,PREF:;;{address}
URL:{website}
{more_url}
END:VCARD
'''

def create_vcard(name, phone_work=None, phone_home=None, email=None, org=None,
                 title=None, address=None, url=None, another_urls=None):
    def split_name(full_name):
        names = full_name.split()
        if len(names) > 1:
            family_name = names[-1]
            given_name = " ".join(names[:-1])
        else:
            family_name = full_name
            given_name = ""
        return family_name, given_name

    try:
        vcard = vobject.vCard()
        family_name, given_name = split_name(name)
        vcard.add('fn').value = name
        vcard.add('n').value = vobject.vcard.Name(family=family_name, given=given_name)
        if phone_work:
            vcard.add('tel').value = phone_work
        if phone_home:
            vcard.add('tel').value = phone_home
        if email:
            vcard.add('email').value = email
        if org:
            vcard.add('org').value = [org]
        if title:
            vcard.add('title').value = title
        if address:
            attr_address = dict()
            if address.get('street'):
                attr_address['street'] = address['street']
            if address.get('city'):
                attr_address['city'] = address['city']
            if address.get('region'):
                attr_address['region'] = address['region']
            if address.get('code'):
                attr_address['code'] = address['code']
            if address.get('country'):
                attr_address['country'] = address['country']
            if attr_address:
                vcard.add('adr').value = vobject.vcard.Address(**attr_address)
        if url:
            vcard.add('url').value = url
        if another_urls:
            for social in another_urls:
                if not social.link:
                    continue
                vcard.add('x-socialprofile').value = social.link
        return vcard.serialize()
    except Exception as e:
        _logger.error('ERROR when create Vcard %s ' % str(e))
        raise UserError(e)

class ResPartner(models.Model):
    _inherit = 'res.partner'

    contact_qr = fields.Binary('Contact QR', attachment=False,
                              store=True, readonly=True, compute='_compute_qr_code')
    website_qr = fields.Binary('Website QR', attachment=False,
                              store=True, readonly=True, compute='_compute_website_qr_code')
    social_ids = fields.One2many('member.social', 'partner_id', string='Social links')
    registered_business = fields.Char(string=_('Registered Business'), required=False)
    specific_business = fields.Boolean(default=False)
    profile_tmp = fields.Selection(string=_('Profile Template'), selection=[('tmp_1', 'Template 1'), ('tmp_2', 'Template 2')],
                                  default='tmp_1', required=True)
    committee_ids = fields.One2many(comodel_name='membership.partner.committee',
                                   inverse_name='partner_id', copy=False, string='Committees')
    is_committee = fields.Boolean(compute='_compute_committee', store=True, copy=False)
    show_journal_committee = fields.Boolean(default=True)
    membership_resume_ids = fields.One2many(comodel_name='membership.resume.line',
                                           inverse_name='partner_id', copy=False, string='Membership Resume')
    # Áp dụng tìm kiếm tương đối
    normalized_name = fields.Char(
        string='Normalized Name',
        compute='_compute_normalized_fields',
        store=True,
        index=True,
    )
    normalized_function = fields.Char(
        string='Normalized Function',
        compute='_compute_normalized_fields',
        store=True,
        index=True,
    )
    normalized_registered_business = fields.Char(
        string='Normalized Registered Business',
        compute='_compute_normalized_fields',
        store=True,
        index=True,
    )
    normalized_commercial_company_name = fields.Char(
        string='Normalized Commercial Company Name',
        compute='_compute_normalized_fields',
        store=True,
        index=True,
    )
    normalized_street = fields.Char(
        string='Normalized Street',
        compute='_compute_normalized_fields',
        store=True,
        index=True,
    )
    normalized_city = fields.Char(
        string='Normalized City',
        compute='_compute_normalized_fields',
        store=True,
        index=True,
    )
    normalized_zip = fields.Char(
        string='Normalized Zip',
        compute='_compute_normalized_fields',
        store=True,
        index=True,
    )
    normalized_parent_registered_business = fields.Char(
        string='Normalized Parent Registered Business',
        compute='_compute_normalized_fields',
        store=True,
        index=True,
    )
    normalized_country_name = fields.Char(
        string='Normalized Country Name',
        compute='_compute_normalized_fields',
        store=True,
        index=True,
    )

    @api.constrains('specific_business')
    def _specific_business_required_company_multi_contract(self):
        for record in self:
            if record.specific_business:
                if record.is_company:
                    raise UserError(_('Only use for Individual membership'))
                else:
                    parent = record.parent_id
                    if len(self.env['res.partner'].search([('parent_id', '=', parent.id)])) < 2:
                        raise UserError(_('Only usage for Company has many contact'))

    def set_show_committee(self):
        self.ensure_one()
        current = self.show_journal_committee
        self.write({'show_journal_committee': not current})

    @api.depends('committee_ids')
    def _compute_committee(self):
        for record in self:
            if len(record.committee_ids) > 0:
                record.is_committee = True
            else:
                record.is_committee = False

    @api.depends('name', 'function', 'registered_business', 'commercial_company_name', 'street', 'city', 'zip', 'parent_id.registered_business', 'country_id.name')
    def _compute_normalized_fields(self):
        for partner in self:
            def normalize_field(value):
                if not value:
                    return ''
                cleaned = re.sub(r'\s+', ' ', re.sub(r'[^\w\s]', '', value)).strip()
                return unidecode(cleaned).lower()

            partner.normalized_name = normalize_field(partner.name)
            partner.normalized_function = normalize_field(partner.function)
            partner.normalized_registered_business = normalize_field(partner.registered_business)
            partner.normalized_commercial_company_name = normalize_field(partner.commercial_company_name)
            partner.normalized_street = normalize_field(partner.street)
            partner.normalized_city = normalize_field(partner.city)
            partner.normalized_zip = normalize_field(partner.zip)
            partner.normalized_parent_registered_business = normalize_field(partner.parent_id.registered_business)
            partner.normalized_country_name = normalize_field(partner.country_id.name)

    def _normalize_search_term(self, term):
        """Normalize search term: remove special chars, extra spaces, and accents."""
        if not term:
            return term
        cleaned = re.sub(r'\s+', ' ', re.sub(r'[^\w\s]', '', term)).strip()
        return unidecode(cleaned).lower()

    def _get_committe_journal(self):
        self.ensure_one()
        result = []
        if not self.committee_ids:  # Fixed: Changed len < 0 to not self.committee_ids
            return result

        committee_index = 0
        for committee in self.committee_ids:
            committee_index += 1
            result.append({
                'committee_index': committee_index,
                'committee_name': committee.committee_id.name,
                'name': committee.committee_tmp_id.name,
                'description': committee.description,
                'date_start': committee.committee_id.date_start.strftime("%d/%m/%Y"),
                'date_end': committee.committee_id.date_end.strftime("%d/%m/%Y"),
            })
        return result

    def _get_membership_resume(self):
        self.ensure_one()
        result = []
        resume_ids = self.env['membership.resume.line'].sudo().search([('partner_id', '=', self.id)], order="date_start desc")
        if len(resume_ids) < 1:
            return result

        index = 0
        for resume in resume_ids:
            index += 1
            result.append({
                'index': index,
                'name': resume.name,
                'description': resume.description,
                'date_start': resume.date_start.strftime("%d/%m/%Y"),
                'date_end': resume.date_end.strftime("%d/%m/%Y") if resume.date_end else _('Current'),
                'month_year': resume.date_start.strftime("%m-%Y"),
            })
        return result

    def _compute_website_url(self):
        super()._compute_website_url()
        for partner in self:
            partner.website_url = "/partners/members/%s" % slug(partner)

    def _partner_full_address(self):
        self.ensure_one()
        partner = self
        address = ""
        if partner.street:
            address += partner.street + ", "
        if partner.street2:
            address += partner.street2 + ", "
        if partner.city:
            address += partner.city + ", "
        if partner.state_id:
            address += partner.state_id.name + ", "
        if partner.zip:
            address += partner.zip + ", "
        if partner.country_id:
            address += partner.country_id.name
        return address

    def _partner_dict_address(self) -> dict:
        self.ensure_one()
        partner = self
        return {
            'street': partner.street,
            'city': partner.city,
            'region': partner.state_id.name,
            'code': partner.zip,
            'country': partner.country_id.name,
        }

    def _compute_website_qr_code(self):
        for record in self:
            url = urls.url_join(record.get_base_url(), record.website_url)
            qr = qrcode.QRCode(version=1,
                               error_correction=qrcode.constants.ERROR_CORRECT_L,
                               box_size=10,
                               border=4)
            qr.add_data(url.encode('utf-8'))
            qr.make(fit=True)
            img = qr.make_image(fill_color="black", back_color="white")
            temp = io.BytesIO()
            img.save(temp, format='PNG')
            record.website_qr = base64.b64encode(temp.getvalue())

    FIELDS_QR = ['name', 'function', 'website', 'email', 'phone', 'mobile', 'social_ids']

    @api.depends(lambda self: self.FIELDS_QR)
    def _compute_qr_code(self):
        for record in self:
            vcard_data = record._get_vcard()
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(vcard_data.encode('utf-8'))
            qr.make(fit=True)
            img = qr.make_image(fill_color="black", back_color="white")
            temp = io.BytesIO()
            img.save(temp, format='PNG')
            qr_image = base64.b64encode(temp.getvalue())
            record.contact_qr = qr_image

    def refresh_new_imge_qr_code(self):
        self.ensure_one()
        self._compute_qr_code()

    def _get_vcard(self):
        self.ensure_one()
        record = self
        if vobject:
            name = record.name
            phone_home = record.phone
            phone_work = record.mobile
            email = record.email
            org = record.parent_id.name
            title = record.function
            address = record._partner_dict_address()
            url = record.website
            vcard_data = create_vcard(name, phone_work, phone_home, email, org,
                                      title, address, url, another_urls=record.social_ids)
            if not vcard_data:
                vcard_data = record._contact_qr_code()
        else:
            vcard_data = record._contact_qr_code()
        return vcard_data

    def _contact_qr_code(self):
        self.ensure_one()
        more_url = ""
        for social in self.social_ids:
            if social.link:
                more_url += f"X-SOCIALPROFILE;TYPE={social.social_type}:{social.link}\n"
        value_qr = VCARD_FORMAT.format(
            name=self.full_name_vcard(),
            home_phone=self.phone,
            mobile_phone=self.mobile,
            email=self.email,
            company_name=self.parent_id.name,
            function=self.function,
            address=self.full_address_vcard(),
            more_url=more_url,
            website=self.website
        )
        return value_qr

    def full_address_vcard(self):
        """The method return full address of format Vcard"""
        self.ensure_one()
        partner = self
        address = ""
        if partner.street:
            address += partner.street
        if partner.street2:
            address += ";" + partner.street2
        if partner.city:
            address += ";" + partner.city
        if partner.state_id:
            address += ";" + partner.state_id.name
        if partner.zip:
            address += ";" + partner.zip
        if partner.country_id:
            address += ";" + partner.country_id.name
        return address

    def full_name_vcard(self):
        self.ensure_one()
        return self.name.replace(" ", ";")

    def _get_member_member_title_filter(self):
        titles = self.env['res.partner.title'].sudo().search([])
        return [('all', _('All'))] + [(title.shortcut, title.name) for title in titles]