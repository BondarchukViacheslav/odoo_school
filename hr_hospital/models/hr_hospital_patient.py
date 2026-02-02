import logging

from odoo import models, fields

_logger = logging.getLogger(__name__)


class HRHospitalPatient(models.Model):
    _name = 'hr.hospital.patient'
    _description = 'Patient'

    res_partner_id = fields.Many2one('res.partner',
                                 string='Contact',
                                 required=True,
                                 ondelete='cascade')

    name = fields.Char(related='res_partner_id.name',
                       readonly=False)
#    name = fields.Char(string='Full Name', required=True)
#    doctor_id = fields.Many2one('hr.hospital.doctor',
#    string='Personal Doctor', required=True)
