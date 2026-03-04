from datetime import date

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError


class HRHospitalDoctor(models.Model):
    """
    Stores information about medical staff, including their specialty,
    license details, and mentorship status for interns.
    """
    _name = 'hr.hospital.doctor'
    _description = 'Doctor'
    # _rec_name = 'full_name'
    _inherit = ['hr.hospital.abstract.person']

    active = fields.Boolean(string='Active', default=True)

    user_id = fields.Many2one('res.users', string='System User')

    specialty_id = fields.Many2one(
        comodel_name='hr.hospital.doctor.specialty',
        string='Specialty'
    )

    is_intern = fields.Boolean(string='Is Intern', default=False)

    mentor_id = fields.Many2one(
        comodel_name='hr.hospital.doctor',
        string='Mentor',
        domain="[('is_intern', '=', False), ('id', '!=', id)]",
        help="Only non-interns can be mentors"
    )

    license_number = fields.Char(
        string='License Number',
        required=True,
        copy=False
    )
    license_issue_date = fields.Date(string='License Issue Date')

    experience = fields.Integer(
        string='Years of Experience',
        compute='_compute_experience',
        store=True
    )

    rating = fields.Float(
        string='Rating',
        digits=(3, 2),
        help="Rating from 0.00 to 5.00"
    )

    schedule_ids = fields.One2many(
        comodel_name='hr.hospital.doctor.schedule',
        inverse_name='doctor_id',
        string='Work Schedule'
    )
    country_study_id = fields.Many2one(
        'res.country',
        string='Country of Study')

    patient_ids = fields.One2many(
        comodel_name='hr.hospital.patient',
        inverse_name='personal_doctor_id',
        string='Patients',
    )

    intern_ids = fields.One2many(
        comodel_name='hr.hospital.doctor',
        inverse_name='mentor_id',
        string='Interns',
        domain=[('is_intern', '=', True)]
    )

    # Related поля (вони тільки для читання і підтягуються автоматично)
    mentor_photo = fields.Image(
        related='mentor_id.image_1920',
        string="Mentor Photo"
    )
    mentor_full_name = fields.Char(
        related='mentor_id.full_name',
        string="Mentor Name"
    )
    mentor_specialty_id = fields.Many2one(
        related='mentor_id.specialty_id',
        string="Mentor Specialty"
    )
    mentor_license_number = fields.Char(
        related='mentor_id.license_number',
        string="Mentor License"
    )
    mentor_license_issue_date = fields.Date(
        related='mentor_id.license_issue_date',
        string="Mentor Issue Date"
    )

    def action_create_visit_from_kanban(self):
        """
        Open a wizard to create a new visit directly from the doctor's kanban view.
        Sets the current doctor as the default for the new appointment.

        :return: dict: an action to open the visit form view in a target window
        """
        self.ensure_one()
        return {
            'name': _('Quick Appointment'),
            'type': 'ir.actions.act_window',
            'res_model': 'hr.hospital.visit',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_doctor_id': self.id,
            }
        }

    # 5.1. SQL Constraints Унікальність ліцензійного номера лікаря
    _license_number_unique = models.Constraint(
        'UNIQUE(license_number)',
        'The license number must be unique!')

    _check_rating = models.Constraint(
        'CHECK(rating >= 0 AND rating <= 5)',
        'The doctor rating must be between 0 and 5.00!',
    )

    # 5.2. Python обмеження (@api.constrains)
    # Заборона вибору інтерна як лікаря-ментора
    # Перевірка що лікар не може бути ментором самому собі
    @api.constrains('mentor_id', 'is_intern')
    def _check_mentorship(self):
        """
        Validate mentorship logic for interns.
        Ensures a doctor cannot mentor themselves and that an intern
        cannot be assigned as a mentor for another doctor.

        :raises ValidationError: if mentorship rules are violated
        """
        for rec in self:
            if rec.is_intern and rec.mentor_id:
                if rec.mentor_id == rec:
                    raise ValidationError(
                        _("A doctor cannot be a mentor to themselves!"))

                if rec.mentor_id.is_intern:
                    raise ValidationError(
                        _("An intern cannot be a mentor for another intern!"))

    # 5.3.Обмеження на видалення та архівування
    # Заборона архівування лікарів, що мають активні візити
    def write(self, vals):
        """
        Override write to prevent archiving doctors with active appointments.
        If 'active' is set to False, checks for any visits in 'planned' state.

        :param vals: dictionary of fields to update
        :raises UserError: if the doctor has any scheduled (planned) visits
        """
        if 'active' in vals and not vals['active']:
            for doctor in self:
                active_visits = self.env['hr.hospital.visit'].search_count([
                    ('doctor_id', '=', doctor.id),
                    ('state', '=', 'planned')
                ])
                if active_visits > 0:
                    raise UserError(
                        _("Cannot archive doctor %s "
                          "because he has scheduled visits (%s).")
                        % (doctor.display_name, active_visits))
        return super().write(vals)

    # 6.2. Обчислювальні поля з залежностями (@api.depends)
    # Досвід роботи лікаря від дати видачі ліцензії
    @api.depends('license_issue_date')
    def _compute_experience(self):
        """
        Computes the doctor's years of experience based on the date
        their license was issued.
        """
        today = date.today()
        for rec in self:
            if rec.license_issue_date:
                rec.experience = today.year - rec.license_issue_date.year - (
                        (today.month, today.day) < (rec.license_issue_date.month, rec.license_issue_date.day)
                )
            else:
                rec.experience = 0

    # 6.3. Методи onchange (@api.onchange)
    # При виборі лікаря-інтерна - автоматично заповнювати ментора
    @api.onchange('is_intern')
    def _onchange_is_intern(self):
        """
        Automatically handle mentor assignment when the intern status changes.
        If the doctor becomes an intern, it searches for a potential non-intern
        mentor. If the status is unchecked, clears the mentor field.
        """
        if self.is_intern:
            if not self.mentor_id:
                potential_mentor = self.env['hr.hospital.doctor'].search([
                    ('is_intern', '=', False),
                    ('id', '!=', self._origin.id if self._origin else False)
                ], limit=1)
                if potential_mentor:
                    self.mentor_id = potential_mentor
        else:
            self.mentor_id = False

    # 6.4. Перевизначення стандартних методів
    # name_get для моделі "Лікар" -
    # відображати "Ім'я (Спеціальність)" _compute_display_name
    @api.depends('full_name', 'specialty_id.name')
    def _compute_display_name(self):
        """
        Compute a custom display name for the doctor.
        Combines the doctor's full name with their specialty in parentheses.
        Example: "John Doe (Cardiologist)"
        """
        for rec in self:
            # Перевіряємо на наявність даних, щоб не було помилок з None
            name = rec.full_name or _("New Doctor")
            specialty = rec.specialty_id.name or _("No Specialty")
            rec.display_name = f"{name} ({specialty})"

    # 8.2. Динамічні домени через методи
    # Доступні лікарі для запису (за спеціальністю та розкладом)
    # Викликається з моделі візитів
    @api.model
    def get_available_doctors_domain(self, specialty_id, visit_datetime):
        """
        Calculates a dynamic domain for selecting doctors based on
        the required specialty and their work schedule for the
        requested visit time.
        """
        if not specialty_id or not visit_datetime:
            return [('id', '=', 0)]

        # 1. Отримуємо день тижня (Odoo/Python: 0=Пн, 6=Нд)
        dt = fields.Datetime.from_string(visit_datetime)
        day_of_week = str(dt.weekday())

        # 2. Отримуємо час у форматі Float (наприклад, 14:30 -> 14.5)
        visit_hour = dt.hour + dt.minute / 60.0

        # 3. Шукаємо записи в моделі розкладу, які підходять під час візиту
        schedules = self.env['hr.hospital.doctor.schedule'].search([
            ('day_of_week', '=', day_of_week),
            ('start_hour', '<=', visit_hour),
            ('end_hour', '>', visit_hour),
        ])

        # 4. Отримуємо ID лікарів з цих розкладів
        scheduled_doctor_ids = schedules.mapped('doctor_id').ids

        # 5. Фінальний домен: лікар має бути в списку за розкладом
        # ТА мати потрібну спеціальність
        return [
            ('id', 'in', scheduled_doctor_ids),
            ('specialty_id', '=', specialty_id)
        ]

    # 8.2. Динамічні домени через методи
    # Лікарі за країною навчання
    @api.model
    def _get_doctors_by_country_domain(self, country_id):
        """
        Generate a dynamic domain to filter doctors by their country of study.

        :param country_id: ID of the country (res.country) to filter by.
        :return: A list containing a domain tuple or an empty list.
        """
        if not country_id:
            return []
        return [('country_study_id', '=', country_id)]
