{
    'name': 'Business',
    'summary': """Extend the business module""",
    'author': 'BachTN',
    'version': '0.1',
    'category': 'Uncategorized',
    'depends': [
        'base',
        'product',
        'sale',
        'purchase',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/purchase_plus_views.xml',
        'views/sale_plus_views.xml',
    ],
    # 'qweb': ['static/src/xml/*.xml'],
    'installable': True,
    'application': True,
}