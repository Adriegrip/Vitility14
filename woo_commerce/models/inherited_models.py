# -*- coding: utf-8 -*-
######################################################################################
#
#    Cybrosys Technologies Pvt. Ltd.
#
#    Copyright (C) 2020-TODAY Cybrosys Technologies(<https://www.cybrosys.com>).
#    Author: Noushid Khan (odoo@cybrosys.com)
#
#    This program is under the terms of the Odoo Proprietary License v1.0 (OPL-1)
#    It is forbidden to publish, distribute, sublicense, or sell copies of the Software
#    or modified copies of the Software.
#
#    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
#    IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
#    DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
#    ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
#    DEALINGS IN THE SOFTWARE.
#
########################################################################################

from odoo import models, fields, api


class ProductTemplateInherited(models.Model):
    _inherit = 'product.template'

    woo_id = fields.Char(string="WooCommerce ID", readonly=True)
    instance_id = fields.Many2one('woo.commerce', string="Instance", readonly=True)
    woo_variant_check = fields.Boolean(readonly=True)

    def unlink(self):
        """
        For deleting on both instances.
        """
        for recd in self:
            if recd.woo_id:
                wcapi = recd.instance_id.get_api()
                wcapi.delete("products/" + recd.woo_id + "", params={"force": True}).json()
        return super(ProductTemplateInherited, self).unlink()


class ProductProductInherited(models.Model):
    _inherit = 'product.product'

    woo_price = fields.Float(string="woo price")
    woo_var_id = fields.Char(string="Woo Variant ID", readonly=True)

    def unlink(self):
        """
        For deleting on both instances.
        """
        for recd in self:
            if recd.woo_var_id:
                wcapi = recd.product_tmpl_id.instance_id.get_api()
                wcapi.delete("products/" + recd.product_tmpl_id.woo_id + "/variations/" + recd.woo_var_id + "",
                             params={"force": True}).json()
        return super(ProductProductInherited, self).unlink()

    @api.depends('list_price', 'price_extra')
    @api.depends_context('uom')
    def _compute_product_lst_price(self):
        """
        function is override for Changing Variant Price
        based on the woo price.

        """
        for recd in self:
            product_id = self.env['product.template'].search([('product_variant_ids', 'in', recd.id)])
            if not product_id.woo_variant_check:
                to_uom = None
                if 'uom' in self._context:
                    to_uom = self.env['uom.uom'].browse(self._context['uom'])

                for product in self:
                    if to_uom:
                        list_price = product.uom_id._compute_price(product.list_price, to_uom)
                    else:
                        list_price = product.list_price
                    product.lst_price = list_price + product.price_extra
            else:
                if recd.woo_price == 0:
                    recd.lst_price = recd.product_tmpl_id.lst_price
                else:
                    recd.lst_price = recd.woo_price


class ResPartnerInherited(models.Model):
    _inherit = 'res.partner'

    woo_id = fields.Char(string="WooCommerce ID", readonly=True)
    woo_user_name = fields.Char(string="User Name", readonly=True)
    instance_id = fields.Many2one('woo.commerce', string="Instance", readonly=True)

    def unlink(self):
        """
        For deleting on both instances.
        """
        for recd in self:
            if recd.woo_id:
                wcapi = recd.instance_id.get_api()
                wcapi.delete("customers/" + str(recd.id),
                             params={"force": True}).json()
        return super(ResPartnerInherited, self).unlink()


class SaleOrderInherit(models.Model):
    _inherit = 'sale.order'

    woo_id = fields.Char(string="WooCommerce ID")
    woo_order_key = fields.Char(string="Order Key", readonly=True)
    instance_id = fields.Many2one('woo.commerce', string="Instance", readonly=True)
    woo_order_status = fields.Char('WooCommerce Order Status', readonly=True)
    state_check = fields.Boolean(compute='state_change')
    woo_coupon_ids = fields.One2many('woo.order.coupons', 'woo_order_id', string="Woo Coupon Details", readonly=True)

    def state_change(self):
        """
        For computing invoiced quantity based on the woo status.
        """
        if self.woo_order_status != 'completed':
            for order in self.order_line:
                order.qty_invoiced = 0
        self.state_check = True


class WooOrderCoupons(models.Model):
    _name = 'woo.order.coupons'
    _description = "Woo Order Coupons"

    woo_coupon_id = fields.Char('Woo ID', readonly=True)
    coupon_code = fields.Char("Coupon Code", readonly=True)
    discount_amount = fields.Float("Discount Amount", readonly=True)
    tax_discount = fields.Float("Tax Discount", readonly=True)
    woo_order_id = fields.Many2one('sale.order')


class AccountTaxInherited(models.Model):
    _inherit = 'account.tax'

    woo_id = fields.Char(string="WooCommerce ID", readonly=True)
    instance_id = fields.Many2one('woo.commerce', string="Instance", readonly=True)
    tax_class = fields.Char(string="Tax Class", readonly=True)


class ProductCategoryInherited(models.Model):
    _inherit = 'product.category'

    woo_id = fields.Char(string="WooCommerce ID", readonly=True)
    instance_id = fields.Many2one('woo.commerce', string="Instance", readonly=True)


class ProductAttributeInherited(models.Model):
    _inherit = 'product.attribute'

    woo_id = fields.Char(string="WooCommerce ID", readonly=True)
    instance_id = fields.Many2one('woo.commerce', string="Instance", readonly=True)
