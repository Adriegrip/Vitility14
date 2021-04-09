# -*- coding: utf-8 -*-
# Copyright 2017 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': "DHL - Print Delivery Label",
    'description': "DHL - Print Delivery Label",
    'author': 'Onestein',
    'website': 'http://www.onestein.eu',
    'category': 'Warehouse',
    'version': '10.0.1.0.0',
    'license': 'AGPL-3',
    'depends': [
        'stock',
        'delivery',
        'base_dhl',
    ],
    'data': [
        'views/stock_picking_view.xml',
        'views/delivery_carrier_view.xml',
    ],
}
