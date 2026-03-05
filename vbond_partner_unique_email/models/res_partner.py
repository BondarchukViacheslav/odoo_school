from odoo import models, api, _
from odoo.exceptions import ValidationError


class ResPartner(models.Model):
    """
    Extends the base res.partner model to enforce email uniqueness.

    This class overrides the default partner behavior by adding a
    database-level SQL constraint. It prevents the creation or
    update of partner records if the provided email already exists
    in the database for another partner.

    Attributes:
         _inherit (str): The name of the model being extended ('res.partner').
        """
    _inherit = 'res.partner'

    # _sql_constraints = [
    #     (
    #         'email_unique',
    #         'unique(email)',
    #         'The email address must be unique across all partners!'
    #     )
    # ]
    @api.constrains('email')
    def _check_unique_email(self):
        for record in self:
            if record.email:
                duplicate = self.search([
                    ('email', '=', record.email),
                    ('id', '!=', record.id)
                ], limit=1)

                if duplicate:
                    raise ValidationError(_("The email %s is already in use by another partner!") % record.email)
