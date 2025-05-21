# -*- coding: utf-8 -*-

import datetime
from dateutil.relativedelta import relativedelta

from odoo.addons.account.tests.common import AccountTestInvoicingCommon


class TestMembershipCommon(AccountTestInvoicingCommon):

    @classmethod
    def setUpClass(cls, chart_template_ref=None):
        super().setUpClass(chart_template_ref=chart_template_ref)

        # Test memberships
        cls.membership_1 = cls.env['product.product'].create({
            'membership': True,
            'membership_product_tmp_type': 'recurring',
            'number_date': 90,
            'start_recurring_after_assigned': False,
            'membership_date_from': datetime.date.today() + relativedelta(days=-2),
            'membership_date_to': datetime.date.today() + relativedelta(months=1),
            'name': 'Basic Limited',
            'type': 'service',
            'list_price': 100.00,
        })

        # Test people
        cls.partner_1 = cls.env['res.partner'].create({
            'name': 'Ignasse Reblochon',
        })
        cls.partner_2 = cls.env['res.partner'].create({
            'name': 'Martine Poulichette',
            'free_member': True,
        })

        cls.committee_1 = cls.env['membership.committee'].create({
            'name': 'Committee 1',
            'date_start': datetime.date.today() + relativedelta(days=-2),
            'date_end': datetime.date.today() + relativedelta(months=1),
        })
        
        cls.commitee_tmp_1 = cls.env['membership.committee.tmp'].create({
            'name': 'Committee tmp 1',
            'description': 'Des Template 1',
            'level_committee': 'lv1',
            'committee_ids': cls.committee_1,
        })

        cls.commitee_tmp_2 = cls.env['membership.committee.tmp'].create({
            'name': 'Committee tmp 2',
            'description': 'Des Template 2',
            'level_committee': 'lv1',
            'committee_ids': cls.committee_1,
        })

        cls.commitee_tmp_3 = cls.env['membership.committee.tmp'].create({
            'name': 'Committee tmp 3',
            'description': 'Des Template 3',
            'level_committee': 'lv1',
            'committee_ids': cls.committee_1,
        })