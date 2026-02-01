from odoo import models, fields


class HRHospitalVisit(models.Model):
    _name = 'hr.hospital.visit'
    _description = 'Patient Visit'
    _order = 'visit_date desc'

    visit_date = fields.Datetime(
        string='Date and Time',
        default=fields.Datetime.now,
        required=True
    )

    patient_id = fields.Many2one(
        comodel_name='hr.hospital.patient',
        string='Patient',
        required=True
    )

    doctor_id = fields.Many2one(
        comodel_name='hr.hospital.doctor',
        string='Doctor',
        required=True
    )

    disease_id = fields.Many2one(
        comodel_name='hr.hospital.disease',
        string='Disease Type'
    )

    diagnosis = fields.Text(
        string='Diagnosis Details'
    )