# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class MembershipResumeLine(models.Model):
    _name = 'membership.resume.line'
    _description = "Resume line of an membership"
    _order = "line_type_id, date_end desc, date_start desc"

    partner_id = fields.Many2one('res.partner', required=True, ondelete='cascade')
    name = fields.Char(required=True, translate=True)
    date_start = fields.Date(required=True)
    date_end = fields.Date()
    description = fields.Text(string="Description", translate=True)
    line_type_id = fields.Many2one('membership.resume.line.type', string="Type")

    # Used to apply specific template on a line
    display_type = fields.Selection([('classic', 'Classic'), ('course', 'Course'), ('certification', 'Certification')],
                                    string="Display Type", default='classic')

    _sql_constraints = [
        ('date_check', "CHECK ((date_start <= date_end OR date_end = NULL))", "The start date must be anterior to the end date."),
    ]


class MembershipResumeLineType(models.Model):
    _name = 'membership.resume.line.type'
    _description = "Type of a resume line"
    _order = "sequence"

    name = fields.Char(required=True)
    sequence = fields.Integer('Sequence', default=10)
