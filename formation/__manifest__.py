{
    'name':'Formation technique odoo CE v12',
    'version':'1.0',
    'author':'Tokyniaina',
    'website':'http://www.kasia.mg',
    'support':'toky@kasia.mg',
    'license':'AGPL-3',
    'complexity':'easy',
    'sequence':'1',
    'category':'category',
    'description': """
        This is the module to studie odoo
            -modul 1
            -modul 2
            -modul 3
    """,
    'depends':['base','mail','hr'],
    'summary':'formation, odoo12, erp',
    'data':[
       # 'security/ModuleName.xml',
        'security/ir.model.access.csv',
        'views/formation_views.xml',
        'views/menu_views.xml',
        'views/formation_inherit.xml',
    ],
    'demo':[

    ],
    'css':[

    ],
    'price':100.00,
    'currency':'EUR',
    'installable':True,
    'application':True,
}