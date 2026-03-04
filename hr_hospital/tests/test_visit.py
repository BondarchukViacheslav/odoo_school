from datetime import timedelta
from odoo.exceptions import UserError, ValidationError
from odoo import fields
from .common import TestHRHospitalCommon


class TestHRHospitalVisit(TestHRHospitalCommon):

    def test_01_prevent_delete_with_diagnosis(self):
        # Тест обмеження: заборона видалення візиту з діагнозами
        # Test constraint: cannot delete a visit that has diagnoses attached
        visit = self.env['hr.hospital.visit'].create({
            'doctor_id': self.doctor.id,
            'patient_id': self.patient.id,
            'planned_date': fields.Datetime.now(),
        })

        # Створюємо фіктивний діагноз для візиту
        # Adding a diagnosis to trigger the restriction
        disease = self.env['hr.hospital.disease'].create({'name': 'Lupus'})
        self.env['hr.hospital.diagnosis'].create({
            'visit_id': visit.id,
            'patient_id': self.patient.id,
            'doctor_id': self.doctor.id,
            'disease_id': disease.id,
        })

        # Очікується помилка користувача під час спроби видалення
        # Expecting UserError when trying to delete
        with self.assertRaises(UserError, msg="System should prevent deletion of visits with linked diagnoses"):
            visit.unlink()

    def test_02_visit_schedule_constraint(self):
        # Перевірка @api.constrains: заборона запису до того ж лікаря в той самий день
        # Business Rule: Patient cannot have multiple appointments with the same doctor on the same day
        appointment_time = fields.Datetime.now()

        self.env['hr.hospital.visit'].create({
            'doctor_id': self.doctor.id,
            'patient_id': self.patient.id,
            'planned_date': appointment_time,
        })

        # Expecting ValidationError for duplicate time slot
        with self.assertRaises(ValidationError, msg="Duplicate visit for same doctor/patient/day should be blocked"):
            self.env['hr.hospital.visit'].create({
                'doctor_id': self.doctor.id,
                'patient_id': self.patient.id,
                'planned_date': appointment_time + timedelta(minutes=30),
            })
