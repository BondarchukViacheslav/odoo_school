import logging

from odoo import fields, models

_logger = logging.getLogger(__name__)


class ResPartner(models.Model):
    _inherit = 'res.partner'

#    specialty = fields.Text(string="Specialty")

#    has_medical_degree = fields.Boolean(
#        string='Has Medical Degree',
#        help='Check this box if the partner has a medical diploma/degree.',
#        default=False
#    )
