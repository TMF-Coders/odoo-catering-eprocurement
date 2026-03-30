from odoo import models, fields, api

class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    is_kiosk_order = fields.Boolean(
        string='Created via Kiosk', 
        default=False, 
        copy=False,
        help="Indicates if this order was placed through the Chef Kiosk interface."
    )

    @api.model
    def create_kiosk_order(self, partner_id, order_lines):
        """
        API endpoint for the OWL Kiosk to submit an order in one go.
        order_lines is a list of dicts: [{'product_id': int, 'product_qty': float}]
        """
        partner = self.env['res.partner'].browse(partner_id)
        
        lines_vals = []
        for line in order_lines:
            product = self.env['product.product'].browse(line['product_id'])
            # Let the ORM calculate the price based on supplier info or standard price
            lines_vals.append((0, 0, {
                'product_id': product.id,
                'product_qty': line['product_qty'],
                'product_uom': product.uom_po_id.id or product.uom_id.id,
                # name and price_unit will be auto-computed by onchanges usually,
                # but in create we might need to force the compute if not using new()
            }))
            
        po = self.create({
            'partner_id': partner.id,
            'is_kiosk_order': True,
            'order_line': lines_vals,
        })
        
        # In Odoo 18/19, we might want to manually trigger the recompute of prices
        # if the standard create doesn't pull supplier prices properly without onchanges.
        for line in po.order_line:
            line._compute_price_unit_and_date_planned_and_name()

        return po.id
