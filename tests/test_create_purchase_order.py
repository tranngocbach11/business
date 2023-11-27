from odoo.tests.common import TransactionCase

class TestPurchaseOrder(TransactionCase):

    def setUp(self):
        super(TestPurchaseOrder, self).setUp()
        self.partner = self.env['res.partner'].create({'name': 'Test Partner'})
        self.product = self.env['product.product'].create({'name': 'Test Product', 'type': 'product'})
        self.purchase_order = self.env['purchase.order'].create({
            'partner_id': self.partner.id,
            'order_line': [(0, 0, {
                'product_id': self.product.id,
                'product_qty': 5,
                'price_unit': 10.0,
            })],
        })

    def test_action_rfq_send(self):
        self.purchase_order.action_rfq_send()

        sale_order = self.env['sale.order'].search([('client_order_ref', '=', self.purchase_order.name)])
        self.assertTrue(sale_order, "Sale Order have not created.")

        self.assertEqual(sale_order.order_line[0].product_id, self.product, "Product mismatch in Sale Order.")
        self.assertEqual(sale_order.order_line[0].product_uom_qty, 5, "Quantity mismatch in Sale Order.")
        self.assertEqual(sale_order.order_line[0].price_unit, 10.0, "Price mismatch in Sale Order.")



