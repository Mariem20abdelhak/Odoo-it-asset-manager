from datetime import date, timedelta
from odoo.tests import TransactionCase, tagged


@tagged('post_install', '-at_install', 'it_asset')
class TestItAsset(TransactionCase):
    """Tests unitaires pour le module IT Asset Manager."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        # Catégorie
        cls.category_pc = cls.env['it.asset.category'].create({
            'name': 'Ordinateur portable',
            'code': 'PC',
        })

        # Employé de test
        cls.employee = cls.env['hr.employee'].create({
            'name': 'Jean Dupont Test',
        })

        # Asset de base
        cls.asset = cls.env['it.asset'].create({
            'name': 'MacBook Pro Test',
            'category_id': cls.category_pc.id,
            'brand': 'Apple',
            'model_name': 'MacBook Pro 14"',
            'serial_number': 'SN-TEST-001',
            'purchase_date': date.today() - timedelta(days=365),
            'warranty_end_date': date.today() + timedelta(days=60),
            'purchase_price': 2500.0,
        })

    # ── Séquence ────────────────────────────────────────────────────────────────

    def test_reference_generated(self):
        """La référence doit être auto-générée à la création."""
        self.assertNotEqual(self.asset.reference, 'Nouveau')
        self.assertIn('ASSET/', self.asset.reference)

    # ── Statut garantie ─────────────────────────────────────────────────────────

    def test_warranty_status_valid(self):
        """Asset avec garantie à 60 jours → statut 'valid'."""
        self.assertEqual(self.asset.warranty_status, 'valid')
        self.assertGreater(self.asset.days_until_warranty_end, 30)

    def test_warranty_status_expiring(self):
        """Asset avec garantie à 15 jours → statut 'expiring'."""
        self.asset.warranty_end_date = date.today() + timedelta(days=15)
        self.assertEqual(self.asset.warranty_status, 'expiring')

    def test_warranty_status_expired(self):
        """Asset avec garantie dépassée → statut 'expired'."""
        self.asset.warranty_end_date = date.today() - timedelta(days=10)
        self.assertEqual(self.asset.warranty_status, 'expired')

    def test_warranty_status_none(self):
        """Asset sans date de garantie → statut 'none'."""
        self.asset.warranty_end_date = False
        self.assertEqual(self.asset.warranty_status, 'none')

    # ── Numéro de série unique ───────────────────────────────────────────────────

    def test_serial_number_unique(self):
        """Deux assets ne peuvent pas avoir le même numéro de série."""
        from odoo.exceptions import ValidationError
        with self.assertRaises(ValidationError):
            self.env['it.asset'].create({
                'name': 'Doublon',
                'category_id': self.category_pc.id,
                'serial_number': 'SN-TEST-001',  # déjà pris
            })

    # ── Affectation ─────────────────────────────────────────────────────────────

    def test_assignment_changes_state(self):
        """Créer une affectation passe l'asset en état 'assigned'."""
        self.assertEqual(self.asset.state, 'available')
        self.env['it.asset.assignment'].create({
            'asset_id': self.asset.id,
            'employee_id': self.employee.id,
            'date_start': date.today(),
        })
        self.assertEqual(self.asset.state, 'assigned')
        self.assertEqual(self.asset.employee_id, self.employee)

    def test_return_asset_sets_available(self):
        """Retourner un asset remet l'état à 'available'."""
        assignment = self.env['it.asset.assignment'].create({
            'asset_id': self.asset.id,
            'employee_id': self.employee.id,
            'date_start': date.today(),
        })
        assignment.action_return_asset()
        self.assertEqual(self.asset.state, 'available')
        self.assertFalse(self.asset.employee_id)

    def test_assignment_count(self):
        """Le compteur d'affectations est correct."""
        initial = self.asset.assignment_count
        self.env['it.asset.assignment'].create({
            'asset_id': self.asset.id,
            'employee_id': self.employee.id,
            'date_start': date.today(),
        })
        self.assertEqual(self.asset.assignment_count, initial + 1)

    # ── Contrainte dates ─────────────────────────────────────────────────────────

    def test_warranty_date_before_purchase(self):
        """La fin de garantie ne peut pas précéder la date d'achat."""
        from odoo.exceptions import ValidationError
        with self.assertRaises(ValidationError):
            self.env['it.asset'].create({
                'name': 'Asset invalide',
                'category_id': self.category_pc.id,
                'purchase_date': date.today(),
                'warranty_end_date': date.today() - timedelta(days=1),
            })

    # ── Actions état ─────────────────────────────────────────────────────────────

    def test_action_set_maintenance(self):
        self.asset.action_set_maintenance()
        self.assertEqual(self.asset.state, 'maintenance')

    def test_action_retire(self):
        self.asset.action_retire()
        self.assertEqual(self.asset.state, 'retired')

    def test_cron_warranty_alerts(self):
        """Le cron ne plante pas et envoie un message sur les assets concernés."""
        self.asset.warranty_end_date = date.today() + timedelta(days=30)
        msg_count_before = len(self.asset.message_ids)
        self.env['it.asset']._cron_warranty_expiry_alerts()
        self.assertGreater(len(self.asset.message_ids), msg_count_before)
