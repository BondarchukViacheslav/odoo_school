import logging

from odoo import models, fields

_logger = logging.getLogger(__name__)


class HRHospitalDoctor(models.Model):
    _name = 'hr.hospital.doctor'
    _description = 'Doctor'

    res_partner_id = fields.Many2one(
        'res.partner',
        string='Contact',
        required=True,
        ondelete='cascade')
    name = fields.Char(
        related='res_partner_id.name',
        readonly=False)

    #    name = fields.Char(string='Full Name', required=True)
    specialty = fields.Char(
        string='Specialty',
        required=True)
