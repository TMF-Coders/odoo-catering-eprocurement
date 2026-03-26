{
    'name': 'Catering e-Procurement Kiosk',
    'version': '19.0.1.0.0',
    'category': 'Inventory/Purchase',
    'summary': 'Touch-friendly B2B purchasing kiosk for kitchen staff and chefs',
    'description': """
Vituallas HORECA Suite: Catering e-Procurement
==============================================
Part of the Vituallas Catering Suite.
Transforms Odoo's standard purchase flow into a high-speed, touch-friendly 
kiosk for kitchens, replacing complex RFQs with a "shopping cart" B2B experience.

Features:
- **Chef Kiosk**: Touch UI for rapid supplier selection and product ordering.
- **Auto-PO**: Generates confirmed Purchase Orders or RFQs in the background.
- **Suite Integration**: Works seamlessly alongside Food Waste Manager and Supply Forecast.
    """,
    'author': 'TMFCoders SL',
    'license': 'OPL-1',
    'depends': ['purchase', 'stock', 'product', 'web'],
    'data': [
        'security/catering_security.xml',
        'views/catering_menus.xml',
        'views/kiosk_action.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'catering_eprocurement/static/src/components/kiosk/eprocurement_kiosk.scss',
            'catering_eprocurement/static/src/components/kiosk/eprocurement_kiosk.xml',
            'catering_eprocurement/static/src/components/kiosk/eprocurement_kiosk.js',
        ],
    },
    'installable': True,
    'application': True,
}
