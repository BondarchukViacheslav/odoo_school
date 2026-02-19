from odoo import models, fields


class HRHospitalDoctorSpecialty(models.Model):
    _name = 'hr.hospital.doctor.specialty'
    _description = 'Doctor Specialty'
    _order = 'name'

    # Поля:
    #     Назва (req), Код (size=10, req), Опис, Активна (bool).
    #     Зв'язки: Лікарі (One2many).

    name = fields.Char(
        string='Specialty Name',
        required=True,
        translate=True
    )

    code = fields.Char(
        string='Specialty Code',
        size=10,
        required=True
    )

    description = fields.Text(string='Description')

    active = fields.Boolean(
        string='Active',
        default=True,
        help="If unchecked, it will allow you to hide the specialty "
             "without removing it."
    )


doctor_ids = fields.One2many(
    comodel_name='hr.hospital.doctor',
    inverse_name='specialty_id',
    string='Doctors'
)
