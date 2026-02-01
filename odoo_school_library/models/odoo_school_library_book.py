import logging

from odoo import models, fields

CONST_EXP = "Odoo school constant example"

logger = logging.getLogger(__name__)

class OSLBook(models.Model):
    _name = 'odoo.school.library.book'
    _description = 'Book'

    name = fields.Char()

    active = fields.Boolean(default=True, )

    description = fields.Char()

    res_partner_id = fields.Many2one(
        comodel_name='res.partner',
        string='Main Author',
    )

    res_partner_ids = fields.Many2many(
        comodel_name='res.partner',
        string='Additional Author',
    )
