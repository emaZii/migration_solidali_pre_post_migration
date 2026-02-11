
{
    'name': 'PIX - Solidali Base',
    'version': '16.0.1.0.2',
    'category': 'Base Solidali',
    'description': """
                Gestione Base per Solidali - Questo modulo fornisce un sistema integrato per la gestione di servizi di assistenza domiciliare, 
                inclusi contratti, presenze, buste paga, contributi INPS e adempimenti fiscali
                """,
    'author': 'Pixora',
    'website': 'http://www.pixora.it',
    'license': 'Other proprietary',
    'depends': [
        'sale_subscription',
        'hr_recruitment',
        'hr_attendance',
        'hr_payroll',
        'web_refresher',
        'report_py3o',
        'hr_work_entry_contract'
    ],
    'data': [
        'data/product.xml',
        'data/ir_sequence_data.xml',
        'security/solidali_security.xml',
        'security/ir.model.access.csv',
        'views/partner_view.xml',
        'views/solidali_paghe_menuitems.xml',
        'views/reports.xml',
        'views/calendar_event_view.xml',
        'views/solidali_paghe_mav_view.xml',
        'views/solidali_paghe_ra_view.xml',
        'views/solidali_paghe_view.xml',
        'views/solidali_servizio_view.xml',
        'views/solidali_titolo_studio_view.xml',
        'views/hr_employee.xml',
        'views/account_move_view.xml',
        'views/subscription_id_view.xml'
        'config/solidali_paghe_conf_fatture_view.xml',
        'config/solidali_paghe_conf_indennita_view.xml',
        'config/solidali_paghe_conf_ra_view.xml',
        'config/solidali_paghe_conf_retribuzioni_view.xml',
        'config/solidali_paghe_conf_tabella_inps_view.xml',
        'config/solidali_paghe_conf_tessera_asnali_view.xml',
        'config/solidali_paghe_indice_istat_view.xml',
        'wizard/crea_mav.xml',
        'wizard/create_bp.xml',
        'wizard/filtra_abbonamento_wizard.xml',
        'wizard/work_entry_duplicate.xml',
        'views/sale_order_actions.xml'
    ],
    'demo': [
        'data/demo_data.xml'
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
}
