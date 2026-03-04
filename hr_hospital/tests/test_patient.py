from datetime import date, timedelta

from odoo.exceptions import ValidationError

from .common import TestHRHospitalCommon


class TestHRHospitalPatient(TestHRHospitalCommon):

    def test_01_birth_date_constraint(self):
        # Тест бізнес-правила: дата народження має бути в минулому
        # Test business rule: birth date must be in the past
        future_date = date.today() + timedelta(days=1)

        # Testing validation constraint
        with self.assertRaises(ValidationError, msg="Validation error should be raised for future birth date"):
            self.patient.write({'birth_date': future_date})

    def test_02_doctor_history_automatic_creation(self):
        # Тест бізнес-процесу: автоматичне створення запису в історії при зміні лікаря
        # Test business process: automatic history record creation on doctor change
        new_doctor = self.env['hr.hospital.doctor'].create({
            'first_name': 'New',
            'last_name': 'Doctor',
            'full_name': 'New Doctor',
            'license_number': 'NEW-LIC-777',
        })

        # Виклик методу write моделі пацієнта
        # Trigger the write method override
        self.patient.write({'personal_doctor_id': new_doctor.id})

        # Перевірка результату в пов'язаній моделі історії
        # Verify a record was created in hr.hospital.patient.doctor.history
        history = self.env['hr.hospital.patient.doctor.history'].search([
            ('patient_id', '=', self.patient.id),
            ('doctor_id', '=', new_doctor.id)
        ])
        self.assertTrue(history, "The system must automatically create a history record upon doctor reassignment")
