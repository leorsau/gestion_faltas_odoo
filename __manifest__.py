# -*- coding: utf-8 -*-
{
    'name': 'Gestion de faltas',
    'version': '1.0',
    'depends': ['base'],
    'author': 'Lehi',
    'category': 'Education',
    'description': 'Proyecto sistema de gestion de faltas',
    'data': [  
    'security/security.xml',
    'security/ir.model.access.csv',

    'views/parte_views.xml',
    'views/profesor_views.xml',
    'views/alumno_views.xml',
    'views/grupo_views.xml',
    'views/graficas_views.xml',
    'views/menus.xml',

    'data/data.xml',

    'report/report_alumno.xml',
    'report/report_grupo.xml',
                ],
                
    'installable': True,
    'application': True,
}
