from odoo import models, fields, api
from odoo.exceptions import ValidationError


class HRHospitalDiseaseReportWizard(models.TransientModel):
    _name = 'hr.hospital.disease.report.wizard'
    _description = 'Disease Report Wizard'

    start_date = fields.Date(string='Start Date', required=True)
    end_date = fields.Date(string='End Date', required=True)

    doctor_ids = fields.Many2many('hr.hospital.doctor', string='Doctors')
    disease_ids = fields.Many2many('hr.hospital.disease', string='Diseases')
    country_ids = fields.Many2many('res.country', string='Countries')

    report_type = fields.Selection([
        ('detail', 'Detailed'),
        ('summary', 'Summary')
    ], string='Report Type', default='detail', required=True)

    group_by = fields.Selection([
        ('doctor', 'By Doctor'),
        ('disease', 'By Disease'),
        ('month', 'By Month'),
        ('country', 'By Country')
    ], string='Group By', default='disease')

    @api.constrains('start_date', 'end_date')
    def _check_dates(self):
        for rec in self:
            if rec.start_date > rec.end_date:
                raise ValidationError(
                    "Start date cannot be later than end date!"
                )

    def action_get_report(self):
        self.ensure_one()

        domain = [
            ('visit_id.planned_date', '>=', self.start_date),
            ('visit_id.planned_date', '<=', self.end_date)
        ]

        if self.doctor_ids:
            domain.append(('doctor_id', 'in', self.doctor_ids.ids))

        if self.disease_ids:
            domain.append(('disease_id', 'in', self.disease_ids.ids))

        if self.country_ids:
            domain.append(('country_id', 'in', self.country_ids.ids))

        action = self.env.ref(
            'hr_hospital.hr_hospital_diagnosis_action'
        ).read()[0]

        action['domain'] = domain

        group_field = {
            'doctor': 'doctor_id',
            'disease': 'disease_id',
            'month': 'planned_date:month',
            'country': 'country_id'
        }.get(self.group_by)

        action['context'] = {'group_by': group_field}
        return action
