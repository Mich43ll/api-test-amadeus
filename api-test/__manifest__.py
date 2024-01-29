{
    'name': 'Amadeus API Integration',
    'version': '14.0',
    'summary': 'Integrate Amadeus API to fetch flight data',
    'sequence': 10,
    'description': """Integrate Amadeus API to fetch flight data""",
    'category': 'Tools',
    'website': 'yourwebsite.com',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/amadeus_example_view.xml',
    ],
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}
