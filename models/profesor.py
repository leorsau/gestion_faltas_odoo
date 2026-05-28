# -*- coding: utf-8 -*-
from odoo import models, fields, api

class Profesor(models.Model):
    _name = 'gestion_faltas.profesor'
    _description = 'Profesor'

    nombre_completo = fields.Char(
        string='Nombre completo',
        compute='_compute_nombre_completo',
        store=True
    )

    name = fields.Char(string='Nombre', required=True)
    apellido1 = fields.Char(string='Apellido1', required=True)
    apellido2 = fields.Char(string='Apellido2', default="sin-apellido2")

    @api.model
    def create(self, vals):
        if 'name' in vals and vals['name']:
            vals['name'] = vals['name'].lower()
        if 'apellido1' in vals and vals['apellido1']:
            vals['apellido1'] = vals['apellido1'].lower()
        if 'apellido2' in vals and vals['apellido2']:
            vals['apellido2'] = vals['apellido2'].lower()
        return super(Profesor, self).create(vals)

    def write(self, vals):
        if 'name' in vals and vals['name']:
            vals['name'] = vals['name'].lower()
        if 'apellido1' in vals and vals['apellido1']:
            vals['apellido1'] = vals['apellido1'].lower()
        if 'apellido2' in vals and vals['apellido2']:
            vals['apellido2'] = vals['apellido2'].lower()
        return super(Profesor, self).write(vals)
        
    _sql_constraints = [
        ('profesor_unique','unique(name, apellido1, apellido2)', 'El nombre del profesor ya existe.'),
    ]


    @api.depends('name', 'apellido1', 'apellido2')
    def _compute_nombre_completo(self):
        for rec in self:
            ap2 = rec.apellido2 or 'sin-apellido2'
            rec.nombre_completo = f"{rec.name} {rec.apellido1} {ap2}".strip()

    def name_get(self):
        result = []
        for rec in self:
            result.append((rec.id, rec.nombre_completo))
        return result