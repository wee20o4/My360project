import logging

from datetime import timedelta, date
from odoo import api, models, _


_logger = logging.getLogger(__name__)


class MembershipLine(models.Model):
    _inherit = 'membership.membership_line'

    @api.model_create_multi
    def create(self, vals_list):
        for value in vals_list:
            product_id = value['membership_id']
            membership_product = self.env['product.product'].browse(product_id)
            if membership_product.membership_product_tmp_type == 'recurring':
                invoice_line = self.env['account.move.line'].browse(value['account_invoice_line'])
                invoice = invoice_line.move_id
                if invoice.state not in ['draft', 'cancel']:
                    invoice_date = invoice.invoice_date
                    if not invoice_date:
                        continue
                    delta_periodict = membership_product.periodic_id._get_delta_periodict()
                    date_from = invoice_date
                    date_to = date_from + timedelta(days=delta_periodict)
                    value.update({'date_from': date_from, 'date_to': date_to})
        return super().create(vals_list)

    def update_date_membership_recurring(self):
        self.ensure_one()
        line = self.account_invoice_line
        invoice = line.move_id
        if (line.product_id.membership_product_tmp_type != 'recurring'
            or not invoice.invoice_date
            or invoice.state in ['draft', 'cancel']):
            return
        if line.product_id.periodic_id: 
            delta_periodict = line.product_id.periodic_id._get_delta_periodict()
            date_from = invoice.invoice_date
            date_to = date_from + delta_periodict
            current_time = date.today()
            if date_from <= current_time <= date_to:
                self.partner.write({'is_published': True})
            self.write({'date_from': date_from, 'date_to': date_to})
        

class AccountMove(models.Model):
    _inherit = 'account.move'
    
    def action_post(self):
        # OVERRIDE
        res = super(AccountMove, self).action_post()
        if self.move_type == 'out_invoice':
            lines = self.line_ids.filtered(lambda line: line.product_id.membership)
            existing_memberships = self.env['membership.membership_line'].search([('account_invoice_line', 'in', lines.ids)])

            resume_lines_values = []
            for membership in existing_memberships:
                membership.update_date_membership_recurring()
                line_type = self.env.ref('membership_profile.resume_type_join_membership', raise_if_not_found=True)
                description = _('%s become a membership') % (membership.partner.name)
                if len( membership.partner.membership_resume_ids) > 0:
                    line_type = self.env.ref('membership_profile.resume_type_extend_membership', raise_if_not_found=True)
                    description = _('%s extended membership') % (membership.partner.name)
                resume_lines_values.append({
                    'partner_id': membership.partner.id,
                    'name': membership.account_invoice_line.product_id.name or '',
                    'date_start': membership.date_from,
                    'date_end': membership.date_to,
                    'description': description or '',
                    'line_type_id': line_type and line_type.id,
                })

            if len(resume_lines_values) > 0:
                self.env['membership.resume.line'].create(resume_lines_values)
        
        return res

