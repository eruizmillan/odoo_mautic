# -*- coding: utf-8 -*-
{
    'name': 'Odoo Mautic Connector',
    'version': '12.0',
    'category': 'Construction',
    'author': 'Pragmatic TechSoft Pvt Ltd.',
    'website': "www.pragtech.co.in",
    'summary': '2 way Mautic connector',
    'description': '''
Integration of odoo with mautic two way.
========================================
<keywords>
Odoo Mautic Connector
Mautic
Mautic Odoo
Mautic Connector
Odoo Mautic Integration
Odoo Mautic Integration app
marketing automation app
    ''',
    'depends': ['account', 'sale', 'account_asset', 'sale_management'],
    'data': [
        "views/mainview.xml",
        'views/partner.xml'
    ],
    'images': ['images/Animated-mautic-connector.gif'],
    'license': 'OPL-1',
    'price': 35,
    'currency': 'EUR',
    'installable': True,
    'auto_install': False,
}
