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

from datetime import date
from odoo import models, fields, _
from woocommerce import API
import requests
import base64
import logging
import numpy as np

from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)


class WooWizard(models.TransientModel):
    _name = 'woo.wizard'
    _description = "Woo Operation Wizard"

    name = fields.Char(string="Instance Name", readonly=True)
    consumer_key = fields.Char(string="Consumer Key", readonly=True)
    consumer_secret = fields.Char(string="Consumer Secret", readonly=True)
    store_url = fields.Char(string="Store URL", readonly=True)
    product_check = fields.Boolean(string="Products")
    customer_check = fields.Boolean(string="Customers")
    order_check = fields.Boolean(string="Orders")
    currency = fields.Char("Currency", readonly=True)

    def get_api(self):
        """
        It returns the API object for operations
        """

        wcapi = API(
            url="" + self.store_url + "/index.php/",  # Your store URL
            consumer_key=self.consumer_key,  # Your consumer key
            consumer_secret=self.consumer_secret,  # Your consumer secret
            wp_api=True,  # Enable the WP REST API integration
            version="wc/v3",  # WooCommerce WP REST API version
            timeout=500,
        )
        return wcapi

    def image_upload(self, image):
        """
        Uploads image into imgur API for getting product image in the woo.
        """

        url = "https://api.imgur.com/3/image"

        payload = {'image': image}
        files = [

        ]
        headers = {
            'Authorization': 'Client-ID 3a0493870db422c'
        }

        response = requests.request("POST", url, headers=headers, data=payload, files=files)

        result = response.json()

        data = result['data']
        if 'link' in data:
            link = data['link']
        else:
            raise ValidationError(_(data['error']['message']))
        return link

    def get_woo_import(self):
        """
        function for importing data from woocommerce
        database

        """
        currency_name = self.env.company.currency_id.name
        currency_cal = requests.get('https://api.exchangerate-api.com/v4/latest/'+currency_name+'').json()
        currency_rates = currency_cal['rates']

        if self.product_check:
            active_id = self._context.get('active_id')
            wcapi = self.get_api()
            res = wcapi.get("products/categories", params={"per_page": 100}).json()

            category_ids = self.env['product.category'].search([])
            woo_ids = category_ids.mapped('woo_id')
            for recd in res:
                if str(recd.get('id')) not in woo_ids:
                    vals_cat = {
                        'name': recd.get('name'),
                        'woo_id': recd.get('id'),
                        'instance_id': active_id
                    }
                    self.env['product.category'].create(vals_cat)
            for recd in res:
                if recd.get('parent') != 0:
                    category_id = self.env['product.category'].search([('woo_id', '=', recd.get('id'))])
                    parent_id = self.env['product.category'].search([('woo_id', '=', recd.get('parent'))])
                    category_id.write({
                        'parent_id': parent_id.id,
                    })
            wcapi_attr = self.get_api()
            res = wcapi_attr.get("products/attributes", params={"per_page": 100}).json()
            attribute_ids = self.env['product.attribute'].search([])
            woo_ids = attribute_ids.mapped('woo_id')
            for recd in res:
                #
                if str(recd.get('id')) not in woo_ids:
                    vals_attr = {
                        'name': recd.get('name'),
                        'woo_id': recd.get('id'),
                        'instance_id': active_id,
                        'display_type': 'select',
                    }
                    self.env['product.attribute'].create(vals_attr)
            wcapi = self.get_api()

            res = wcapi.get("products", params={"per_page": 100}).json()

            product_ids = self.env['product.template'].search([])
            woo_ids = product_ids.mapped('woo_id')

            if 'extra_charge' not in woo_ids:
                self.env['product.template'].create({
                    'name': 'Extra Charges',
                    'type': 'service',
                    'taxes_id': False,
                    'woo_id': 'extra_charge',
                    'instance_id': active_id
                })
            for recd in res:
                attr_info = []

                for attr in recd.get('attributes'):

                    var_info = []
                    attr_id = self.env['product.attribute'].search(
                        [('woo_id', '=', attr.get('id')), ('instance_id', '=', active_id)])
                    color_info = []
                    if attr.get('variation'):
                        for var in attr.get('options'):

                            color_info.append(var)
                            if var not in attr_id.value_ids.mapped('name'):
                                vals_line = (0, 0, {
                                    'name': var
                                })
                                var_info.append(vals_line)

                        if var_info:
                            attr_id.write({
                                'value_ids': var_info
                            })

                        if attr_id.value_ids:
                            vals_line = (0, 0, {
                                'attribute_id': attr_id.id,
                                'value_ids': attr_id.value_ids.filtered(lambda r: r.name in color_info)
                            })
                            attr_info.append(vals_line)

                if str(recd.get('id')) not in woo_ids:
                    categ_id = recd.get('categories')[len(recd.get('categories')) - 1].get('id')
                    category_id = self.env['product.category'].search([('woo_id', '=', categ_id)])
                    list_price = round(float(recd.get('price')) * currency_rates[self.currency], 4)
                    if recd.get('images'):
                        output_img = base64.b64encode(requests.get(recd['images'][0].get('src')).content)
                        vals = {
                            'name': recd.get('name'),
                            'list_price': list_price,
                            'type': "product",
                            'image_1920': output_img,
                            'taxes_id': False,
                            'woo_id': recd.get('id'),
                            'instance_id': active_id,
                            'categ_id': category_id.id,
                            'attribute_line_ids': attr_info if attr_info else False,
                        }
                        prd_id = self.env['product.template'].create(vals)

                        if recd.get('manage_stock'):

                            product_id = self.env['product.product'].search([('product_tmpl_id', '=', prd_id.id)])

                            location_id = self.env.ref('stock.stock_location_stock')
                            if len(prd_id.product_variant_ids) == 1:
                                stock_vals = {
                                    'location_id': location_id.id,
                                    'inventory_quantity': recd.get('stock_quantity'),
                                    'quantity': recd.get('stock_quantity'),
                                    'product_id': product_id.id,
                                    'on_hand': True
                                }
                                stock_id = self.env['stock.quant'].sudo().create(stock_vals)

                        for var_id in prd_id.product_variant_ids:
                            prd_opt = var_id.product_template_attribute_value_ids.mapped('name')
                            wcapi = self.get_api()
                            result = wcapi.get("products/" + str(recd.get('id')) + "/variations").json()

                            for dit in result:
                                woo_price = round(float(dit.get('price')) * currency_rates[self.currency], 4)
                                options = [i['option'] for i in dit.get('attributes')]

                                if set(prd_opt) == set(options):

                                    prd_id.write({
                                        'woo_variant_check': True
                                    })
                                    if dit.get('image'):
                                        output_img = base64.b64encode(requests.get(dit['image'].get('src')).content)
                                    var_id.write({
                                        'woo_var_id': dit.get('id'),
                                        'woo_price': woo_price,
                                        'image_1920': output_img
                                    })
                                    if dit.get('manage_stock'):
                                        location_id = self.env.ref('stock.stock_location_stock')
                                        stock_vals = {
                                            'location_id': location_id.id,
                                            'inventory_quantity': dit.get('stock_quantity'),
                                            'quantity': dit.get('stock_quantity'),
                                            'product_id': var_id.id,
                                            'on_hand': True
                                        }
                                        stock_id = self.env['stock.quant'].sudo().create(stock_vals)

                    else:
                        list_price = round(float(recd.get('price')) * currency_rates[self.currency], 4) if recd.get('price') else 0
                        vals = {
                            'name': recd.get('name'),
                            'list_price': list_price,
                            'type': "product",
                            'woo_id': recd.get('id'),
                            'taxes_id': False,
                            'instance_id': active_id,
                            'categ_id': category_id.id,

                        }
                        prd_id = self.env['product.template'].create(vals)

                        if recd.get('manage_stock'):
                            product_id = self.env['product.product'].search([('product_tmpl_id', '=', prd_id.id)])

                            location_id = self.env.ref('stock.stock_location_stock')
                            stock_vals = {
                                'location_id': location_id.id,
                                'inventory_quantity': recd.get('stock_quantity'),
                                'product_id': product_id.id,
                                'quantity': recd.get('stock_quantity'),
                                'on_hand': True
                            }
                            stock_id = self.env['stock.quant'].sudo().create(stock_vals)

        if self.customer_check:
            wcapi = self.get_api()
            res = wcapi.get("customers", params={"per_page": 100}).json()

            customer_ids = self.env['res.partner'].search([])
            woo_ids = customer_ids.mapped('woo_id')

            active_id = self._context.get('active_id')
            for recd in res:
                if str(recd.get('id')) not in woo_ids:
                    if recd['billing'].get('country') and recd['billing'].get('state') and \
                            recd['shipping'].get('country') and recd['shipping'].get('state'):
                        country_id = self.env['res.country'].search([('code', '=', recd['billing'].get('country'))])
                        state_id = self.env['res.country.state'].search([('code', '=', recd['billing'].get('state')),
                                                                         ('country_id', '=', country_id.id)])
                        vals = {
                            'company_type': "person",
                            'name': recd.get('first_name') + " " + recd.get('last_name'),
                            'street': recd['billing'].get('address_1'),
                            'city': recd['billing'].get('city'),
                            'state_id': state_id.id,
                            'zip': recd['billing'].get('postcode'),
                            'country_id': country_id.id,
                            'phone': recd['billing'].get('phone'),
                            'email': recd.get('email'),
                            'woo_id': recd.get('id'),
                            'woo_user_name': recd.get('username'),
                            'instance_id': active_id
                        }
                        contact = self.env['res.partner'].create(vals)

                    else:
                        vals = {
                            'company_type': "person",
                            'name': recd.get('first_name') + " " + recd.get('last_name'),
                            'email': recd.get('email'),
                            'woo_id': recd.get('id'),
                            'woo_user_name': recd.get('username'),
                            'instance_id': active_id
                        }
                        contact = self.env['res.partner'].create(vals)

        if self.order_check:
            active_id = self._context.get('active_id')
            wcapi = self.get_api()
            res = wcapi.get("taxes", params={"per_page": 100}).json()

            tax_ids = self.env['account.tax'].search([])
            woo_ids = tax_ids.mapped('woo_id')
            for recd in res:
                if str(recd.get('id')) not in woo_ids:
                    vals_tax = {
                        'name': recd.get('name'),
                        'amount': recd.get('rate'),
                        'woo_id': recd.get('id'),
                        'instance_id': active_id,
                        'tax_class': recd.get('class'),
                        'description': recd.get('rate').split('.')[0] + ".00%"
                    }

                    self.env['account.tax'].create(vals_tax)
            wcapi = self.get_api()
            res = wcapi.get("orders", params={"per_page": 100}).json()

            sale_order_ids = self.env['sale.order'].search([('state', '!=', 'cancel')])
            woo_ids = sale_order_ids.mapped('woo_id')
            service_id = self.env['product.product'].search([('woo_id', '=', 'extra_charge')])
            for recd in res:
                if str(recd.get('id')) not in woo_ids and recd.get('status') != 'cancelled':
                    partner_id = self.env['res.partner'].search([('woo_id', '=', recd.get('customer_id'))])

                    if not partner_id:
                        if recd['billing'].get('country') and recd['billing'].get('state'):
                            country_id = self.env['res.country'].search([('code', '=', recd['billing'].get('country'))])
                            state_id = self.env['res.country.state'].search(
                                [('code', '=', recd['billing'].get('state')),
                                 ('country_id', '=', country_id.id)])
                            vals = {
                                'company_type': "person",
                                'name': recd['billing'].get('first_name') + " " + recd['billing'].get('last_name'),
                                'street': recd['billing'].get('address_1'),
                                'city': recd['billing'].get('city'),
                                'state_id': state_id.id,
                                'zip': recd['billing'].get('postcode'),
                                'country_id': country_id.id,
                                'phone': recd['billing'].get('phone'),
                                'email': recd['billing'].get('email'),
                                'woo_id': recd.get('customer_id'),
                                'instance_id': active_id
                            }
                            contact = self.env['res.partner'].create(vals)

                        else:
                            vals = {
                                'company_type': "person",
                                'name': recd['billing'].get('first_name') + " " + recd['billing'].get('last_name'),
                                'email': recd['billing'].get('email'),
                                'woo_id': recd.get('customer_id'),
                                'instance_id': active_id
                            }
                            contact = self.env['res.partner'].create(vals)

                        partner_id = contact
                    order_info = []
                    coupon_info = []
                    for coupon in recd.get('coupon_lines'):
                        discount_amount = round(int(coupon.get('discount')) * currency_rates[self.currency], 4)
                        tax_discount = round(int(coupon.get('discount_tax')) * currency_rates[self.currency], 4)
                        coupon_vals = (0, 0, {
                            'woo_coupon_id': coupon.get('id'),
                            'coupon_code': coupon.get('code'),
                            'discount_amount': discount_amount,
                            'tax_discount': tax_discount
                        })
                        coupon_info.append(coupon_vals)
                    for line in recd.get('line_items'):
                        if line.get('variation_id'):
                            product_id = self.env['product.product'].search([('woo_id', '=', line.get('product_id')),
                                                                             ('woo_var_id', '=',
                                                                              line.get('variation_id'))])
                        else:
                            product_id = self.env['product.product'].search([('woo_id', '=', line.get('product_id'))])

                        ids = []
                        if line.get('taxes'):
                            for tax in line.get('taxes'):
                                if tax.get('total') != '':
                                    ids.append(tax.get('id'))
                        line_tax_ids = self.env['account.tax'].search([('woo_id', 'in', ids)])
                        price_unit = round(float(line.get('price')) * currency_rates[self.currency], 4)
                        vals_line = (0, 0, {
                            'product_id': product_id.id,
                            'name': product_id.description if product_id.description else product_id.name,
                            'product_uom_qty': line.get('quantity'),
                            'price_unit': price_unit,
                            'tax_id': line_tax_ids if line_tax_ids else False
                        })
                        order_info.append(vals_line)
                    if recd.get('shipping_lines'):
                        for line in recd.get('shipping_lines'):
                            ids = []
                            if line.get('taxes'):
                                for tax in line.get('taxes'):
                                    if tax.get('total') != '':
                                        ids.append(tax.get('id'))
                            line_tax_ids = self.env['account.tax'].search([('woo_id', 'in', ids)])
                            price_unit = round(int(line.get('total')) * currency_rates[self.currency], 4)
                            if float(line.get('total')) > 0:
                                vals_line = (0, 0, {
                                    'product_id': service_id.id,
                                    'name': "Shipping : " + line.get('method_title'),
                                    'price_unit': price_unit,
                                    'tax_id': line_tax_ids if line_tax_ids else False
                                })
                                order_info.append(vals_line)
                    if recd.get('fee_lines'):
                        for line in recd.get('fee_lines'):
                            ids = []
                            if line.get('taxes'):
                                for tax in line.get('taxes'):
                                    if tax.get('total') != '':
                                        ids.append(tax.get('id'))
                            line_tax_ids = self.env['account.tax'].search([('woo_id', 'in', ids)])
                            price_unit = round(int(line.get('total')) * currency_rates[self.currency], 4)
                            if float(line.get('total')) > 0:
                                vals_line = (0, 0, {
                                    'product_id': service_id.id,
                                    'name': line.get('name'),
                                    'price_unit': price_unit,
                                    'tax_id': line_tax_ids if line_tax_ids else False
                                })
                                order_info.append(vals_line)

                    vals = {
                        'partner_id': partner_id.id,
                        'order_line': order_info,
                        'woo_id': recd.get('id'),
                        'woo_order_key': recd.get('order_key'),
                        'instance_id': active_id,
                        'woo_order_status': recd.get('status'),
                        'woo_coupon_ids': coupon_info,
                        'state': 'sale'
                    }
                    sale_id = self.env['sale.order'].create(vals)
                    if sale_id:
                        for picking in sale_id.picking_ids:
                            button_details = picking.button_validate()
                            transfer_id = self.env['stock.immediate.transfer'].search(
                                [('id', '=', button_details.get('res_id'))])
                            transfer_id.process()

    def get_woo_export(self):
        """
        function for Exporting data to woocommerce
        database

        """
        currency_name = self.env.company.currency_id.name
        currency_cal = requests.get('https://api.exchangerate-api.com/v4/latest/'+currency_name+'').json()
        currency_rates = currency_cal['rates']
        if self.product_check:
            active_id = self._context.get('active_id')
            wcapi = self.get_api()
            category_ids = self.env['product.category'].search([('woo_id', '=', False)])

            for recd in category_ids:
                if not recd.parent_id:
                    data = {
                        "name": recd.name,
                    }
                    cat_res = wcapi.post("products/categories", data).json()

                    recd.woo_id = cat_res.get('id')
                    recd.instance_id = active_id

            for recd in category_ids:
                if recd.parent_id:
                    parent_id = self.env['product.category'].search([('id', '=', recd.parent_id.id)])
                    data = {
                        "name": recd.name,
                        "parent": parent_id.woo_id
                    }
                    cat_res = wcapi.post("products/categories", data).json()

                    recd.woo_id = cat_res.get('id')
                    recd.instance_id = active_id
            wcapi = self.get_api()
            attribute_ids = self.env['product.attribute'].search([('woo_id', '=', False)])
            for recd in attribute_ids:
                data = {
                    "name": recd.name,
                    "slug": recd.name,
                    "type": "select",
                    "order_by": "menu_order",
                    "has_archives": True
                }
                att_res = wcapi.post("products/attributes", data).json()
                recd.woo_id = att_res.get('id')
                recd.instance_id = active_id

            products = self.env['product.template'].search([('woo_id', '=', False), ('type', '=', 'product')])

            sl_no = 0
            _logger.info("Products %s", products)
            for recd in products:
                att_id = []
                sl_no += 1
                image_url = False
                product = self.env['product.product'].search([('product_tmpl_id', '=', recd.id)])

                stock_check = False
                stock_qty = 0
                if len(recd.product_variant_ids) == 1 and product.stock_quant_ids:
                    stock_check = True
                    stock_qty = recd.qty_available
                if recd.image_1920:
                    image = base64.decodebytes(recd.image_1920)
                    image_url = self.image_upload(image)

                for att in recd.attribute_line_ids:
                    var_info = []
                    for var in att.value_ids:
                        var_info.append(var.name)
                    att_data = {
                        'id': att.attribute_id.woo_id,
                        'visible': True,
                        'variation': True,
                        'options': var_info
                    }
                    att_id.append(att_data)

                if att_id and recd.image_1920:
                    wcapi = self.get_api()
                    regular_price = round(currency_rates[self.currency] * recd.list_price, 4) if recd.list_price else 0
                    data = {
                        "name": recd.name,
                        "type": "variable",
                        "regular_price": str(regular_price),
                        "description": "",
                        "manage_stock": stock_check,
                        "stock_quantity": stock_qty,
                        "short_description": "",
                        "categories": [
                            {
                                'id': recd.categ_id.woo_id
                            }
                        ],
                        "attributes": att_id,
                        "images": [
                            {
                                "src": image_url
                            },
                        ],
                    }

                    res = wcapi.post("products", data).json()

                    _logger.info("Variant With Image %s", res)
                    recd.woo_id = res.get('id')
                    recd.instance_id = active_id
                    recd.woo_variant_check = True
                    wcapi = self.get_api()

                    for var in recd.product_variant_ids:

                        opt_info = []
                        for color in var.product_template_attribute_value_ids:
                            for att_color in att_id:
                                for i in range(len(att_color['options'])):

                                    if att_color['options'][i] == color.name:
                                        att_vals = {
                                            "id": int(att_color['id']),
                                            "option": color.name
                                        }
                                        opt_info.append(att_vals)
                        if var.image_1920:
                            image = base64.decodebytes(var.image_1920)
                            image_url = self.image_upload(image)

                        else:
                            image = False
                        today = date.today()

                        stock_qty = 0
                        stock_check = False
                        if var.qty_available:
                            stock_check = True
                            stock_qty = var.qty_available
                        regular_price = round(currency_rates[self.currency] * var.lst_price, 4)
                        data = {
                            "regular_price": str(regular_price),
                            "attributes": opt_info,
                            "image": {
                                "src": image_url
                            },
                            "manage_stock": stock_check,
                            "stock_quantity": stock_qty

                        }

                        var_res = wcapi.post("products/" + str(res.get('id')) + "/variations", data).json()

                        var.woo_var_id = var_res.get('id')
                if att_id and not recd.image_1920:
                    wcapi = self.get_api()
                    regular_price = round(currency_rates[self.currency] * recd.list_price, 4) if recd.list_price else 0
                    data = {
                        "name": recd.name,
                        "type": "variable",
                        "regular_price": str(regular_price),
                        "description": "",
                        "short_description": "",
                        "manage_stock": stock_check,
                        "stock_quantity": stock_qty,
                        "categories": [
                            {
                                'id': recd.categ_id.woo_id
                            }
                        ],
                        "attributes": att_id,

                    }

                    res = wcapi.post("products", data).json()
                    _logger.info("Variant With out Image %s", res)

                    recd.woo_id = res.get('id')
                    recd.instance_id = active_id
                    recd.woo_variant_check = True
                    wcapi = self.get_api()

                    for var in recd.product_variant_ids:

                        opt_info = []
                        stock_qty = 0
                        stock_check = False
                        if var.qty_available:
                            stock_check = True
                            stock_qty = var.qty_available
                        for color in var.product_template_attribute_value_ids:
                            for att_color in att_id:
                                for i in range(len(att_color['options'])):

                                    if att_color['options'][i] == color.name:
                                        att_vals = {
                                            "id": int(att_color['id']),
                                            "option": color.name
                                        }
                                        opt_info.append(att_vals)
                        regular_price = round(currency_rates[self.currency] * var.lst_price, 4)
                        data = {
                            "regular_price": str(regular_price),
                            "attributes": opt_info,
                            "manage_stock": stock_check,
                            "stock_quantity": stock_qty,
                        }

                        var_res = wcapi.post("products/" + str(res.get('id')) + "/variations", data).json()

                        var.woo_var_id = var_res.get('id')
                if not att_id and recd.image_1920:
                    wcapi = self.get_api()
                    regular_price = round(currency_rates[self.currency] * recd.list_price, 4) if recd.list_price else 0
                    data = {
                        "name": recd.name,
                        "type": "simple",
                        "regular_price": str(regular_price),
                        "description": "",
                        "short_description": "",
                        "manage_stock": stock_check,
                        "stock_quantity": stock_qty,
                        "categories": [
                            {
                                'id': recd.categ_id.woo_id
                            }
                        ],
                        "images": [
                            {
                                "src": image_url
                            },
                        ],
                    }

                    res = wcapi.post("products", data).json()
                    _logger.info(" no Variant With Image %s", res)
                    recd.woo_id = res.get('id')
                    recd.instance_id = active_id
                if not recd.image_1920 and not att_id:
                    wcapi = self.get_api()
                    regular_price = round(currency_rates[self.currency] * recd.list_price, 4) if recd.list_price else 0
                    data = {
                        "name": recd.name,
                        "type": "simple",
                        "regular_price": str(regular_price),
                        "description": "",
                        "short_description": "",
                        "manage_stock": stock_check,
                        "stock_quantity": stock_qty,
                        "categories": [
                            {
                                'id': recd.categ_id.woo_id
                            }
                        ],
                    }

                    res = wcapi.post("products", data).json()
                    _logger.info("no Variant With no Image %s", res)

                    recd.woo_id = res.get('id')
                    recd.instance_id = active_id
        if self.customer_check:
            active_id = self._context.get('active_id')
            wcapi = self.get_api()
            customer_ids = self.env['res.partner'].search([('woo_id', '=', False), ('is_company', '=', False),
                                                           ('email', '!=', False)])
            for recd in customer_ids:
                name = recd.name.split(' ')
                username = recd.email.split('@')
                data = {
                    "email": recd.email,
                    "first_name": name[0],
                    "last_name": name[1] if len(name) > 1 else "",
                    "username": username[0],
                    "billing": {
                        "first_name": name[0],
                        "last_name": name[1] if len(name) > 1 else "",
                        "company": "",
                        "address_1": recd.street if recd.street else "",
                        "address_2": "",
                        "city": recd.city if recd.city else "",
                        "state": recd.state_id.code if recd.state_id else "",
                        "postcode": recd.zip if recd.zip else "",
                        "country": recd.country_id.code if recd.country_id else "",
                        "email": recd.email if recd.email else "",
                        "phone": recd.phone if recd.phone else ""
                    },
                    "shipping": {
                        "first_name": name[0],
                        "last_name": name[1] if len(name) > 1 else "",
                        "company": "",
                        "address_1": recd.street if recd.street else "",
                        "address_2": "",
                        "city": recd.city if recd.city else "",
                        "state": recd.state_id.code if recd.state_id else "",
                        "postcode": recd.zip if recd.zip else "",
                        "country": recd.country_id.code if recd.country_id else ""
                    }
                }
                res = wcapi.post('customers', data).json()
                recd.woo_id = res.get('id')
                recd.instance_id = active_id

    def sync_details(self):
        """
        Function Used for syncing woo details into odoo.
        """
        currency_name = self.env.company.currency_id.name
        currency_cal = requests.get('https://api.exchangerate-api.com/v4/latest/' + currency_name + '').json()
        currency_rates = currency_cal['rates']
        active_id = self._context.get('active_id')
        wcapi = self.get_api()
        res = wcapi.get("orders", params={"per_page": 100}).json()

        for order in res:

            if order.get('status') == 'cancelled':
                order_id = self.env['sale.order'].search([('woo_id', '=', order.get('id')),
                                                          ('instance_id', '=', active_id), ('state', '!=', 'cancel')])

                order_id.state = 'cancel'
                order_id.woo_order_status = order.get('status')
                for picking in order_id.picking_ids:

                    for move in picking.move_line_ids_without_package:
                        move_line = self.env['stock.move'].create({
                            'name': "Product Move",
                            'product_id': move.product_id.id,
                            'product_uom': move.product_uom_id.id,
                            'product_uom_qty': move.qty_done,
                            'location_id': move.location_dest_id.id,
                            'location_dest_id': move.location_id.id,
                            'picking_id': picking.id,
                            'quantity_done': move.qty_done,
                            'move_line_ids': [(0, 0, {
                                'product_id': move.product_id.id,
                                'lot_id': move.lot_id.id,
                                'qty_done': move.qty_done,
                                'product_uom_id': move.product_uom_id.id,
                                'location_id': move.location_dest_id.id,
                                'location_dest_id': move.location_id.id
                            })]
                        })

                        picking.action_confirm()
                        picking.action_assign()
                        button_details = picking.button_validate()
                        transfer_id = self.env['stock.immediate.transfer'].search(
                            [('id', '=', button_details.get('res_id'))])

                        transfer_id.process()
            if order.get('status') == 'completed':

                order_id = self.env['sale.order'].search([('woo_id', '=', order.get('id')),
                                                          ('instance_id', '=', active_id),
                                                          ('state', '!=', 'cancel'),
                                                          ('woo_order_status', '!=', 'completed')])

                for line in order_id.order_line:
                    line.qty_invoiced = line.product_uom_qty
            sale_id = self.env['sale.order'].search([('woo_id', '=', order.get('id')), ('state', '!=', 'cancel')])
            sale_id.woo_order_status = order.get('status')
        res_prd = wcapi.get("Products", params={"per_page": 100}).json()

        woo_ids = []
        for prd in res_prd:
            woo_ids.append(str(prd.get('id')))

            product_id = self.env['product.template'].search([('woo_id', '=', prd.get('id')),
                                                              ('instance_id', '=', active_id)])
            list_price = float(prd.get('price')) * currency_rates[self.currency]
            list_price = round(list_price, 4)
            product_id.list_price = list_price
            if prd.get('variations'):
                woo_var_ids = [int(i.woo_var_id) for i in product_id.product_variant_ids]

                res_var = wcapi.get("products/" + str(prd.get('id')) + "/variations").json()
                for var in res_var:
                    woo_var_ids.append(var.get('id'))
                    variant_id = self.env['product.product'].search([('woo_var_id', '=', var.get('id')),
                                                                     ('instance_id', '=', active_id)])
                    woo_price = round(float(var.get('price')) * currency_rates[self.currency], 4)
                    variant_id.write({
                        'woo_price': woo_price
                    })
                    if var.get('manage_stock') and variant_id:
                        if variant_id.qty_available != var.get('stock_quantity'):
                            qty_needed = var.get('stock_quantity') - variant_id.qty_available

                            location_id = self.env.ref('stock.stock_location_stock')
                            stock_vals = {
                                'location_id': location_id.id,
                                'inventory_quantity': qty_needed,
                                'quantity': qty_needed,
                                'product_id': variant_id.id,
                                'on_hand': True
                            }
                            stock_id = self.env['stock.quant'].sudo().create(stock_vals)

            if prd.get('manage_stock') and not prd.get('variations'):

                if prd.get('stock_quantity') != product_id.qty_available and len(
                        product_id.product_variant_ids) == 1:
                    var_id = self.env['product.product'].search([('product_tmpl_id', '=', product_id.id)])
                    qty_needed = prd.get('stock_quantity') - product_id.qty_available

                    location_id = self.env.ref('stock.stock_location_stock')
                    stock_vals = {
                        'location_id': location_id.id,
                        'inventory_quantity': qty_needed,
                        'quantity': qty_needed,
                        'product_id': var_id.id,
                        'on_hand': True
                    }
                    stock_id = self.env['stock.quant'].sudo().create(stock_vals)

        product_ids = self.env['product.template'].search([])
        prd_woo_ids = product_ids.mapped('woo_id')
        upd_woo_ids = []
        for i in prd_woo_ids:
            if i not in [False, 'extra_charge']:
                upd_woo_ids.append(i)
        diff_list = np.setdiff1d(upd_woo_ids, woo_ids)
        diff_list = list(diff_list)

        for d in diff_list:
            product_id = self.env['product.template'].search([('woo_id', '=', d),
                                                              ('instance_id', '=', active_id)])
            product_id.active = False
        cus_res = wcapi.get("customers", params={"per_page": 100}).json()
        cus_ids = self.env['res.partner'].search([])
        cus_woo_ids = cus_ids.filtered(lambda x: x.woo_id).mapped('woo_id')
        cus_woo_id = []
        for cus in cus_res:
            cus_woo_id.append(str(cus.get('id')))
        diff_list = np.setdiff1d(cus_woo_ids, cus_woo_id)
        diff_list = list(diff_list)

        for d in diff_list:
            customer_id = self.env['res.partner'].search([('woo_id', '=', d),
                                                          ('instance_id', '=', active_id)])
            customer_id.active = False

