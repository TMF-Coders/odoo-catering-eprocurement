# Catering e-Procurement Kiosk

Part of the **Vituallas HORECA Suite**. This module adds a simplified, touch-friendly kiosk interface for kitchens and chefs to rapidly order supplies without navigating complex backend menus.

## Features
- **Supplier Selection**: Visual grid of available suppliers.
- **Product Catalog**: Quick search and add-to-cart mechanism for ingredients.
- **Background PO Generation**: Automatically generates Odoo Purchase Orders (`purchase.order`).
- **Cart System**: Review and modify quantities before sending to the supplier.

## Technical Details
Built entirely with **OWL 3** for Odoo 19.
Hooks directly into standard Odoo purchase flows.

## Pre-commit
This repository uses OCA pre-commit hooks.
```bash
pre-commit install
```
