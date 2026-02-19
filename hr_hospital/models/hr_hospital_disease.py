from odoo import models, fields


class HRHospitalDisease(models.Model):
    _name = 'hr.hospital.disease'
    _description = 'Disease Dictionary'
    _parent_name = "parent_id"
    _parent_store = True
    _order = 'parent_path, name'

    name = fields.Char(
        string='Disease Name',
        required=True,
        translate=True)

    code = fields.Char(
        string='ICD-10 Code',
        size=10)

    parent_id = fields.Many2one(
        comodel_name='hr.hospital.disease',
        string='Parent Category',
        ondelete='cascade',
        index=True
    )

    child_ids = fields.One2many(
        comodel_name='hr.hospital.disease',
        inverse_name='parent_id',
        string='Sub-diseases'
    )

    parent_path = fields.Char(index=True)

    severity = fields.Selection([
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('critical', 'Critical')
    ], string='Danger Level', default='low')

    is_contagious = fields.Boolean(
        string='Is Contagious',
        default=False)

    symptoms = fields.Text(
        string='Common Symptoms')

    country_ids = fields.Many2many(
        comodel_name='res.country',
        string='Regions of Prevalence'
    )
