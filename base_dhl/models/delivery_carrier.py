# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


from odoo import models, fields, _, api


class DeliveryCarrier(models.Model):
    _inherit = 'delivery.carrier'

    def get_shipping_price_from_so(self, orders):
        self.ensure_one()
        if self.delivery_type == 'dhl':
            return [0]

    delivery_type = fields.Selection(
        selection_add=[('dhl', "DHL")],
        ondelete={'dhl': lambda recs: recs.write(
            {'delivery_type': 'fixed', 'fixed_price': 0})})

    dhl_user_id = fields.Char(string="DHL User ID")
    dhl_password = fields.Char(string="DHL Password")
    dhl_shipment_option = fields.Selection(
        [('DOOR', 'Door'), ('BP', 'Bp')],
        default="DOOR",
        string="DHL Shipment Option")
    dhl_parcel_type = fields.Selection(
        [('SMALL', 'Small'), ('MEDIUM', 'Medium'), ('LARGE', 'Large'),
         ('PALLET', 'Pallet')], default="SMALL",
        string="DHL Parcel Type")
    dhl_account_id = fields.Char(string="DHL Account ID")


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def _create_delivery_line(self, carrier, price_unit):
        sol = super(SaleOrder, self)._create_delivery_line(carrier, price_unit)
        for s in sol:
            vals = {
                'price_unit': price_unit
            }
            if self._context.get('picking_id'):
                picking_id = self.env['stock.picking'].browse(
                    self._context.get('picking_id')[0])
                vals.update({
                    'qty_delivered': picking_id.number_of_packages
                })
            s.write(vals)
        return sol

    def action_confirm(self):
        for so in self:
            if so.carrier_id and \
                    any([line.product_id.type == 'product' for line in
                         so.order_line]) and \
                    all([not line.is_delivery for line in so.order_line]):
                so.delivery_set()
        return super(SaleOrder, self).action_confirm()


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    is_extra_weight = fields.Boolean(string="Is extra Weight?")
    is_extra_dimension = fields.Boolean(string="Is extra Weight?")


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    is_extra_weight = fields.Boolean(string="Extra cost weight?")
    extra_weight = fields.Integer(string="Value")

    is_extra_dimension = fields.Boolean(string="Extra cost Dimension?")
    extra_dimension = fields.Integer(string="Value")

    @api.onchange('is_extra_weight')
    def _onchange_is_extra_weight(self):
        if not self.is_extra_weight:
            self.extra_weight = 0.0

    @api.onchange('extra_weight')
    def _onchange_extra_weight(self):
        if self.is_extra_weight:
            if self.extra_weight < self._origin.extra_weight:
                warning_mess = {
                    'title': _('Weight decreased!'),
                    'message': _('You are decreasing the weight! '
                                 'Do not forget to manually update '
                                 'the delivery order if needed.'),
                }
                return {'warning': warning_mess}

    @api.onchange('extra_dimension')
    def _onchange_extra_dimension(self):
        if self.is_extra_dimension:
            if self.extra_dimension < self._origin.extra_dimension:
                warning_mess = {
                    'title': _('Dimension decreased!'),
                    'message': _('You are decreasing the dimension! '
                                 'Do not forget to manually update '
                                 'the delivery order if needed.'),
                }
                return {'warning': warning_mess}

    @api.onchange('is_extra_dimension')
    def _onchange_is_extra_dimension(self):
        if not self.is_extra_dimension:
            self.extra_dimension = 0.0

    def _add_delivery_cost_to_so(self):
        self.ensure_one()
        sale_order = self.sale_id
        if sale_order.invoice_shipping_on_delivery:
            sale_order.with_context(picking_id=self.ids)._create_delivery_line(
                self.carrier_id, self.carrier_price)

    # @api.multi
    # def do_transfer(self):
    #     """ If no pack operation, we do simple action_done of the picking.
    #     Otherwise, do the pack operations. """
    #     # TDE CLEAN ME: reclean me, please
    #     self._create_lots_for_picking()
    #
    #     no_pack_op_pickings = self.filtered(lambda picking: not picking.pack_operation_ids)
    #     no_pack_op_pickings.action_done()
    #     if no_pack_op_pickings:
    #         no_pack_op_pickings.action_set_delivered_qty()
    #     other_pickings = self - no_pack_op_pickings
    #     if other_pickings:
    #         other_pickings.action_set_delivered_qty()
    #     for picking in other_pickings:
    #         need_rereserve, all_op_processed = picking.picking_recompute_remaining_quantities()
    #         todo_moves = self.env['stock.move']
    #         toassign_moves = self.env['stock.move']
    #
    #         # create extra moves in the picking (unexpected product moves coming from pack operations)
    #         if not all_op_processed:
    #             todo_moves |= picking._create_extra_moves()
    #
    #         if need_rereserve or not all_op_processed:
    #             moves_reassign = any(x.origin_returned_move_id or x.move_orig_ids for x in picking.move_lines if x.state not in ['done', 'cancel'])
    #             if moves_reassign and picking.location_id.usage not in ("supplier", "production", "inventory"):
    #                 # unnecessary to assign other quants than those involved with pack operations as they will be unreserved anyways.
    #                 picking.with_context(reserve_only_ops=True, no_state_change=True).rereserve_quants(move_ids=picking.move_lines.ids)
    #             picking.do_recompute_remaining_quantities()
    #
    #         # split move lines if needed
    #         for move in picking.move_lines:
    #             rounding = move.product_id.uom_id.rounding
    #             remaining_qty = move.remaining_qty
    #             if move.state in ('done', 'cancel'):
    #                 # ignore stock moves cancelled or already done
    #                 continue
    #             elif move.state == 'draft':
    #                 toassign_moves |= move
    #             if float_compare(remaining_qty, 0,  precision_rounding=rounding) == 0:
    #                 if move.state in ('draft', 'assigned', 'confirmed'):
    #                     todo_moves |= move
    #             elif float_compare(remaining_qty, 0, precision_rounding=rounding) > 0 and float_compare(remaining_qty, move.product_qty, precision_rounding=rounding) < 0:
    #                 # TDE FIXME: shoudl probably return a move - check for no track key, by the way
    #                 new_move_id = move.split(remaining_qty)
    #                 new_move = self.env['stock.move'].with_context(mail_notrack=True).browse(new_move_id)
    #                 todo_moves |= move
    #                 # Assign move as it was assigned before
    #                 toassign_moves |= new_move
    #
    #         # TDE FIXME: do_only_split does not seem used anymore
    #         if todo_moves and not self.env.context.get('do_only_split'):
    #             todo_moves.action_done()
    #         elif self.env.context.get('do_only_split'):
    #             picking = picking.with_context(split=todo_moves.ids)
    #
    #         picking._create_backorder()
    #     return True

    def action_set_delivered_qty(self, vals):
        for rec in self:
            if rec.sale_id:
                line_id = rec.sale_id.order_line.filtered(
                    lambda s: s.product_id == s.order_id.carrier_id.product_id)
                if line_id:
                    line_id.write({
                        'qty_delivered': vals.get('number_of_packages')
                    })

    def remove_extra_weight_line(self):
        prod_tmpl_id = self.env.ref('base_dhl.extra_weight_product')
        for rec in self:
            line_id = rec.sale_id.order_line.filtered(
                lambda l: l.is_extra_weight)
            if line_id:
                line_id.sudo().write({
                    'qty_delivered': 0.0,
                    'price_unit': 0.0,
                })
            move_line_id = rec.pack_operation_product_ids.filtered(
                lambda a: a.product_id.product_tmpl_id == prod_tmpl_id)
            move_line_id.write({
                'qty_done': 0.0,
                'product_qty': 0.0
            })
            return True

    def set_update_extra_weight_line(self, vals):
        SaleOrderLine = self.env['sale.order.line']
        prod_tmpl_id = self.env.ref('base_dhl.extra_weight_product')
        for rec in self:
            line_id = rec.sale_id.order_line.filtered(
                lambda l: l.is_extra_weight)
            if line_id:
                line_id.sudo().write({
                    'qty_delivered': vals.get('extra_weight'),
                    'product_uom_qty': vals.get('extra_weight')
                })
            else:
                values = {
                    'name': _("Extra Weight B2B"),
                    'product_uom_qty': vals.get('extra_weight'),
                    'product_uom': prod_tmpl_id.uom_id.id,
                    'product_id': prod_tmpl_id.product_variant_id.id,
                    'qty_delivered': vals.get('extra_weight') or 0.0,
                    'price_unit': 0.0,
                    'tax_id': [],
                    'is_extra_weight': True,
                    'order_id': rec.sale_id.id
                }
                line_id = SaleOrderLine.sudo().create(values)
                line_id.product_id_change()
            move_line_id = rec.pack_operation_product_ids.filtered(
                lambda a: a.product_id.product_tmpl_id == prod_tmpl_id)
            move_line_id.write({
                'qty_done': vals.get('extra_weight'),
                'product_qty': vals.get('extra_weight')
            })
            return True

    def remove_extra_dimension_line(self):
        prod_tmpl_id = self.env.ref('base_dhl.extra_dimension_product')
        for rec in self:
            line_id = rec.sale_id.order_line.filtered(
                lambda l: l.is_extra_dimension)
            if line_id:
                line_id.sudo().write({
                    'qty_delivered': 0.0,
                    'price_unit': 0.0,
                })
            move_line_id = rec.pack_operation_product_ids.filtered(
                lambda a: a.product_id.product_tmpl_id == prod_tmpl_id)
            move_line_id.write({
                'qty_done': 0.0,
                'product_qty': 0.0,
            })
            return True

    def set_update_extra_dimension_line(self, vals):
        SaleOrderLine = self.env['sale.order.line']
        prod_tmpl_id = self.env.ref('base_dhl.extra_dimension_product')
        for rec in self:
            line_id = rec.sale_id.order_line.filtered(
                lambda l: l.is_extra_dimension)
            if line_id:
                line_id.sudo().write({
                    'qty_delivered': vals.get('extra_dimension'),
                    'product_uom_qty': vals.get('extra_dimension')
                })
            else:
                values = {
                    'name': _("Extra Dimension B2B"),
                    'product_uom_qty': vals.get('extra_dimension'),
                    'product_uom': prod_tmpl_id.uom_id.id,
                    'product_id': prod_tmpl_id.product_variant_id.id,
                    'qty_delivered': vals.get('extra_dimension') or 0.0,
                    'price_unit': 0.0,
                    'tax_id': [],
                    'is_extra_dimension': True,
                    'order_id': rec.sale_id.id
                }
                line_id = SaleOrderLine.sudo().create(values)
                line_id.product_id_change()
            move_line_id = rec.pack_operation_product_ids.filtered(
                lambda a: a.product_id.product_tmpl_id == prod_tmpl_id)
            move_line_id.write({
                'qty_done': vals.get('extra_dimension'),
                'product_qty': vals.get('extra_dimension')
            })
            return True

    def write(self, vals):
        if 'number_of_packages' in vals:
            self.action_set_delivered_qty(vals)
        if ('is_extra_weight' in vals and vals.get(
                'is_extra_weight')) or 'extra_weight' in vals:
            self.set_update_extra_weight_line(vals)
        if 'is_extra_weight' in vals and not vals.get('is_extra_weight'):
            self.remove_extra_weight_line()
        if ('is_extra_dimension' in vals and vals.get(
                'is_extra_dimension')) or 'extra_dimension' in vals:
            self.set_update_extra_dimension_line(vals)
        if 'is_extra_dimension' in vals and not vals.get('is_extra_dimension'):
            self.remove_extra_dimension_line()
        return super(StockPicking, self).write(vals)


class StockPackOperation(models.Model):
    _inherit = 'stock.move.line'

    @api.model
    def create(self, vals):
        weight_product_id = self.env.ref(
            'base_dhl.extra_weight_product').product_variant_id.id
        dimension_product_id = self.env.ref(
            'base_dhl.extra_dimension_product').product_variant_id.id
        res = super(StockPackOperation, self).create(vals)
        if res.picking_id:
            if res.picking_id.is_extra_weight and res.product_id.id == weight_product_id:
                res.write({
                    'product_qty': res.picking_id.extra_weight,
                    'qty_done': res.picking_id.extra_weight
                })
            if res.picking_id.is_extra_dimension and res.product_id.id == dimension_product_id:
                res.write({
                    'product_qty': res.picking_id.extra_dimension,
                    'qty_done': res.picking_id.extra_dimension
                })
        return res
