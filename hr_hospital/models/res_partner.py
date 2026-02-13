import logging

from odoo import models  # , fields

_logger = logging.getLogger(__name__)


class ResPartner(models.Model):
    _inherit = 'res.partner'

    # is_doctor = fields.Boolean(
    #     string='Has Medical Degree',
    #     help='Check this box if the partner has a medical diploma/degree.',
    #     default=False
    # )
