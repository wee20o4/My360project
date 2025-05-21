import logging

from urllib.parse import urlparse, urlunparse

from odoo import api, models, fields, _


_logger = logging.getLogger(__name__)


DEFAULT_SOCIAL = [
    ('facebook', 'Facebook'),
    ('twitter', 'Twitter'),
    ('linkedin', 'Linked In'),
    ('github', 'GitHub'),
    ('youtube', 'YouTube'),
    ('instagram', 'Instagram'),
    ('zalo', 'Zalo'), # Currently, Odoo doesn't support Icon Type Zalo
    ('tiktok', 'TikTok'),  # Currently, Odoo doesn't support Icon Type tiktok
]

def normalize_url(url):
    if not url:
        return ""
    parsed_url = urlparse(url)

    # If the scheme is not present, replace it with "https"
    if not parsed_url.scheme:
        netloc = parsed_url.netloc
        path = parsed_url.path
        parsed_url = parsed_url._replace(scheme="https")
        if not netloc and path:
            parsed_url = parsed_url._replace(netloc=path, path='')

    # Reconstruct the URL
    normalized_url = urlunparse(parsed_url)

    return normalized_url


class Social(models.Model):
    _name = 'member.social'
    _description = 'Partner Socials'
    
    social_type = fields.Selection(selection=DEFAULT_SOCIAL, required=True)
    # is_other = fields.Boolean(default=False)
    link = fields.Char('Link Social')
    partner_id = fields.Many2one('res.partner', 'Member', required=True)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if 'link' in vals:
                vals['link'] = normalize_url(vals['link'])
        return super().create(vals_list)

    def write(self, vals):
        if 'link' in vals:
            vals['link'] = normalize_url(vals['link'])
        return super(Social, self).write(vals)