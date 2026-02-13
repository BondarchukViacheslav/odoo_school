import logging

from odoo import models, fields

_logger = logging.getLogger(__name__)


class HRHospitalDoctorSchedule(models.Model):
    _name = 'hr.hospital.doctor.schedule'
    _description = 'Doctor Schedule'
    _order = 'day_of_week, start_hour'

    doctor_id = fields.Many2one(
        comodel_name='hr.hospital.doctor',
        string='Doctor',
        ondelete='cascade',
        required=True,
        domain=[('specialty_id', '!=', False)],
    )

    day_of_week = fields.Selection([
        ('0', 'Monday'),
        ('1', 'Tuesday'),
        ('2', 'Wednesday'),
        ('3', 'Thursday'),
        ('4', 'Friday'),
        ('5', 'Saturday'),
        ('6', 'Sunday'),
    ], string='Day of Week', required=True)

    start_hour = fields.Float(string='Start Hour', required=True)
    end_hour = fields.Float(string='End Hour', required=True)

    appointment_type = fields.Selection([
        ('online', 'Online'),
        ('offline', 'In-Person'),
    ], string='Type', default='offline')

    # 5.1. SQL Constraints Час закінчення > час початку в розкладі лікаря
    # _check_hours_order = models.Constraint(
    #     'CHECK(end_hour > start_hour)',
    #     'The end hour must be greater than the start hour!'
    # )
    _check_hours_order = models.Constraint(
        'CHECK(start_hour < end_hour)',
        'The start hour must be earlier than the end hour!',
    )
