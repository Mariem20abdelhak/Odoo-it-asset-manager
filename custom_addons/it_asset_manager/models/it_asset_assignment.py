from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class ItAssetAssignment(models.Model):
    _name = 'it.asset.assignment'
    _description = "Affectation d'asset IT"
    _order = 'date_start desc'
    _inherit = ['mail.thread']

    asset_id = fields.Many2one(
                                'it.asset', string='Asset', required=True,
                                ondelete='cascade', tracking=True)
    employee_id = fields.Many2one(
                                'hr.employee', string='Employé', required=True,
                                tracking=True, ondelete='restrict')
    date_start = fields.Date(
                            string="Date d'affectation", required=True,
                            default=fields.Date.today, tracking=True)
    date_end = fields.Date(string='Date de retour', tracking=True)
    is_active = fields.Boolean(
                            string='Affectation active',
                            compute='_compute_is_active', store=True)
    notes = fields.Text(string='Notes')

    @api.depends('date_end')
    def _compute_is_active(self):
        today = fields.Date.today()
        for rec in self:
            rec.is_active = not rec.date_end or rec.date_end >= today

    @api.constrains('date_start', 'date_end')
    def _check_dates(self):
        for rec in self:
            if rec.date_end and rec.date_end < rec.date_start:
                raise ValidationError(
                    _("La date de retour ne peut pas être antérieure à la date d'affectation.")
                )

    def write(self, vals):
        result = super().write(vals)
        if vals.get('date_end'):
            for rec in self:
                rec.asset_id.write({
                    'state': 'available', 'employee_id': False})
        return result

    @api.model_create_multi
    def create(self, vals_list):
        records = super().create(vals_list)
        for rec in records:
            rec.asset_id.write({
                'state': 'assigned', 'employee_id': rec.employee_id.id})
            rec.asset_id.message_post(
                body=_('Asset affecté à %s le %s.') % 
                (rec.employee_id.name, rec.date_start)
            )
        return records

    def action_return_asset(self):
        self.write({'date_end': fields.Date.today()})
