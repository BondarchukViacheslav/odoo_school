import logging
# import re
# from datetime import date
from odoo import models, fields, api, _

# from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)


class HRHospitalAbstractPerson(models.AbstractModel):
    _name = 'hr_hospital.abstract.person'
    _description = 'Abstract Person'
    _inherit = ['image.mixin']

    # first_name = fields.Char(string='First Name', required=True)
    # last_name = fields.Char(string='Last Name', required=True)
    # middle_name = fields.Char(string='Middle Name')
    #
    # # Обчислювальне поле для повного імені
    # complete_name = fields.Char(
    #     string='Full Name',
    #     compute='_compute_complete_name',
    #     store=True
    # )
    #
    # phone = fields.Char(string='Phone')
    # email = fields.Char(string='Email')
    #
    # gender = fields.Selection([
    #     ('male', 'Male'),
    #     ('female', 'Female'),
    #     ('other', 'Other')
    # ], string='Gender', default='other')
    #
    # birth_date = fields.Date(string='Date of Birth')
    #
    # # Обчислювальне поле для віку
    # age = fields.Integer(
    #     string='Age',
    #     compute='_compute_age',
    #     readonly=True
    # )
    #
    # country_id = fields.Many2one('res.country', string='Country of Citizenship')
    # lang_id = fields.Many2one('res.lang', string='Language')
    #
    # @api.depends('first_name', 'last_name', 'middle_name')
    # def _compute_complete_name(self):
    #     for rec in self:
    #         names = [rec.last_name, rec.first_name, rec.middle_name]
    #         rec.complete_name = " ".join(filter(None, names))
    #
    # @api.depends('birth_date')
    # def _compute_age(self):
    #     today = date.today()
    #     for rec in self:
    #         if rec.birth_date:
    #             # Обчислюємо різницю років
    #             rec.age = today.year - rec.birth_date.year - (
    #                     (today.month, today.day) < (rec.birth_date.month, rec.birth_date.day)
    #             )
    #         else:
    #             rec.age = 0
    #
    # @api.constrains('email')
    # def _check_email(self):
    #     for rec in self:
    #         if rec.email and not re.match(r"[^@]+@[^@]+\.[^@]+", rec.email):
    #             raise ValidationError(_("Invalid email format!"))
    #
    # @api.constrains('phone')
    # def _check_phone(self):
    #     # Проста валідація: тільки цифри, +, - та пробіли
    #     pattern = r"^\+?[0-9\s\-]+$"
    #     for rec in self:
    #         if rec.phone and not re.match(pattern, rec.phone):
    #             raise ValidationError(_("Invalid phone format! Use numbers, spaces, '-' or '+'."))
