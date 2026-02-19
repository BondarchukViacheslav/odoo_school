from odoo import models, fields


class HRHospitalContactPerson(models.Model):
    _name = 'hr.hospital.contact.person'
    _description = 'Contact person'
    _rec_name = 'full_name'
    _inherit = ['hr.hospital.abstract.person']

    # Наслідування: від abstract.person.
    # При створенні контактної особи за допомогою домену
    # показувати тільки пацієнтів з заповненим полем "алергії"

    patient_ids = fields.One2many(
        comodel_name='hr.hospital.patient',
        inverse_name='contact_person_id',
        string='Patients',
        domain="[('allergies', '!=', False), ('allergies', '!=', '')]"
    )

    # res_partner_id = fields.Many2one(
    #     'res.partner',
    #     string='Contact',
    #     required=True,
    #     ondelete='cascade')
    # name = fields.Char(
    #     related='res_partner_id.name',
    #     readonly=False)
    #
    # #    name = fields.Char(string='Full Name', required=True)
    # specialty = fields.Char(
    #     string='Specialty',
    #     required=True)
