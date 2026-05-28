# -*- coding: utf-8 -*-
from odoo import models, fields, api

class Motivo(models.Model):
    _name = 'gestion_faltas.motivo'
    _description = 'Motivo / Tipo de falta'

    code = fields.Char(string='Código', required=True)  
    name = fields.Text(string='Motivo', required=True)   
    dias_castigo=fields.Char(string='escriba dias de castigo aprox como referencia a la falta Ej: 3-10')

    @api.model
    def create(self, vals):
        if 'name' in vals and vals['name']:
            vals['name'] = vals['name'].lower()
        return super(Motivo, self).create(vals)

    def write(self, vals):
        if 'name' in vals and vals['name']:
            vals['name'] = vals['name'].lower()
        return super(Motivo, self).write(vals)

    _sql_constraints = [
        ('motivo_code_unique', 'unique(code)', 'El código ya existe.'),
        ('motivo_name_unique', 'unique(name)', 'El motivo ya existe.'),
    ]
