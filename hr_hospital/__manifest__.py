{
    'name': 'Odoo school Hospital',
    'version': '19.0.1.2.0',
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

        'wizard/hr_hospital_reschedule_visit_wizard_view.xml',
        'views/hr_hospital_visit_view.xml',
        'views/hr_hospital_doctor_view.xml',
        'views/hr_hospital_patient_view.xml',
        'views/hr_hospital_contact_person_view.xml',
        'views/hr_hospital_doctor_specialty_views.xml',
        'views/hr_hospital_disease_view.xml',
        'views/hr_hospital_diagnosis_view.xml',
        'views/hr_hospital_doctor_schedule_view.xml',
        'wizard/hr_hospital_mass_reassign_doctor_wizard_view.xml',
        'wizard/hr_hospital_disease_report_wizard_view.xml',
        'wizard/hr_hospital_doctor_schedule_wizard_view.xml',
        'wizard/hr_hospital_patient_card_export_wizard_view.xml',
        'views/hr_hospital_menu.xml',
        'views/res_partner_views.xml',
    ],
    'demo': [
        'demo/res_users_demo.xml',
        'demo/hr_hospital_doctor_specialty_demo.xml',
        'demo/hr_hospital_doctor_demo.xml',
        'demo/hr_hospital_patient_demo.xml',
        'demo/hr_hospital_disease_demo.xml',
        'demo/hr_hospital_visit_demo.xml',
        'demo/hr_hospital_diagnosis_demo.xml',
        'demo/hr_hospital_schedule_demo.xml',
        # 'demo/hr_hospital_patient_doctor_history_demo.xml',
        # 'demo/res_partner_demo.xml',
        # # 'demo/hr_hospital_contact_person_demo.xml',
    ],

    'installable': True,
    'application': True,
    'auto_install': False,

    'images': [
        'static/description/icon.png'
    ],
}
