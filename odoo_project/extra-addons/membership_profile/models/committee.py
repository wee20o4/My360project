import logging
import datetime

from odoo.exceptions import UserError, ValidationError
from odoo import api, models, fields, _

_logger = logging.getLogger(__name__)


class Committee(models.Model):
    _name = 'membership.committee'
    _description = 'Membership Committees'
    
    name = fields.Char(_('Name'), required=True)
    date_start = fields.Date('Start Date', required=True)
    date_end = fields.Date('End Date', required=True)
    
    
class CommitteeTemplate(models.Model):
    _name = 'membership.committee.tmp'
    _description = 'Membership Committee Template'

    name = fields.Char(_('Name'), required=True)
    description = fields.Char(string=_('Description'))
    committee_ids = fields.Many2many('membership.committee', 'membership_commmittee_template_rel',
                                     'committee_tmp_id', 'committee_id', string='Committees')
    # TEMPLATE
    tmp_type_id = fields.Many2one('membership.committee.tmp.type', ondelete='restrict', required=True)
    raise_in_template = fields.Boolean(default=False)

    
class CommitteeTemplateType(models.Model):
    _name = 'membership.committee.tmp.type'
    _description = 'Committee Template Type'
    _order = "sequence"

    name = fields.Char(required=True)
    specific_type = fields.Selection(
                    string=_('Specific'),
                    selection=[('manager', 'Manager'),
                               ('member', 'Member'),
                               ('delegate', 'Delegation')],
                    default='member', required=True)
    visible = fields.Boolean(default=True)
    sequence = fields.Integer('Sequence', default=10)

    _sql_constraints = [
        ('committee_tmp_type', 'unique (name, specific_type)',
         'The combination template name/specific_type already exists!'),
    ]

                                     
class PartnerMembershipCommittee(models.Model):
    _name = 'membership.partner.committee'
    _description = 'Membership Partner Committee'

    partner_id = fields.Many2one('res.partner', 'Partner', copy=False, required=True, ondelete='cascade')
    committee_id = fields.Many2one('membership.committee', 'Committee', copy=False, required=True, ondelete='cascade')
    committee_tmp_id = fields.Many2one('membership.committee.tmp', 'Committee Template', copy=False, required=True, ondelete='cascade')

    description = fields.Char(_('Description'))
    
    _sql_constraints = [
        ('partner_committee_committee_tmp', 'unique (partner_id, committee_id, committee_tmp_id)',
         'The combination partner/committee/committe template already exists!'),
    ]

    @api.model_create_multi
    def create(self, vals_list):
        res = super(PartnerMembershipCommittee, self).create(vals_list) 

        resume_lines_values = []
        for partner_committee in res:
            line_type = self.env.ref('membership_profile.resume_type_join_committee', raise_if_not_found=False)
            resume_lines_values.append({
                'partner_id': partner_committee.partner_id.id,
                'name': "{} - {}".format(partner_committee.committee_tmp_id.name, partner_committee.committee_id.name) or '',
                'date_start': partner_committee.committee_id.date_start,
                'date_end': partner_committee.committee_id.date_end,
                'description': partner_committee.description or '',
                'line_type_id': line_type and line_type.id,
            })
        self.env['membership.resume.line'].create(resume_lines_values)
        return res