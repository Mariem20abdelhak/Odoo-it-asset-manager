from odoo import fields, models


class ItAssetCategory(models.Model):
    _name = 'it.asset.category'
    _description = "Catégorie d'asset IT"
    _order = 'name'

    name = fields.Char(string='Catégorie', required=True, translate=True)
    code = fields.Char(string='Code', size=10,
    help="Code court utilisé dans la référence (ex: PC, SRV, TEL)")
    description = fields.Text(string='Description')
    color = fields.Integer(string='Couleur')
    asset_ids = fields.One2many('it.asset', 'category_id', string='Assets')
    asset_count = fields.Integer(string="Nombre d'assets", compute='_compute_asset_count')

    def _compute_asset_count(self):
        for rec in self:
            rec.asset_count = len(rec.asset_ids)

    def action_view_assets(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': f'Assets — {self.name}',
            'res_model': 'it.asset',
            'view_mode': 'kanban,list,form',
            'domain': [('category_id', '=', self.id)],
            'context': {'default_category_id': self.id},
        }
