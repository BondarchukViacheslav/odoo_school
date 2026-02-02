import logging

from odoo import models, fields

_logger = logging.getLogger(__name__)


class HRHospitalDooctor(models.Model):
    _name = 'hr.hospital.doctor'
    _description = 'Doctor'

    partner_id = fields.Many2one('res.partner',
                                 string='Contact',
                                 required=True,
                                 ondelete='cascade')
    name = fields.Char(related='partner_id.name',
                       readonly=False)
#    name = fields.Char(string='Full Name', required=True)
    description = fields.Char(string='Specialty',
                              required=True)
