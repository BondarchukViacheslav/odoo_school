import logging

from odoo import models, fields
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)


class HRHospitalRescheduleVisitWizard(models.TransientModel):
    _name = 'hr.hospital.reschedule.visit.wizard'
    _description = 'Reschedule Visit Wizard'

    visit_id = fields.Many2one(
        'hr.hospital.visit',
        string='Current Visit',
        readonly=True
    )
    new_doctor_id = fields.Many2one(
        'hr.hospital.doctor',
        string='New Doctor'
    )
    new_date = fields.Datetime(string='New Date & time', required=True)
    # new_hour = fields.Float(string='New Time', required=True)
    reason = fields.Text(string='Reason for Rescheduling', required=True)

    def action_reschedule(self):
        self.ensure_one()

        if self.new_date < fields.Datetime.today():
            raise ValidationError(
                "You cannot reschedule a visit to a past date."
            )

        old_visit = self.visit_id

        new_visit_vals = {
            'patient_id': old_visit.patient_id.id,
            'doctor_id': self.new_doctor_id.id or old_visit.doctor_id.id,
            'planned_date': self.new_date,
            # 'planned_hour': self.new_hour,
            'state': 'planned',
            'comment': "Rescheduled from visit #%s. Reason: %s" % (
                old_visit.id, self.reason
            )
        }
        new_visit = self.env['hr.hospital.visit'].create(new_visit_vals)

        old_visit.write({
            'state': 'cancelled',
            # 'active': False
        })

        return {
            'name': 'New Scheduled Visit',
            'type': 'ir.actions.act_window',
            'res_model': 'hr.hospital.visit',
            'res_id': new_visit.id,
            'view_mode': 'form',
            'target': 'current',
        }
