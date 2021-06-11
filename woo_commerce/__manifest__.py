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

{
    'name': 'Odoo WooCommerce Connector',
    'version': '14.0.1.0.1',
    'summary': 'Odoo WooCommerce Connector V14',
    'description': 'Odoo WooCommerce Connector V14, WooCommerce, WooCommerce Odoo, WooCommerce Instance Connector, Odoo WooCommerce',
    'category': 'Sales',
    'author': 'Cybrosys Techno Solutions',
    'maintainer': 'Cybrosys Techno Solutions',
    'company': 'Cybrosys Techno Solutions',
    'website': 'https://www.cybrosys.com',
    'depends': [
        'base',
        'stock',
        'sale_management',
        'account',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/woo_commerce.xml',
        'views/product_product.xml',
        'views/res_partner.xml',
        'views/sale_order.xml',
        'views/account_tax.xml',
        'views/product_category.xml',
        'views/product_attribute.xml',
        'wizard/woo_wizard.xml',
    ],
    'images': ['static/description/banner.png'],
    "external_dependencies": {"python": ["WooCommerce", "django"]},
    'license': 'OPL-1',
    'price': 49,
    'currency': 'EUR',
    'installable': True,
    'application': True,
    'auto_install': False,
}
