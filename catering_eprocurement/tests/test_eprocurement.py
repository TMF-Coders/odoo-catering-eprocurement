from odoo.tests.common import TransactionCase

class TestEProcurement(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.supplier = cls.env['res.partner'].create({
            'name': 'Test Supplier',
            'supplier_rank': 1
        })
        cls.product = cls.env['product.product'].create({
            'name': 'Test Ingredient',
            'type': 'product',
            'purchase_ok': True,
        })
        # Add supplier info
        cls.env['product.supplierinfo'].create({
            'partner_id': cls.supplier.id,
            'product_tmpl_id': cls.product.product_tmpl_id.id,
            'price': 10.0,
        })

    def test_kiosk_order_creation(self):
        """Test that the custom API correctly generates a PO."""
        order_lines = [{'product_id': self.product.id, 'product_qty': 5.0}]
        
        po_id = self.env['purchase.order'].create_kiosk_order(self.supplier.id, order_lines)
        po = self.env['purchase.order'].browse(po_id)
        
        self.assertTrue(po.exists())
        self.assertEqual(po.partner_id.id, self.supplier.id)
        self.assertTrue(po.is_kiosk_order)
        self.assertEqual(len(po.order_line), 1)
        self.assertEqual(po.order_line[0].product_id.id, self.product.id)
        self.assertEqual(po.order_line[0].product_qty, 5.0)
        # Verify that price computation worked (it should pull 10.0 from supplier info)
        self.assertEqual(po.order_line[0].price_unit, 10.0)
