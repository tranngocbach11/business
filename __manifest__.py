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
    ],
    # 'qweb': ['static/src/xml/*.xml'],
    'installable': True,
    'application': True,
}