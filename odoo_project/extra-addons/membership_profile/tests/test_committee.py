# -*- coding: utf-8 -*-

import json
import datetime
from dateutil.relativedelta import relativedelta
from unittest.mock import patch
from werkzeug.urls import url_encode, url_join

from odoo import _

from odoo.addons.membership.tests.common import TestMembershipCommon
from odoo.tests import tagged
from odoo.tests.common import TransactionCase, HttpCase, tagged

# python odoo-bin -c odoo.conf --log-level=test --test-enable --stop-after-init --test-tags /membership_profile:TestMemberCommittee.test_get_committee


@tagged('post_install', '-at_install')
class TestMemberCommittee(HttpCase):
    def setUp(self, *args, **kwargs):
        super().setUp(*args, **kwargs)
        self.user = self.env.ref('base.public_user')

        self.partner_1 = self.env['res.partner'].create({
            'name': 'Ignasse Reblochon',
        })
        self.partner_2 = self.env['res.partner'].create({
            'name': 'Martine Poulichette',
            'free_member': True,
        })

        self.committee_1 = self.env['membership.committee'].create({
            'name': 'Committee 1',
            'date_start': datetime.date.today() + relativedelta(days=-2),
            'date_end': datetime.date.today() + relativedelta(months=1),
        })
        
        self.commitee_tmp_1 = self.env['membership.committee.tmp'].create({
            'name': 'Committee tmp 1',
            'description': 'Des Template 1',
            'committee_ids': self.committee_1,
        })

        self.commitee_tmp_2 = self.env['membership.committee.tmp'].create({
            'name': 'Committee tmp 2',
            'description': 'Des Template 2',
            'committee_ids': self.committee_1,
            'raise_in_template': True,
        })

        self.commitee_tmp_3 = self.env['membership.committee.tmp'].create({
            'name': 'Committee tmp 3',
            'description': 'Des Template 3',
            'committee_ids': self.committee_1,
        })
        
        self.partner_member_committee_1 = self.env['membership.partner.committee'].create({
            'partner_id': self.partner_1.id,
            'committee_id': self.committee_1.id,
            'committee_tmp_id': self.commitee_tmp_1.id,
        })

        self.partner_member_committee_2 = self.env['membership.partner.committee'].create({
            'partner_id': self.partner_2.id,
            'committee_id': self.committee_1.id,
            'committee_tmp_id': self.commitee_tmp_2.id,
        })

    def test_get_committee(self):
        url = url_join(self.base_url(), '/snippet/member_committee/{}'.format(self.committee_1.id))
        res = self.opener.get(url, json={})
        self.assertEqual(res.status_code, 200)
        data_response = json.loads(res.text)
        print(data_response)
        self.assertTrue('result' in data_response)
        # self.assertTrue('level_1' in data_response['result'])
        # self.assertTrue('level_2' in data_response['result'])
        # self.assertTrue('level_3' in data_response['result'])

    def test_create_membership_resume_type(self):
        committee = self.partner_member_committee_1
        partner = self.partner_1
        
        self.assertEqual(committee.partner_id.id, partner.id)

        line_type = self.env.ref('membership_profile.resume_type_join_committee', raise_if_not_found=True)
        self.assertTrue(partner.membership_resume_ids.filtered(lambda e: e.line_type_id.id == line_type.id).exists())
        print('PASS')