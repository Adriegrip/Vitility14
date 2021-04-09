# -*- coding: utf-8 -*-
# Copyright 2017 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': "DHL Shipping",
    'description': "DHL Shipping",
    'author': 'BusinessAgilityMasters',
    'website': 'http://www.businessagilitymasters.com',
    'category': 'Warehouse',
    'version': '13.0.1',
    'license': 'AGPL-3',
    'depends': [
        'delivery',
    ],
    'data': [
        'data/delivery_dhl_data.xml',
        'views/delivery_carrier_view.xml',
    ],
}
