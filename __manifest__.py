# -*- coding: utf-8 -*-
{
    "name": "Ease",
    "summary": "Short (1 phrase/line) summary of the module's purpose",
    "description": """
This apps otomation external apps Intergration (Tokopedia,Shoppe, & Blibli)
    """,
    "author": "Ease Corporation",
    "website": "https://www.yourcompany.com",
    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    "category": "Uncategorized",
    "version": "0.1",
    # any module necessary for this one to work correctly
    "depends": [
        "base",
        "website_sale",  # Karena menggunakan e-commerce
        "product",  # Untuk product.template
    ],
    # always loaded
    "data": [
        "security/ir.model.access.csv",
        "views/views.xml",
        "views/templates.xml",
    ],
    # only loaded in demonstration mode
    # 'demo': [
    #     'demo/demo.xml',
    # ],
    "installable": True,
    "application": True,
}
