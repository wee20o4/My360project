from odoo import api, SUPERUSER_ID # type: ignore

def clear_asset_cache(cr, registry):
    env = api.Environment(cr, SUPERUSER_ID, {})
    # Chỉ xóa các bản ghi ir.attachment liên quan đến module membership_profile_search
    attachments = env['ir.attachment'].search([
        ('url', 'like', '/web/assets/%'),
        ('res_model', '=', False),
        ('res_id', '=', False),
        ('name', 'like', 'membership_profile_search%'),  # Giới hạn trong tài nguyên của module
    ])
    if attachments:
        attachments.unlink()

    # Xóa các view không còn được sử dụng liên quan đến membership_profile_search
    views = env['ir.ui.view'].search([
        ('key', 'like', 'membership_profile_search.%'),
    ])
    if views:
        views.unlink()