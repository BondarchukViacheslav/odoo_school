from odoo import models, fields, api
from odoo.exceptions import ValidationError


class HRHospitalDiagnosis(models.Model):
    _name = 'hr.hospital.diagnosis'
    _description = 'Medical Diagnosis'

    visit_id = fields.Many2one(
        comodel_name='hr.hospital.visit',
        string='Visit',
        ondelete='cascade',
        required=True
    )

    disease_id = fields.Many2one(
        comodel_name='hr.hospital.disease',
        string='Disease',
        required=True,
        domain=[
            ('is_contagious', '=', True),
            ('severity', 'in', ['high', 'critical'])
        ],
    )

    description = fields.Text(string='Diagnosis Description')
    treatment = fields.Html(string='Prescribed Treatment')

    is_approved = fields.Boolean(string='Approved', default=False)

    approved_doctor_id = fields.Many2one(
        comodel_name='hr.hospital.doctor',
        string='Approved By',
        readonly=True
    )

    approval_date = fields.Datetime(
        string='Approval Date',
        readonly=True
    )

    severity = fields.Selection([
        ('mild', 'Mild'),
        ('moderate', 'Moderate'),
        ('severe', 'Severe'),
        ('critical', 'Critical')
    ], string='Severity', default='mild')

    doctor_id = fields.Many2one(
        related='visit_id.doctor_id',
        store=True,
        string='Doctor'
    )
    patient_id = fields.Many2one(
        related='visit_id.patient_id',
        store=True,
        string='Patient'
    )

    country_id = fields.Many2one(
        related='visit_id.patient_id.country_id',
        store=True,
        string='Country'
    )
    planned_date = fields.Datetime(
        related='visit_id.planned_date',
        store=True,
        string='Planned Date & Time'
    )

    disease_type_id = fields.Many2one(
        related='disease_id.parent_id',
        string='Disease Type',
        store=True,
        readonly=True
    )

    # 5.2. Python обмеження (@api.constrains)
    # Дата проведення дослідження не може бути раніше дати призначення
    @api.constrains('approval_date', 'visit_id')
    def _check_approval_date(self):
        for rec in self:
            if rec.approval_date and rec.visit_id.planned_date:
                if rec.approval_date < rec.visit_id.planned_date:
                    raise ValidationError(
                        "The approval date cannot be earlier "
                        "than the visit date!"
                    )

    # 6.1. Автоматичні дії
    # При затвердженні діагнозу ментором -
    # оновлювати поле "Затверджено" та дати
    def write(self, vals):
        if vals.get('is_approved'):
            current_user = self.env.user
            doctor = self.env['hr.hospital.doctor'].search([
                ('user_id', '=', current_user.id)
            ], limit=1)

            if doctor:
                vals.update({
                    'approved_doctor_id': doctor.id,
                    'approval_date': fields.Datetime.now(),
                })

        elif 'is_approved' in vals and not vals.get('is_approved'):
            vals.update({
                'approved_doctor_id': False,
                'approval_date': False,
            })

        return super(HRHospitalDiagnosis, self).write(vals)
