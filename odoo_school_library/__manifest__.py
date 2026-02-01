{
    'name': 'Odoo school library Bondarchuk',
    'version': '19.0.1.1.0',
    'author': 'Bondarchuk V',
    'category': 'Customizations',
    'website': 'http://www.bondarchuk.com',
    'license': 'OPL-1',

    'depends': [
        'base',
    ],

    'external_dependencies': {
        'python': []
    },

    'data': [

        'security/ir.model.access.csv',

        'views/odoo_school_library_menu.xml',
        'views/odoo_school_library_book_views.xml',
    ],
    'demo': [
        'demo/res_partner_demo.xml',
        'demo/odoo.school.library.book.csv',
    ],

    'installable': True,
    'auto_install': False,

    'images': [
        'static/description/icon.png'
    ],
}
