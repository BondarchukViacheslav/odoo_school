{
    'name': 'Odoo school Hospital',
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

        'views/hr_hospital_visit_view.xml',
        'views/hr_hospital_doctor_view.xml',
        'views/hr_hospital_patient_view.xml',
        'views/hr_hospital_disease_view.xml',
        'views/hr_hospital_menu.xml',
    ],
    'demo': [
        'demo/res_partner_demo.xml',
        'demo/hr_hospital_doctor_demo.xml',
        'demo/hr_hospital_patient_demo.xml',
        'demo/hr_hospital_disease_demo.xml',
        'demo/hr_hospital_visit_demo.xml',
    ],

    'installable': True,
    'application': True,
    'auto_install': False,

    'images': [
        'static/description/icon.png'
    ],
}
