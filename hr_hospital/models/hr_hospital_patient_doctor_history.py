from odoo import models, fields, api


class HRHospitalPatientDoctorHistory(models.Model):
    _name = 'hr.hospital.patient.doctor.history'
    _description = 'Patient Doctor History'
    _order = 'appointment_date desc'

    patient_id = fields.Many2one(
        'hr.hospital.patient',
        string='Patient',
        ondelete='cascade')
    doctor_id = fields.Many2one(
        'hr.hospital.doctor',
        string='Doctor',
        required=True)
    appointment_date = fields.Datetime(
        string='Date of Appointment',
        default=fields.Datetime.now)

    change_date = fields.Date(
        string='Change Date'
    )

    change_reason = fields.Text(
        string='Reason for Change'
    )

    active = fields.Boolean(
        string='Active',
        default=True
    )

    # 6.4. Перевизначення create: деактивація попередніх записів
    # create для моделі "Історія персональних лікарів" -
    # встановлювати попередній запис як неактивний
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            # Шукаємо старі записи ПЕРЕД створенням нового
            old_records = self.search([
                ('patient_id', '=', vals.get('patient_id')),
                ('active', '=', True)
            ])
            old_records.write({
                'active': False,
                'change_date': fields.Date.today()
            })
        return super().create(vals_list)
