from odoo import fields, models

class Member(models.Model):
    _name = 'member.member'
    _description = 'Member'

    name = fields.Char(string='Name', required=True)
    email = fields.Char(string='Email')
    image_1920 = fields.Image(string='Avatar', max_width=1920, max_height=1920)
    company_name = fields.Char(string='Company Name')
    industry_id = fields.Many2one('res.partner.industry', string='Industry')
    street = fields.Char(string='Street')
    city = fields.Char(string='City')
    state_id = fields.Many2one('res.country.state', string='State')
    country_id = fields.Many2one('res.country', string='Country')