# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


from odoo import models, fields


class DeliveryCarrier(models.Model):
    _inherit = 'delivery.carrier'

    saturday_delivery = fields.Boolean("Saturday Delivery")
    evening_delivery = fields.Boolean("Evening Delivery")
