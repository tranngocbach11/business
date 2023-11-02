from odoo import models, api

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    def action_assign(self):
        res = super(StockPicking, self).action_assign()

        for picking in self:
            if picking.origin:
                sale_order = self.env['sale.order'].sudo().search([('name', '=', picking.origin)], limit=1)
                if sale_order and sale_order.picking_ids.filtered(lambda p: p.state == 'assigned'):
                    purchase_order = self.env['purchase.order'].sudo().search(
                        [('name', '=', sale_order.client_order_ref)], limit=1)
                    if purchase_order:
                        purchase_order_picking = purchase_order.picking_ids.filtered(lambda p: p.state != ['ready', 'done'])
                        if purchase_order_picking:
                            purchase_order_picking.write({'state': 'assigned'})

        return res