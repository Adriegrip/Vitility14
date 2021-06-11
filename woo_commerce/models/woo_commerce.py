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

import requests
from woocommerce import API

from odoo import models, fields, _, api
from odoo.exceptions import UserError
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError


class WooCommerceInstance(models.Model):
    _name = 'woo.commerce'
    _description = "WooCommerce Instances"

    name = fields.Char(string="Instance Name", required=True)
    color = fields.Integer('Color')
    consumer_key = fields.Char(string="Consumer Key", required=True)
    consumer_secret = fields.Char(string="Consumer Secret", required=True)
    store_url = fields.Char(string="Store URL", required=True)
    currency = fields.Char("Currency", readonly=True)

    def get_api(self):
        """
        Returns API object.
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

    def get_wizard(self):
        """
        function used for returning wizard view
        for operations

        """
        set_wcapi = API(
            url="" + self.store_url + "/index.php/wp-json/wc/v3/system_status?",  # Your store URL
            consumer_key=self.consumer_key,  # Your consumer key
            consumer_secret=self.consumer_secret,  # Your consumer secret
            wp_api=True,  # Enable the WP REST API integration
            version="wc/v3",  # WooCommerce WP REST API version
            timeout=500

        )
        set_res = set_wcapi.get("").json()
        currency = set_res['settings'].get('currency')
        self.currency = currency
        return {
            'name': _('Instance Operations'),
            'view_mode': 'form',
            'res_model': 'woo.wizard',
            'domain': [],
            'view_id': False,
            'type': 'ir.actions.act_window',
            'target': 'new',
            'context': {'default_name': self.name,
                        'default_consumer_key': self.consumer_key,
                        'default_consumer_secret': self.consumer_secret,
                        'default_store_url': self.store_url,
                        'default_currency': self.currency
                        }
        }

    def get_instance(self):
        """
        function is used for returning
        current form view of instance.

        """
        return {
            'name': _('Instance'),
            'view_mode': 'form',
            'res_model': 'woo.commerce',
            'res_id': self.id,
            'domain': [],
            'view_id': False,
            'type': 'ir.actions.act_window',
            'target': 'current',

        }

    @api.model
    def create(self, vals_list):
        """
        It checks all the connection validations.
        """
        set_wcapi = API(
            url="" + vals_list['store_url'] + "/index.php/wp-json/wc/v3/system_status?",  # Your store URL
            consumer_key=vals_list['consumer_key'],  # Your consumer key
            consumer_secret=vals_list['consumer_secret'],  # Your consumer secret
            wp_api=True,  # Enable the WP REST API integration
            version="wc/v3",  # WooCommerce WP REST API version
            timeout=500

        )
        validate = URLValidator()

        try:

            validate(set_wcapi.url)


        except ValidationError as exception:

            raise UserError(_("URL Doesn't Exist."))

        try:

            response = requests.get(set_wcapi.url)


        except requests.ConnectionError as exception:

            raise UserError(_("URL Doesn't Exist."))
        if set_wcapi.get("").status_code != 200:
            raise UserError(_("URL Doesn't Exist."))
        set_res = set_wcapi.get("").json()
        if set_res['settings']:
            currency = set_res['settings'].get('currency')
            vals_list['currency'] = currency
        return super(WooCommerceInstance, self).create(vals_list)
