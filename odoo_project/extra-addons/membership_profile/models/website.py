# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, _


class Website(models.Model):
    _inherit = "website"

    default_filter_member = fields.Char('Default filter Member', default='title')
    value_field_filter_member = fields.Char(help='Value of field default filter')
