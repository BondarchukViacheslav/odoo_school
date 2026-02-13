import logging

import json
import io
import csv
import base64
from odoo import models, fields, api

_logger = logging.getLogger(__name__)


class HRospitalPatientCardExportWizard(models.TransientModel):
    _name = 'hr.hospital.patient.card.export.wizard'
    _description = 'Patient Card Export Wizard'

    patient_id = fields.Many2one(
        'hr.hospital.patient',
        string='Patient',
        required=True
    )

    start_date = fields.Date(string='Start Date')
    end_date = fields.Date(string='End Date')

    include_diagnoses = fields.Boolean(
        string='Include Diagnoses',
        default=True
    )

    include_recommendations = fields.Boolean(
        string='Include Recommendations',
        default=True
    )

    lang_id = fields.Many2one('res.lang', string='Report Language')
    export_format = fields.Selection([
        ('json', 'JSON'),
        ('csv', 'CSV')
    ], string='Export Format', default='json', required=True)

    # Поля для завантаження файлу
    file_data = fields.Binary(readonly=True)
    file_name = fields.Char(readonly=True)

    @api.onchange('patient_id')
    def _onchange_patient_id(self):
        if self.patient_id:
            self.lang_id = self.patient_id.lang_id

    def action_export(self):
        self.ensure_one()

        # 1. Пошук діагнозів за критеріями
        domain = [('visit_id.patient_id', '=', self.patient_id.id)]
        if self.start_date:
            domain.append(('visit_id.planned_date', '>=', self.start_date))
        if self.end_date:
            domain.append(('visit_id.planned_date', '<=', self.end_date))

        diagnoses = self.env['hr.hospital.diagnosis'].search(domain)

        # 2. Підготовка структури даних
        data = []
        for diag in diagnoses:
            item = {
                'date': str(diag.visit_id.planned_date),
                'doctor': diag.visit_id.doctor_id.full_name,
                'disease': diag.disease_id.name,
            }
            if self.include_diagnoses:
                item['diagnosis'] = diag.description
            if self.include_recommendations:
                item['treatment'] = diag.treatment
            data.append(item)

        # 3. Генерація файлу
        if self.export_format == 'json':
            output = json.dumps(data, indent=4, ensure_ascii=False)
            file_content = output.encode('utf-8')
            extension = 'json'
        else:
            output = io.StringIO()
            writer = csv.DictWriter(
                output,
                fieldnames=data[0].keys()
                if data else []
            )

            writer.writeheader()
            writer.writerows(data)
            file_content = output.getvalue().encode('utf-8')
            extension = 'csv'

        # 4. Запис файлу в базу та повернення вікна для завантаження
        self.write({
            'file_data': base64.b64encode(file_content),
            'file_name': f"medical_card_{self.patient_id.id}.{extension}"
        })

        return {
            'type': 'ir.actions.act_window',
            'res_model': self._name,
            'res_id': self.id,
            'view_mode': 'form',
            'target': 'new',
        }
