from datetime import date, timedelta
from odoo.tests.common import TransactionCase


class TestHRHospitalCommon(TransactionCase):

    def setUp(self):
        super(TestHRHospitalCommon, self).setUp()

        self.specialty = self.env['hr.hospital.doctor.specialty'].create({
            'name': 'Cardiologist',
            'code': 'CARD-01',
        })

        self.doctor = self.env['hr.hospital.doctor'].create({
            'first_name': 'Test',
            'last_name': 'Doctor',
            'full_name': 'Test Doctor',
            'license_number': 'UNIQUE-LIC-123',
            'specialty_id': self.specialty.id,
            'license_issue_date': date.today() - timedelta(days=365 * 10 + 5),
            'gender': 'male',
        })

        self.patient = self.env['hr.hospital.patient'].create({
            'first_name': 'Test',
            'last_name': 'Patient',
            'full_name': 'Test Patient',
            'birth_date': date.today() - timedelta(days=365 * 25),
        })
