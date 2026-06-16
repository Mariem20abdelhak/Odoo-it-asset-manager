# 📦 IT Asset Manager (Odoo Module)

![Odoo](https://img.shields.io/badge/Odoo-16.0-875A7B?logo=odoo&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Database-336791?logo=postgresql&logoColor=white)
![License](https://img.shields.io/badge/License-Educational-lightgrey)

---

## 🚀 Overview

A custom **Odoo ERP module** for managing IT assets lifecycle, including assignment, tracking, and return workflows.

It provides a structured way to manage company equipment (laptops, desktops, peripherals) and their assignment to employees.


### 🖥️ Asset Management
- Create and track IT assets
- Store key metadata (serial number, type, status)

### 👤 Employee Assignment
- Assign assets to employees
- Track assignment period (`date_start`, `date_end`)

### 🔁 Return Workflow
- One-click return asset action
- Automatic status update

### 🔘 Status Control
- Active / Inactive toggle
- Real-time lifecycle tracking

---

## 🧱 Architecture
Odoo 17 Framework
│
├── Python ORM (models)
├── XML Views (UI layer)
├── PostgreSQL (data layer)
└── Business Logic (server actions)



---

## 📁 Project Structure

it_asset_manager/
│
├── models/
│ └── it_asset.py
│
├── views/
│ └── it_asset_views.xml
│
├── security/
│ └── ir.model.access.csv
│
├── static/
│ └── description/
│ └── icon.png
│
├── docs/
│ ├── screens/
│ │ ├── asset_list.png
│ │ ├── asset_form.png
│
├── manifest.py
└── README.md
---

## 🖼️ Screenshots

### 📋 Asset List View
![Asset List](docs/screens/list1.png)
![Asset List](docs/screens/list2.png)

### 📝 Asset Form View
![Asset Form](docs/screens/form1.png)
![Asset Form](docs/screens/form2.png)
![Asset Form](docs/screens/form3.png)

### 🔄 Assignment Dashboard
![Workflow](docs/screens/Tableaudeboard.png)

---

## ⚙️ Installation

```bash
git clone https://github.com/USERNAME/it_asset_manager.git
cd it_asset_manager
