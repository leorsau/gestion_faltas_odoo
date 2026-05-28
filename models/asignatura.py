# -*- coding: utf-8 -*-
from odoo import models, fields, api

class Asignatura(models.Model):
    _name = 'gestion_faltas.asignatura'
    _description = 'Asignatura'

    name = fields.Char(string='Asignatura', required=True)

    @api.model
    def create(self, vals):
        if 'name' in vals and vals['name']:
            vals['name'] = vals['name'].lower()
        return super(Asignatura, self).create(vals)

    def write(self, vals):
        if 'name' in vals and vals['name']:
            vals['name'] = vals['name'].lower()
        return super(Asignatura, self).write(vals)

    _sql_constraints = [
    ('asignatura_unique', 'unique(name)', 'Esta asignatura ya existe.'),
    ]