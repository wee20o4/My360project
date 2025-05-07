# extra-addons/membership_profile_search/models/membership_profile_search.py
from odoo import fields, models, api

class MembershipProfileSearch(models.Model):
    _inherit = 'res.partner'
    _description = 'Membership Profile Search'

    image_1920 = fields.Image(string='Avatar', max_width=1920, max_height=1920)
    company_name = fields.Char(string='Company Name', store=True, compute='_compute_company_name', readonly=False)
    industry_id = fields.Many2one('res.partner.industry', string='Industry')
    street = fields.Char(string='Street')
    city = fields.Char(string='City')
    state_id = fields.Many2one('res.country.state', string='State')
    country_id = fields.Many2one('res.country', string='Country')

    @api.depends('parent_id', 'parent_id.name')
    def _compute_company_name(self):
        for partner in self:
            if partner.parent_id:
                partner.company_name = partner.parent_id.name or ''
            elif partner.is_company:
                partner.company_name = partner.name or ''
            else:
                partner.company_name = ''