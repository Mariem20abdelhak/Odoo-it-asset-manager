from datetime import date, timedelta
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


ASSET_ASSIGNMENT_MODEL = 'it.asset.assignment'


class ItAsset(models.Model):
    _name = 'it.asset'
    _description = 'Asset informatique'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'name'

    # ── Identification ──────────────────────────────────────────────────────────
    name = fields.Char(string='Nom', required=True, tracking=True)
    reference = fields.Char(string='Référence', readonly=True, copy=False, default='Nouveau')
    category_id = fields.Many2one('it.asset.category', string='Catégorie',required=True, tracking=True, ondelete='restrict')
    brand = fields.Char(string='Marque', tracking=True)
    model_name = fields.Char(string='Modèle', tracking=True)
    serial_number = fields.Char(string='Numéro de série', tracking=True, copy=False)

    # ── État ────────────────────────────────────────────────────────────────────
    state = fields.Selection([
        ('available', 'Disponible'),
        ('assigned', 'Affecté'),
        ('maintenance', 'En maintenance'),
        ('retired', 'Retraité'),
    ], string='État', default='available', required=True, tracking=True)

    condition = fields.Selection([
        ('new', 'Neuf'), ('good', 'Bon état'), ('fair', 'État correct'), ('poor', 'Mauvais état'),
    ], string='Condition', default='new', tracking=True)

    # ── Garantie ────────────────────────────────────────────────────────────────
    purchase_date = fields.Date(string="Date d'achat", tracking=True)
    warranty_end_date = fields.Date(string='Fin de garantie', tracking=True)
    warranty_status = fields.Selection([
        ('valid', 'En garantie'), ('expiring', 'Expire bientôt'),
        ('expired', 'Expirée'), ('none', 'Sans garantie'),
    ], string='Statut garantie', compute='_compute_warranty_status', store=True)
    days_until_warranty_end = fields.Integer(
        string='Jours avant fin de garantie',
        compute='_compute_warranty_status', store=True)

    # ── Financier ───────────────────────────────────────────────────────────────
    purchase_price = fields.Float(string="Prix d'achat", digits=(10, 2), tracking=True)
    currency_id = fields.Many2one('res.currency', string='Devise',default=lambda self: self.env.company.currency_id)
    supplier_id = fields.Many2one('res.partner', string='Fournisseur',domain=[('supplier_rank', '>', 0)])

    # ── Affectation ─────────────────────────────────────────────────────────────
    employee_id = fields.Many2one('hr.employee', string='Employé affecté', tracking=True)
    location = fields.Char(string='Emplacement physique', tracking=True)
    assignment_ids = fields.One2many(ASSET_ASSIGNMENT_MODEL, 'asset_id', string="Historique d'affectations")
    assignment_count = fields.Integer(string='Affectations', compute='_compute_assignment_count')
    notes = fields.Html(string='Notes techniques')

    # ── Computed ────────────────────────────────────────────────────────────────
    @api.depends('warranty_end_date')
    def _compute_warranty_status(self):
        today = date.today()
        for asset in self:
            if not asset.warranty_end_date:
                asset.warranty_status = 'none'
                asset.days_until_warranty_end = 0
                continue
            delta = (asset.warranty_end_date - today).days
            asset.days_until_warranty_end = delta
            if delta < 0:
                asset.warranty_status = 'expired'
            elif delta <= 30:
                asset.warranty_status = 'expiring'
            else:
                asset.warranty_status = 'valid'

    def _compute_assignment_count(self):
        for asset in self:
            asset.assignment_count = len(asset.assignment_ids)

    # ── Séquence ────────────────────────────────────────────────────────────────
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('reference', 'Nouveau') == 'Nouveau':
                vals['reference'] = self.env['ir.sequence'].next_by_code('it.asset') or 'Nouveau'
        return super().create(vals_list)

    # ── Contraintes ─────────────────────────────────────────────────────────────
    @api.constrains('serial_number')
    def _check_serial_number_unique(self):
        for asset in self:
            if asset.serial_number:
                duplicate = self.search([
                    ('serial_number', '=', asset.serial_number),
                    ('id', '!=', asset.id),
                ])
                if duplicate:
                    raise ValidationError(
                        _('Le numéro de série "%s" est déjà utilisé par "%s".')
                        % (asset.serial_number, duplicate.name)
                    )

    @api.constrains('purchase_date', 'warranty_end_date')
    def _check_warranty_date(self):
        for asset in self:
            if (asset.purchase_date and asset.warranty_end_date
                    and asset.warranty_end_date < asset.purchase_date):
                raise ValidationError(
                    _("La date de fin de garantie ne peut pas être antérieure à la date d'achat.")
                )

    # ── Actions ─────────────────────────────────────────────────────────────────
    def action_assign(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _("Affecter l'asset"),
            'res_model': ASSET_ASSIGNMENT_MODEL,
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_asset_id': self.id,
                'default_date_start': fields.Date.today(),
            },
        }

    def action_set_maintenance(self):
        self.write({'state': 'maintenance'})
        self.message_post(body=_('Asset mis en maintenance.'))

    def action_set_available(self):
        self.write({'state': 'available', 'employee_id': False})
        self.message_post(body=_('Asset remis en stock.'))

    def action_retire(self):
        self.write({'state': 'retired'})
        self.message_post(body=_('Asset retraité.'))

    def action_view_assignments(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _("Historique des affectations"),
            'res_model': ASSET_ASSIGNMENT_MODEL,
            'view_mode': 'list,form',
            'domain': [('asset_id', '=', self.id)],
        }

    # ── Cron ────────────────────────────────────────────────────────────────────
    @api.model
    def _cron_warranty_expiry_alerts(self):
        """Envoi d'alertes email 30 jours avant fin de garantie."""
        alert_date = date.today() + timedelta(days=30)
        expiring = self.search([
            ('warranty_end_date', '=', alert_date),
            ('state', '!=', 'retired'),
        ])
        for asset in expiring:
            asset.message_post(
                body=_('La garantie de cet asset expire dans 30 jours (%s). '
                'Pensez à renouveler le contrat ou planifier un remplacement.')
                    % asset.warranty_end_date,
                subject=_('Alerte garantie — %s') % asset.name,
                message_type='email',
                subtype_xmlid='mail.mt_comment',
            )
