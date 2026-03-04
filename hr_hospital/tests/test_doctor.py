from .common import TestHRHospitalCommon


class TestHRHospitalDoctor(TestHRHospitalCommon):

    def test_01_experience_computation(self):
        # Перевірка автоматичного розрахунку досвіду за датою ліцензії
        # Test computed field: verify experience calculation based on license date
        self.assertEqual(self.doctor.experience, 10, "Doctor experience was calculated incorrectly")

    def test_02_display_name_compute(self):
        # Перевірка формату відображення імені: 'Ім'я (Спеціальність)'
        # Test computed field: verify display_name format 'Name (Specialty)'
        expected_name = f"{self.doctor.full_name} ({self.specialty.name})"
        self.assertEqual(self.doctor.display_name, expected_name, "Display name format is incorrect")
