# -*- coding: utf-8 -*-
from odoo import models, fields, api

class Lugar(models.Model):
    _name = 'gestion_faltas.lugar'
    _description = 'Lugar de los hechos'

    name = fields.Char(string='Lugar de los hechos Ej: Aula, Pasillo, Patio, Otros', required=True)

    @api.model
    def create(self, vals):
        if 'name' in vals and vals['name']:
            vals['name'] = vals['name'].lower()
        return super(Lugar, self).create(vals)

    def write(self, vals):
        if 'name' in vals and vals['name']:
            vals['name'] = vals['name'].lower()
        return super(Lugar, self).write(vals)

    _sql_constraints = [
        ('lugar_unique', 'unique(name)', 'Este lugar ya existe.'),
    ]