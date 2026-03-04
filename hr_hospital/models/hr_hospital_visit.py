from odoo import models, fields, api, _
from odoo.exceptions import UserError
from odoo.exceptions import ValidationError


class HRHospitalVisit(models.Model):
    """
    Manages clinical appointments between patients and doctors.
    Tracks visit states (Planned, Completed, Cancelled) and stores
    medical diagnoses and recommendations.
    """
    _name = 'hr.hospital.visit'
    _description = 'Patient Visit'
    _order = 'planned_date desc'

    name = fields.Char(
        string='Visit Reference',
        readonly=True,
        copy=False,
        default='New')

    state = fields.Selection([
        ('planned', 'Planned'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('no_show', 'No Show')
    ],
        string='Status',
        default='planned',
        required=True
        # ,
        # tracking=True
    )

    planned_date = fields.Datetime(
        string='Planned Date & Time',
        required=True
    )

    actual_date = fields.Datetime(
        string='Actual Date & Time')

    doctor_id = fields.Many2one(
        comodel_name='hr.hospital.doctor',
        string='Doctor',
        required=True,
        domain="[('license_number', '!=', False)]"
    )

    patient_id = fields.Many2one(
        comodel_name='hr.hospital.patient',
        string='Patient',
        required=True
        # ,
        # tracking=True
    )

    visit_type = fields.Selection([
        ('primary', 'Primary'),
        ('follow_up', 'Follow-up'),
        ('preventive', 'Preventive'),
        ('emergency', 'Emergency')
    ], string='Visit Type', default='primary')

    diagnosis_ids = fields.One2many(
        comodel_name='hr.hospital.diagnosis',
        inverse_name='visit_id',
        string='Diagnoses'
    )

    recommendations = fields.Html(string='Recommendations')

    currency_id = fields.Many2one(
        'res.currency',
        string='Currency',
        default=lambda self: self.env.company.currency_id
    )

    amount = fields.Monetary(
        string='Visit Cost',
        currency_field='currency_id'
    )

    diagnosis_count = fields.Integer(
        string='Diagnosis Count',
        compute='_compute_diagnosis_count',
        store=True
    )

    comment = fields.Char()

    # Для завдання 8.2, щоб не писати окремий візард
    specialty_id = fields.Many2one(
        comodel_name='hr.hospital.doctor.specialty',
        string='Specialty'
    )

    # 5.2. Python обмеження (@api.constrains)
    # Заборона запису одного пацієнта до одного лікаря
    # більше одного разу на день
    @api.constrains('patient_id', 'doctor_id', 'planned_date')
    def _check_duplicate_visit(self):
        """
        Prevents scheduling multiple visits for the same patient
        with the same doctor on the same day.
        """
        for rec in self:
            if not rec.planned_date or not rec.patient_id or not rec.doctor_id:
                continue

            start_of_day = rec.planned_date.replace(
                hour=0, minute=0, second=0)
            end_of_day = rec.planned_date.replace(
                hour=23, minute=59, second=59)

            domain = [
                ('id', '!=', rec.id),
                ('patient_id', '=', rec.patient_id.id),
                ('doctor_id', '=', rec.doctor_id.id),
                ('planned_date', '>=', start_of_day),
                ('planned_date', '<=', end_of_day),
            ]

            if self.search_count(domain) > 0:
                raise ValidationError(
                    _("This patient already has a visit scheduled with "
                      "this doctor today (%s)!") % rec.planned_date.date())

    # 5.3.Обмеження на видалення та архівування
    # Заборона видалення візитів з діагнозами
    def unlink(self):
        """
        Safety override to prevent deletion of visit records
        that already have associated diagnoses.
        """
        for rec in self:
            if rec.diagnosis_ids:
                raise UserError(
                    _("You cannot delete the visit (ID: %s) "
                      "because it already has diagnoses attached to it.")
                    % rec.name)
        return super().unlink()

    # 5.3.Обмеження на видалення та архівування
    # Заборона зміни лікаря/дати/часу візиту, що вже відбувся
    def write(self, vals):
        """
        Prevent modification of critical fields in completed visits.
        Checks if the visit is in 'completed' state and restricts
        changes to doctor, patient, and date fields.

        :param vals: dictionary of new values to update
        :raises UserError: if any protected field is being modified
            for a completed visit
        """
        protected_fields = ['doctor_id', 'planned_date', 'patient_id']

        for rec in self:
            if rec.state == 'completed':
                if any(field in vals for field in protected_fields):
                    raise UserError(
                        _("You cannot change the doctor, patient, "
                          "or date on a visit that has already been completed.")
                    )
        return super().write(vals)

    # 6.2. Обчислювальні поля з залежностями (@api.depends)
    # Кількість діагнозів на візиті
    @api.depends('diagnosis_ids')
    def _compute_diagnosis_count(self):
        """
        Calculate the total number of diagnoses linked to this visit.
        Used for displaying the counter in the smart button.
        """
        for rec in self:
            # Рахуємо довжину списку ID діагнозів
            rec.diagnosis_count = len(rec.diagnosis_ids)

    # 6.3. Методи onchange (@api.onchange)
    # При виборі пацієнта - показувати попередження про алергії
    @api.onchange('patient_id')
    def _onchange_patient_id_warning(self):
        """
        Show a warning notification if the selected patient has allergies.

        :return: dict: a warning message to be displayed in the web client
        """
        if self.patient_id and self.patient_id.allergies:
            return {
                'warning': {
                    'title': "Allergy Warning!",
                    'message': _("This patient has the following allergies: %s") % self.patient_id.allergies,
                    'type': 'notification',
                }
            }

    # 6.4.Перевизначення стандартних методів unlink
    # для моделі "Візити" - перевіряти наявність діагнозів
    def unlink(self):
        """
        Prevent deletion of visits that contain medical records.
        Ensures data integrity by checking if diagnosis_ids is not empty.

        :raises UserError: if the visit has at least one diagnosis
        """
        for rec in self:
            if rec.diagnosis_ids:
                raise UserError(
                    _("You cannot delete a visit that has diagnoses!")
                )
        return super(HRHospitalVisit, self).unlink()

    @api.depends('planned_date', 'doctor_id', 'patient_id')
    def _compute_display_name(self):
        """
        Generate a descriptive name for the record used in search and breadcrumbs.
        Format: "DD.MM.YYYY HH:MM | Dr: Name | Pt: Name"
        """
        for rec in self:
            # Перетворюємо Float час у формат HH:MM
            # (якщо використовується float_time)
            dt = rec.planned_date
            date_str = dt.strftime('%d.%m.%Y %H:%M') if dt else "No Date"

            doctor_name = rec.doctor_id.full_name or _("No Doctor")
            patient_name = rec.patient_id.full_name or _("No Patient")

            # Формуємо підпис: "12.02.2026 10:30 |
            # Лікар: Іванов | Пацієнт: Петров"
            rec.display_name = (
                f"{date_str} | "
                f"Dr: {doctor_name} | "
                f"Pt: {patient_name}"
            )

    # 8.2. Динамічні домени через методи
    # Доступні лікарі для запису (за спеціальністю та розкладом)
    @api.onchange('specialty_id', 'planned_date')
    def _onchange_doctor_id_domain(self):
        """
        Update the domain for doctor selection based on specialty and availability.
        Calls the model method to find doctors with matching schedules.

        :return: dict: domain for the doctor_id field
        """
        # 1. Створюємо порожній домен за замовчуванням
        domain = []

        # 2. Перевіряємо умови
        if self.specialty_id and self.planned_date:
            domain = self.env['hr.hospital.doctor'].get_available_doctors_domain(
                self.specialty_id.id,
                self.planned_date,
            )

        # 3. Тепер domain існує завжди, навіть якщо він порожній
        return {'domain': {'doctor_id': domain}}
