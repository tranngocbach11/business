from odoo import api, models, tools, fields, _
from odoo.exceptions import UserError, ValidationError

class PurchaseOrder(models.Model):
    _inherit = "purchase.order"
    _description = "Extend the purchase model"

    def action_rfq_send(self):
        # Override
        res = super(PurchaseOrder, self).action_rfq_send()

        for order in self:
            company_id = self.env['res.company'].search([('name', '=', order.partner_id.name)], limit=1)

            if not company_id:
                raise UserError(_("Company not found for partner %s") % order.partner_id.name)

            sale_order = self.env['sale.order'].sudo().search([('client_order_ref', '=', order.name)], limit=1)
            sale_order_vals = {
                'partner_id': order.company_id.partner_id.id,
                'company_id': company_id.id,
                'client_order_ref': order.name,
                'order_line': [(0, 0, {
                    'product_id': rec.product_id.id,
                    'product_uom_qty': rec.product_qty,
                    'price_unit': rec.price_unit,
                    'price_subtotal': rec.price_subtotal
                }) for rec in order.order_line]
            }
            if sale_order:
                sale_order.write({'order_line': [(5, 0, 0)]})
                sale_order.write(sale_order_vals)
            else:
                self.env['sale.order'].sudo().create(sale_order_vals)
        return res

    def button_confirm(self):
        call = super(PurchaseOrder, self).button_confirm()

        sale_order = self.env['sale.order'].sudo().search([('client_order_ref', '=', self.name)], limit=1)
        if sale_order and sale_order.state != 'sale':
            raise ValidationError('A purchase order cannot be confirmed before the sales order has been confirmed.')

        stock_picking = self.env['stock.picking'].search([('origin', '=', self.name)], limit=1)

        if stock_picking:
            stock_picking.write({'state': 'draft'})

        return call

    def action_post(self):
        res = super(PurchaseOrder, self).action_post()
        sale_order = self.env['sale.order'].sudo().search([('client_order_ref', '=', self)], limit=1)
        if sale_order and sale_order.invoice_ids.state != 'posted':
            raise ValidationError(
                'A bill of purchase order cannot be confirmed before the bill of sales order has been confirmed.')
        return res


    

