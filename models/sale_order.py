from odoo import api, models, tools, fields, _
from odoo.exceptions import UserError, ValidationError

class SaleOrder(models.Model):
    """Inherit to create PO while create SO"""
    _inherit = 'sale.order'

    def action_quotation_send(self):
        res = super(SaleOrder, self).action_quotation_send()

        for order in self:
            company_id = self.env['res.company'].search([('name', '=', order.partner_id.name)], limit=1)

            if not company_id:
                raise UserError(_("Company not found for partner %s") % order.partner_id.name)

            purchase_order = self.env['purchase.order'].sudo().search([('display_name', '=', order.client_order_ref)], limit=1)

            purchase_order_vals = {
                'partner_id': order.company_id.partner_id.id,
                'company_id': company_id.id,
                'order_line': [(0, 0, {
                    'product_id': line.product_id.id,
                    'product_qty': line.product_uom_qty,
                    'price_unit': line.price_unit,
                    'price_subtotal': line.price_subtotal,
                }) for line in order.order_line],
            }

            if purchase_order:
                purchase_order.write({'order_line': [(5, 0, 0)]})
                purchase_order.write(purchase_order_vals)
            else:
                self.env['purchase.order'].sudo().create(purchase_order_vals)
        return res

    def action_confirm(self):
        call = super(SaleOrder, self).action_confirm()
        stock_picking = self.env['stock.picking'].search([('origin', '=', self.name)], limit=1)

        if stock_picking:
            stock_picking.write({'state': 'confirmed'})

        return call







