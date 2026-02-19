from odoo import models  # , fields


class ResPartner(models.Model):
    _inherit = 'res.partner'

    # is_doctor = fields.Boolean(
    #     string='Has Medical Degree',
    #     help='Check this box if the partner has a medical diploma/degree.',
    #     default=False
    # )
