# -*- coding: utf-8 -*-

import datetime
import logging
from dateutil.relativedelta import relativedelta
from unittest.mock import patch

from odoo import _

from odoo.addons.membership.tests.common import TestMembershipCommon
from odoo.tests import tagged
from odoo.tests.common import TransactionCase, HttpCase, tagged

LOG = logging.getLogger(__name__)

# AIzaSyC083DDlFDAW4hVQdtt-TJnJicdM6unvlY


@tagged('post_install', '-at_install')
class TestMemberShipCustom(HttpCase):
    def setUp(self, *args, **kwargs):
        super().setUp(*args, **kwargs)
        self.user = self.env.ref('base.public_user')
        self.periodict = self.env['product.periodic.template'].create({
            'periodicity': 'quarterly'
        })
        self.membership_1 = self.env['product.product'].create({
            'membership': True,
            'membership_date_from': datetime.date.today() + relativedelta(days=-2),
            'membership_date_to': datetime.date.today() + relativedelta(months=1),
            'name': 'Basic Limited',
            'membership_product_tmp_type': 'recurring',
            'periodic_id': self.periodict.id,
            'type': 'service',
            'list_price': 100.00,
        })
        self.membership_2 = self.env['product.product'].create({
            'membership': True,
            'membership_date_from': datetime.date.today() + relativedelta(days=-2),
            'membership_date_to': datetime.date.today() + relativedelta(months=1),
            'name': 'Basic Limited',
            'membership_product_tmp_type': 'duration',
            'type': 'service',
            'list_price': 100.00,
        })
        self.partner = self.env['res.partner'].create({
            'name': 'Test partner 1', 'is_published': False,
        })
        
    def test_membership_product_recurring(self):
        membership_1 = self.env['product.product'].create({
            'membership': True,
            'membership_date_from': None,
            'membership_date_to': None,
            'name': 'Basic Limited',
            'membership_product_tmp_type': 'recurring',
            'periodic_id': self.periodict.id,
            'type': 'service',
            'list_price': 100.00,
        })
        self.assertEqual(membership_1.membership_date_to, datetime.date.today())
        self.assertEqual(membership_1.membership_date_from, datetime.date.today())
        print('PASSED')

    def test_membership_product_duration(self):
        membership_1 = self.env['product.product'].create({
            'membership': True,
            'membership_date_from': datetime.date.today() + relativedelta(days=-2),
            'membership_date_to': datetime.date.today() + relativedelta(days=10),
            'name': 'Basic Limited',
            'membership_product_tmp_type': 'duration',
            'periodic_id': self.periodict.id,
            'type': 'service',
            'list_price': 100.00,
        })
        self.assertEqual(membership_1.membership_date_from, datetime.date.today() + relativedelta(days=-2))
        self.assertEqual(membership_1.membership_date_to,datetime.date.today() + relativedelta(days=10)) 
        print('PASSED')

    def test_extenstion_membership(self):
        self.authenticate('admin', 'admin')
        partner = self.partner
        # Create duration membership
        invoice = partner.create_membership_invoice(self.membership_2, 75.0)
        invoice.action_post()
        line_type = self.env.ref('membership_profile.resume_type_join_membership', raise_if_not_found=True)
        self.assertTrue(len(partner.membership_resume_ids.filtered(lambda e: e.line_type_id.id == line_type.id)) > 0)
        self.assertEqual(
            self.partner.membership_start,
            self.membership_2.membership_date_from,
            'membership: date from membership product recurring should be equal invoice date'
        )
        self.assertEqual(
            self.partner.membership_stop,
            self.membership_2.membership_date_to,
            'membership: date to membership product recurring should be equal %s' % (invoice.invoice_date + self.periodict._get_delta_periodict())
        )
        # Extend Membership recurring
        invoice_recurring = partner.create_membership_invoice(self.membership_1, 0.75)
        invoice_recurring.action_post()
        line_type = self.env.ref('membership_profile.resume_type_extend_membership', raise_if_not_found=True)
        self.assertTrue(partner.membership_resume_ids.filtered(lambda e: e.line_type_id.id == line_type.id).exists())

        self.assertEqual(len(partner.membership_resume_ids), 2)
        print(partner._get_membership_resume())

    def test_membership_date_product_type_recurring(self):
        self.authenticate("admin", "admin")
        partner = self.partner
        invoice = partner.create_membership_invoice(self.membership_1, 75.0)
        self.assertEqual(
            invoice.state, 'draft',
            'membership: new subscription should create a draft invoice')
        self.assertEqual(
            invoice.invoice_line_ids[0].product_id, self.membership_1,
            'membership: new subscription should create a line with the membership as product')

        self.assertEqual(
            self.partner.membership_state, 'waiting',
            'membership: new membership should be in waiting state')
        invoice.action_post()
        self.assertEqual(
            self.partner.membership_start,
            invoice.invoice_date,
            'membership: date from membership product recurring should be equal invoice date'
        )
        self.assertEqual(
            self.partner.membership_stop,
            invoice.invoice_date + self.periodict._get_delta_periodict(),
            'membership: date to membership product recurring should be equal %s' % (invoice.invoice_date + self.periodict._get_delta_periodict())
        )
        self.assertTrue(partner.is_published)
        print('PASSED')
        
    def test_membership_date_product_type_duration(self):
        self.authenticate("admin", "admin")
        partner = self.partner
        invoice = partner.create_membership_invoice(self.membership_2, 75.0)
        self.assertEqual(
            invoice.state, 'draft',
            'membership: new subscription should create a draft invoice')
        self.assertEqual(
            invoice.invoice_line_ids[0].product_id, self.membership_2,
            'membership: new subscription should create a line with the membership as product')

        self.assertEqual(
            self.partner.membership_state, 'waiting',
            'membership: new membership should be in waiting state')
        invoice.action_post()
        self.assertEqual(
            self.partner.membership_start,
            self.membership_2.membership_date_from,
            'membership: date from membership product recurring should be equal invoice date'
        )
        self.assertEqual(
            self.partner.membership_stop,
            self.membership_2.membership_date_to,
            'membership: date to membership product recurring should be equal %s' % (invoice.invoice_date + self.periodict._get_delta_periodict())
        )
        print('PASSED')