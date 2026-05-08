# IT Asset Manager — Module Odoo 17

> Module de gestion de parc informatique développé pour Odoo 17.  
> Projet portfolio — démonstration de compétences Odoo développeur.

---

## Fonctionnalités

- **Catalogue d'assets IT** — ordinateurs, serveurs, téléphones, périphériques
- **Affectation aux employés** avec historique complet
- **Suivi de garantie** — alertes automatiques 30 jours avant expiration (cron)
- **États et workflow** — Disponible → Affecté → Maintenance → Retraité
- **Dashboard KPIs** — graphiques par catégorie, état, coût total (graph + pivot)
- **Rapport PDF QWeb** — fiche asset imprimable
- **Sécurité** — deux groupes : Utilisateur (lecture) / Gestionnaire (CRUD)
- **Tests unitaires** — couverture des modèles et contraintes métier

---

## Stack technique

| Couche | Technologies |
|---|---|
| Backend | Python 3, Odoo ORM (`models.Model`, `@api.depends`, `@api.constrains`) |
| Vues | XML (form, list, kanban, search, graph, pivot) |
| Rapports | QWeb PDF |
| Automatisation | `ir.cron`, `mail.thread` |
| Sécurité | `ir.model.access`, groupes XML |
| Tests | `odoo.tests.TransactionCase` |

---

## Installation

```bash
# 1. Cloner dans le dossier addons de votre instance Odoo
git clone https://github.com/Mariem20abdelhak/Odoo-it-asset-manager/tree/17.0/custom_addons/it_asset_manager

# 2. Redémarrer Odoo avec mise à jour
./odoo-bin -u it_asset_manager -d myodoo

# 3. Activer le mode développeur dans Odoo
# Paramètres > Activer le mode développeur
```

### Dépendances

```python
'depends': ['base', 'mail', 'hr', 'helpdesk']
```

---

## Structure du module

```
it_asset_manager/
├── __manifest__.py
├── __init__.py
├── models/
│   ├── __init__.py
│   ├── it_asset_category.py     # Catégories d'assets
│   ├── it_asset.py              # Modèle principal (ORM, cron, workflow)
│   └── it_asset_assignment.py   # Historique d'affectations
├── views/
│   ├── it_asset_category_views.xml
│   ├── it_asset_views.xml       # Form, List, Kanban, Search
│   ├── it_asset_assignment_views.xml
│   ├── it_asset_dashboard_views.xml
│   ├── hr_employee_views.xml    # Extension fiche employé
│   └── menus.xml
├── security/
│   ├── ir.model.access.csv
│   └── it_asset_security.xml
├── data/
│   ├── it_asset_sequence.xml    # Séquence ASSET/YYYY/XXXX
│   └── it_asset_cron.xml        # Cron alertes garantie
├── report/
│   ├── it_asset_report.xml
│   └── it_asset_report_template.xml
├── tests/
│   ├── __init__.py
│   └── test_it_asset.py         # 10 tests unitaires
└── static/
    └── src/css/dashboard.css
```

---

## Lancer les tests

```bash
./odoo-bin --test-tags it_asset_manager -d myodoo --stop-after-init
```

---

## Concepts Odoo illustrés

- `_inherit = ['mail.thread', 'mail.activity.mixin']` — chatter + activités
- `@api.depends` — champs compute stockés (`warranty_status`, `days_until_warranty_end`)
- `@api.constrains` — validation métier (numéro de série unique, cohérence dates)
- `@api.model_create_multi` — override `create` pour la séquence
- `ir.sequence` — référence auto `ASSET/2025/0001`
- `ir.cron` — tâche planifiée quotidienne
- Héritage de vue `hr.employee` — ajout onglet sans toucher le module HR

---

## Auteur

**Votre Nom** — [LinkedIn](https://www.linkedin.com/in/abdelhak-mariem-200114213/) · [GitHub](https://github.com/Mariem20abdelhak)
