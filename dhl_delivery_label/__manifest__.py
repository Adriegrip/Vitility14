# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': "DHL - Print Delivery Label",
    'description': "DHL - Print Delivery Label",
    'author': 'Onestein',
    'website': 'http://www.onestein.eu',
    'category': 'Warehouse',
    'version': '14.0.1.0.0',
    'license': 'AGPL-3',
    'depends': [
        'stock',
        'delivery',
        'base_dhl',
        'partner_street_number',
        'partner_firstname',
    ],
    'data': [
        'views/stock_picking_view.xml',
        'views/delivery_carrier_view.xml',
    ],
}
