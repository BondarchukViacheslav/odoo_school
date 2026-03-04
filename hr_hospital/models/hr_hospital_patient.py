from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class HRHospitalPatient(models.Model):
    """
    Represents a patient record in the hospital system.
    Includes personal health data (blood group, allergies), insurance information,
    and maintains a link to a personal doctor.
    """
    _name = 'hr.hospital.patient'
    _description = 'Patient'
    _rec_name = 'full_name'
    _inherit = ['hr.hospital.abstract.person']

    user_id = fields.Many2one('res.users', string='Related User')

    personal_doctor_id = fields.Many2one(
        comodel_name='hr.hospital.doctor',
        string='Personal Doctor',
        help='Current personal doctor'
    )

    passport_data = fields.Char(string='Passport Details', size=10)

    contact_person_id = fields.Many2one(
        comodel_name='hr.hospital.contact.person',
        string='Emergency contact person'
    )

    blood_group = fields.Selection([
        ('o_plus', 'O(I) Rh+'), ('o_minus', 'O(I) Rh-'),
        ('a_plus', 'A(II) Rh+'), ('a_minus', 'A(II) Rh-'),
        ('b_plus', 'B(III) Rh+'), ('b_minus', 'B(III) Rh-'),
        ('ab_plus', 'AB(IV) Rh+'), ('ab_minus', 'AB(IV) Rh-'),
    ], string='Blood Group & Rh')

    allergies = fields.Text(string='Allergies Info')

    insurance_company_id = fields.Many2one(
        comodel_name='res.partner',
        string='Insurance company',
        domain=[('is_company', '=', True)]
    )
    insurance_policy_number = fields.Char(string='Insurance Policy Number')

    doctor_history_ids = fields.One2many(
        comodel_name='hr.hospital.patient.doctor.history',
        inverse_name='patient_id',
        string='Doctor History',
        context={'active_test': False}  # ЦЕ КРИТИЧНО ВАЖЛИВО
    )

    diagnosis_ids = fields.One2many(
        comodel_name='hr.hospital.diagnosis',
        inverse_name='patient_id',
        string='Diagnosis History',
        readonly=True
    )

    # 5.2. Python обмеження (@api.constrains)
    # Вік пацієнта має бути більше 0
    @api.constrains('birth_date')
    def _check_birth_date(self):
        """
        Constraint to ensure the patient's birth date is in the past.
        Prevents creating records for patients with age 0 or less.
        """
        today = fields.Date.today()
        for rec in self:
            if rec.birth_date and rec.birth_date >= today:
                raise ValidationError(
                    _("Birth date must be in the past! "
                      "Patient age must be greater than 0."))

    # 6.1. Автоматичні дії
    # При зміні персонального лікаря пацієнта -
    # автоматично створювати запис в історії
    # 6.4. Перевизначення стандартних методів
    # write для моделі "Пацієнт" -
    # при зміні персонального лікаря створювати історію
    def write(self, vals):
        """
        Extended write method to track personal doctor changes.
        Automatically creates an entry in 'hr.hospital.patient.doctor.history'
        whenever 'personal_doctor_id' is updated.
        """
        res = super(HRHospitalPatient, self).write(vals)
        if 'personal_doctor_id' in vals:
            for rec in self:
                self.env['hr.hospital.patient.doctor.history'].create({
                    'patient_id': rec.id,
                    'doctor_id': vals['personal_doctor_id'],
                    'appointment_date': fields.Datetime.now(),
                })
        return res

    # 6.3. Методи onchange (@api.onchange)
    # При зміні країни громадянства пацієнта -
    # пропонувати відповідну мову спілкування
    @api.onchange('country_id')
    def _onchange_country_id(self):
        """
        When changing the patient's country of citizenship -
        sets the appropriate language of communication
        """
        if self.country_id:
            lang = self.env['res.lang'].search([
                ('code', 'ilike', self.country_id.code)
            ], limit=1)

            if lang:
                self.lang_id = lang

    # 8.2. Динамічні домени через методи
    # Пацієнти за мовою спілкування та країною громадянства
    @api.model
    def _get_doctors_by_country_domain(self, country_id, lang_id):
        """
        Generate a dynamic domain to filter doctors based on their
        location and spoken language.

        :param country_id: ID of the res.country record
        :param lang_id: ID of the res.lang record
        :return: A list containing Odoo domain tuples
        """
        domain = []

        if country_id:
            domain.append(('country_id', '=', country_id))

        if lang_id:
            domain.append(('lang_id', '=', lang_id))

        return domain

    # Метод для виклику Smart-button
    def action_view_visits(self):
        """
        Action for the Smart-button to display the history of visits
        for the current patient.

        :return: Dictionary containing the action to open hr.hospital.visit
        views (list, form, calendar) filtered by patient.
        """
        self.ensure_one()
        return {
            'name': 'Visits History',
            'type': 'ir.actions.act_window',
            'res_model': 'hr.hospital.visit',
            'view_mode': 'list,form,calendar',
            'domain': [('patient_id', '=', self.id)],
            'context': {'default_patient_id': self.id},
        }

    def action_create_quick_visit(self):
        """
        Launch a form view to quickly create a new appointment.
        Automatically pre-fills the patient and their personal doctor.

        :return: Action dictionary for opening a new visit form.
        """
        self.ensure_one()
        return {
            'name': 'New Appointment',
            'type': 'ir.actions.act_window',
            'res_model': 'hr.hospital.visit',
            'view_mode': 'form',
            'target': 'current',
            'context': {
                'default_patient_id': self.id,
                'default_doctor_id': self.personal_doctor_id.id,
            },
        }
