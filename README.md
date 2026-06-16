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

![Asset List 1](docs/screens/list1.png)

![Asset List 2](docs/screens/list2.png)

---

### 📝 Asset Form View

![Asset Form 1](docs/screens/form1.png)

![Asset Form 2](docs/screens/form2.png)

![Asset Form 3](docs/screens/form3.png)

---

### 🔄 Assignment Dashboard

![Workflow](docs/screens/Tableaudeboard.png)

---
## ⚙️ Installatio

git clone https://github.com/USERNAME/it_asset_manager.git
cd it_asset_manager

### Move to Odoo addons
cp -r it_asset_manager /odoo/custom_addons/
### Restart Odoo & update module
./odoo-bin -c odoo.conf -u it_asset_manager
🧠 Core Data Model
### Field	Type	Description
name	Char	Asset name
employee_id	Many2one	Assigned employee
date_start	Date	Assignment start
date_end	Date	Assignment end
is_active	Boolean	Asset state
### 🔧 Business Logic
action_return_asset()
Unassigns employee
Marks asset as returned
Updates lifecycle state
### 📈 Roadmap
QR Code asset tagging 📱
Maintenance scheduling 🛠️
Depreciation tracking 📉
Dashboard analytics 📊
Asset category hierarchy 🗂️
### 🧪 Fixes Implemented
Fixed Odoo view validation error (missing date_start)
Synchronized XML views with ORM model
Stabilized module installation process
### 👨‍💻 Author

Mariem
Software Developer | Odoo | Cybersecurity | AI Systems

### ⭐ Repository Goal

This project demonstrates:

ERP customization skills (Odoo)
Backend Python ORM design
Business workflow modeling
Production-grade module structuring


