from odoo import api, fields, models
from odoo.exceptions import ValidationError


class HRHospitalMassReassignDoctorWizard(models.TransientModel):
    _name = 'hr.hospital.mass.reassign.doctor.wizard'
    _description = 'Mass Reassign Doctor Wizard'

    old_doctor_id = fields.Many2one(
        comodel_name='hr.hospital.doctor',
        string='Old Doctor'
    )
    new_doctor_id = fields.Many2one(
        comodel_name='hr.hospital.doctor',
        string='New Doctor',
        required=True
    )

    patient_ids = fields.Many2many(
        comodel_name='hr.hospital.patient',
        string='Patients',
        domain="[('personal_doctor_id', '=', old_doctor_id)]"
    )

    change_date = fields.Date(
        string='Change Date',
        default=fields.Date.context_today,
        required=True
    )
    reason = fields.Text(
        string='Reason for Change',
        required=True
    )

    @api.onchange('old_doctor_id')
    def _onchange_old_doctor_id(self):
        if self.old_doctor_id:
            patients = self.env['hr.hospital.patient'].search([
                ('personal_doctor_id', '=', self.old_doctor_id.id)
            ])
            self.patient_ids = [(6, 0, patients.ids)]
        else:
            self.patient_ids = [(5, 0, 0)]

    def action_reassign_doctor(self):
        self.ensure_one()
        if not self.patient_ids:
            raise ValidationError("Please select at least one patient.")

        if self.old_doctor_id == self.new_doctor_id:
            raise ValidationError("Old and New doctors must be different.")

        self.patient_ids.write({
            'personal_doctor_id': self.new_doctor_id.id
        })

        return {
            'type': 'ir.actions.act_window_close',
            'tag': 'display_notification',
            'params': {
                'title': 'Success',
                'message': 'Patients have been successfully reassigned.',
                'sticky': False,
            }
        }
