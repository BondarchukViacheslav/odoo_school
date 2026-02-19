from odoo import models, fields


class HRHospitalDiagnosisReportWizard(models.TransientModel):
    _name = 'hr.hospital.diagnosis.report.wizard'
    _description = 'Wizard for Diagnosis Report'

    date_from = fields.Date(string='Date From', required=True)
    date_to = fields.Date(string='Date To', required=True)

    doctor_ids = fields.Many2many('hr.hospital.doctor', string='Doctors')
    disease_ids = fields.Many2many('hr.hospital.disease', string='Diseases')

    def action_open_report(self):
        self.ensure_one()

        domain = [
            ('approval_date', '>=', self.date_from),
            ('approval_date', '<=', self.date_to)
        ]

        if self.doctor_ids:
            domain.append(('doctor_id', 'in', self.doctor_ids.ids))

        if self.disease_ids:
            domain.append(('disease_id', 'in', self.disease_ids.ids))

        return {
            'name': 'Diagnosis Report',
            'type': 'ir.actions.act_window',
            'res_model': 'hr.hospital.diagnosis',
            'view_mode': 'list,pivot,graph,form',
            'domain': domain,
            'context': {'search_default_group_by_disease': 1},
            'target': 'current',
        }
