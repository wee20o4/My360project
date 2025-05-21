# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import logging
import datetime

from odoo.exceptions import ValidationError
from dateutil.relativedelta import relativedelta

from odoo import api, fields, models, _


_logger = logging.getLogger(__name__)


class Product(models.Model):
    _inherit = 'product.template'
    _description = 'Inherit Product Template mudule membership'

    TYPE_SELECTION = [
        ('recurring', 'Recurring'),
        ('duration', 'Duration'),
    ]
    
    # membership_date_from
    # membership_date_to
    membership_product_tmp_type = fields.Selection(selection=TYPE_SELECTION,
        default='duration', help=_('Membership product Template Data type'))
    periodic_id = fields.Many2one('product.periodic.template', string="Periodic", required=False)

    @api.constrains('membership_product_tmp_type')
    def _check_membership_date(self):
        for record in self:
            if record.membership_product_tmp_type != 'recurring':
                if not record.membership_date_from or not record.membership_date_to:
                    msg = _("Product with type %s required %s and %s") % ('Duration', 'Membership Date From',
                                                                          'Membership Date To')
                    raise ValidationError(msg)
    
    @api.model_create_multi
    def create(self, vals_list):
        for value in vals_list:
            if not value.get('membership_date_to'):
                value['membership_date_to'] = datetime.date.today()
            if not value.get('membership_date_from'):
                value['membership_date_from'] = datetime.date.today()
        return super().create(vals_list)


class PeriodicProductMember(models.Model):
    _name = 'product.periodic.template'
    _description = 'Recurring Template Product'

    PERIODIC_TYPE = [('daily', _('Daily')),
                    ('weekly', _('Weekly')),
                    ('quarterly', _('Quarterly')),
                    ('monthly', _('Monthly')),
                    ('yearly', _('Yearly'))]

    name = fields.Char(_('Name'), store=True, copy=False, compute='_compute_name_periodic')
    periodicity = fields.Selection(selection=PERIODIC_TYPE, default='quarterly')
    number_periodic = fields.Integer(_('Number of Periodic'), default=1)

    def _get_delta_periodict(self):
        self.ensure_one()
        if self.periodicity == 'daily':
            delta = relativedelta(days=1 * self.number_periodic)
        if self.periodicity == 'weekly':
            delta = relativedelta(weeks=1 * self.number_periodic)
        elif self.periodicity == 'monthly':
            delta = relativedelta(months=1 * self.number_periodic)
        elif self.periodicity == 'quarterly':
            delta = relativedelta(months=3 * self.number_periodic)
        elif self.periodicity == 'yearly':
            delta = relativedelta(years=1 * self.number_periodic)
        return  delta

    @api.depends('periodicity', 'number_periodic')
    def _compute_name_periodic(self):
        for record in self:
            record.name = "%s %s" % (record.number_periodic, record.periodicity.title())