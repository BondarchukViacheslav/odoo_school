import logging
import re
from datetime import date
from odoo import models, fields, api
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)


class HRHospitalAbstractPerson(models.AbstractModel):
    _name = 'hr.hospital.abstract.person'
    _description = 'Abstract Person'
    _inherit = ['image.mixin']

    first_name = fields.Char(string='First Name', required=True)
    last_name = fields.Char(string='Last Name', required=True)
    middle_name = fields.Char(string='Middle Name')

    full_name = fields.Char(
        string='Full Name',
        compute='_compute_full_name',
        store=True
    )

    phone = fields.Char(string='Phone')
    email = fields.Char(string='Email')
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other')
    ], string='Gender', default='other')
    birth_date = fields.Date(string='Date of Birth')

    age = fields.Integer(
        string='Age',
        compute='_compute_age',
        readonly=True
    )

    country_id = fields.Many2one(
        'res.country',
        string='Country of Citizenship')

    lang_id = fields.Many2one(
        'res.lang',
        string='Language')

    @api.constrains('phone')
    def _check_phone(self):
        pattern = r"^\+?[0-9\s\-]+$"
        for rec in self:
            if rec.phone and not re.match(pattern, rec.phone):
                raise ValidationError(
                    "Invalid phone format! Use numbers, spaces, '-' or '+'.")

    @api.constrains('email')
    def _check_email(self):
        for rec in self:
            if rec.email and not re.match(r"[^@]+@[^@]+\.[^@]+", rec.email):
                raise ValidationError("Invalid email format!")

    # 6.2. Обчислювальні поля з залежностями (@api.depends)
    # Повне ім'я від окремих полів ПІБ
    @api.depends('first_name', 'last_name', 'middle_name')
    def _compute_full_name(self):
        for rec in self:
            full_name = [rec.last_name, rec.first_name, rec.middle_name]
            rec.full_name = " ".join(filter(None, full_name))

    # 6.2. Обчислювальні поля з залежностями (@api.depends)
    # Вік особи від дати народження
    @api.depends('birth_date')
    def _compute_age(self):
        today = date.today()
        for rec in self:
            if rec.birth_date:

                rec.age = today.year - rec.birth_date.year - (
                        (today.month, today.day) < (rec.birth_date.month, rec.birth_date.day)
                )
            else:
                rec.age = 0
