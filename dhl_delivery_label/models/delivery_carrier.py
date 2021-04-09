# -*- coding: utf-8 -*-
# Copyright 2017 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


from odoo import models, fields


class DeliveryCarrier(models.Model):
    _inherit = 'delivery.carrier'

    saturday_delivery = fields.Boolean("Saturday Delivery")
    evening_delivery = fields.Boolean("Evening Delivery")
    mailbox_delivery = fields.Boolean("Mailbox Delivery")
    express_delivery = fields.Boolean("Express Delivery")