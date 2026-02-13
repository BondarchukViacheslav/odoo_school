import logging

from odoo import models, fields
from datetime import timedelta

_logger = logging.getLogger(__name__)


class HRHospitalDoctorScheduleWizard(models.TransientModel):
    _name = 'hr.hospital.doctor.schedule.wizard'
    _description = 'Wizard to Fill Doctor Schedule'

    doctor_id = fields.Many2one(
        'hr.hospital.doctor',
        string='Doctor',
        required=True
    )

    start_date = fields.Date(
        string='Start Week Date',
        required=True,
        default=fields.Date.today
    )

    weeks_count = fields.Integer(
        string='Weeks Count',
        default=1,
        required=True
    )

    schedule_type = fields.Selection([
        ('standard', 'Standard (Every Week)'),
        ('even', 'Even Weeks'),
        ('odd', 'Odd Weeks')
    ], string='Schedule Type', default='standard', required=True)

    # Дні тижня
    mo = fields.Boolean('Mon')
    tu = fields.Boolean('Tue')
    we = fields.Boolean('Wed')
    th = fields.Boolean('Thu')
    fr = fields.Boolean('Fri')
    sa = fields.Boolean('Sat')
    su = fields.Boolean('Sun')

    start_hour = fields.Float('Start Hour', default=8.0)
    end_hour = fields.Float('End Hour', default=17.0)
    break_start = fields.Float('Break From', default=12.0)
    break_end = fields.Float('Break To', default=13.0)

    def action_generate_schedule(self):
        self.ensure_one()
        days_map = {
            '0': self.mo, '1': self.tu, '2': self.we,
            '3': self.th, '4': self.fr, '5': self.sa, '6': self.su
        }

        current_date = self.start_date
        end_date = self.start_date + timedelta(weeks=self.weeks_count)

        schedule_vals = []

        while current_date < end_date:
            week_number = current_date.isocalendar()[1]
            is_even = week_number % 2 == 0

            skip = False
            if self.schedule_type == 'even' and not is_even:
                skip = True
            elif self.schedule_type == 'odd' and is_even:
                skip = True

            day_num = str(current_date.weekday())
            if not skip and days_map.get(day_num):
                schedule_vals.append({
                    'doctor_id': self.doctor_id.id,
                    # 'date': current_date,
                    'day_of_week': day_num,
                    'start_hour': self.start_hour,
                    'end_hour': self.break_start,
                })
                schedule_vals.append({
                    'doctor_id': self.doctor_id.id,
                    # 'date': current_date,
                    'day_of_week': day_num,
                    'start_hour': self.break_end,
                    'end_hour': self.end_hour,
                })

            current_date += timedelta(days=1)

        if schedule_vals:
            self.env['hr.hospital.doctor.schedule'].create(schedule_vals)

        return {'type': 'ir.actions.act_window_close'}
