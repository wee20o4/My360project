from odoo import fields, models, api # type: ignore
from .. import utils

class MembershipProfileSearch(models.Model):
    _inherit = 'res.partner'
    _description = 'Membership Profile Search'

    image_1920 = fields.Image(string='Profile Image', max_width=1920, max_height=1920)
    company_name = fields.Char(string='Company Name', store=True, compute='_compute_company_name', readonly=False)
    industry_id = fields.Many2one('res.partner.industry', string='Industry')
    street = fields.Char(string='Street')
    city = fields.Char(string='City')
    state_id = fields.Many2one('res.country.state', string='State')
    country_id = fields.Many2one('res.country', string='Country')
    name_no_diacritics = fields.Char(
        string='Name No Diacritics', store=True, compute='_compute_no_diacritics', index=True
    )
    company_name_no_diacritics = fields.Char(
        string='Company Name No Diacritics', store=True, compute='_compute_no_diacritics', index=True
    )
    street_no_diacritics = fields.Char(
        string='Street No Diacritics', store=True, compute='_compute_no_diacritics', index=True
    )

    @api.depends('parent_id', 'parent_id.name', 'name', 'is_company')
    def _compute_company_name(self):
        for partner in self:
            partner.company_name = (
                partner.parent_id.name if partner.parent_id and partner.parent_id.name
                else partner.name if partner.is_company and partner.name
                else ''
            )

    @api.depends('name', 'company_name', 'street')
    def _compute_no_diacritics(self):
        for partner in self:
            partner.name_no_diacritics = utils.remove_diacritics(partner.name or '')
            partner.company_name_no_diacritics = utils.remove_diacritics(partner.company_name or '')
            partner.street_no_diacritics = utils.remove_diacritics(partner.street or '')