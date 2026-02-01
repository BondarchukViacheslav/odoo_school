from odoo import models, fields

class HRHospitalPatient(models.Model):
    _name = 'hr.hospital.patient'
    _description = 'Patient'

    partner_id = fields.Many2one('res.partner', string='Contact', required=True, ondelete='cascade')
    name = fields.Char(related='partner_id.name', readonly=False)
#    name = fields.Char(string='Full Name', required=True)
#    doctor_id = fields.Many2one('hr.hospital.doctor', string='Personal Doctor', required=True)
