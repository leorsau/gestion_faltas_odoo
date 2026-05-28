# -*- coding: utf-8 -*-
from odoo import models, fields,api
from odoo.exceptions import ValidationError

class Alumno(models.Model):
    _name = 'gestion_faltas.alumno'
    _description = 'Alumno'

    nombre_completo = fields.Char(
        string='Nombre completo',
        compute='_compute_nombre_completo',
        store=True
    )

    name = fields.Char(string='Nombre', required=True)
    apellido1 = fields.Char(string='Apellido1', required=True)
    apellido2 = fields.Char(string='Apellido2')
    nia = fields.Char(string='nia_alumno',required=True)
    grupo_id = fields.Many2one('gestion_faltas.grupo', string='Grupo',required=True)
    parte_ids = fields.One2many('gestion_faltas.parte','alumno_id', string='Partes del alumno')


    @api.constrains('grupo_id')
    def _check_cambio_grupo(self):
        for rec in self:
            partes_abiertos = self.env['gestion_faltas.parte'].search([
                ('alumno_id', '=', rec.id),
                ('estado', '!=', 'cerrado')
            ])
            if partes_abiertos:
                raise ValidationError("No puedes cambiar de grupo si el alumno tiene partes abiertos o sin cerrar.")

    @api.model
    def create(self, vals):
        if 'name' in vals and vals['name']:
            vals['name'] = vals['name'].lower()
        if 'apellido1' in vals and vals['apellido1']:
            vals['apellido1'] = vals['apellido1'].lower()
        if 'apellido2' in vals and vals['apellido2']:
            vals['apellido2'] = vals['apellido2'].lower()
        return super(Alumno, self).create(vals)

    def write(self, vals):
        if 'name' in vals and vals['name']:
            vals['name'] = vals['name'].lower()
        if 'apellido1' in vals and vals['apellido1']:
            vals['apellido1'] = vals['apellido1'].lower()
        if 'apellido2' in vals and vals['apellido2']:
            vals['apellido2'] = vals['apellido2'].lower()
        return super(Alumno, self).write(vals)
    
    _sql_constraints = [
    ('nia_unique', 'unique(nia)', 'El NIA ya existe para otro alumno.'),
    ]

    @api.depends('name', 'apellido1', 'apellido2')
    def _compute_nombre_completo(self):
        for rec in self:
            ap2 = rec.apellido2 or 'apellido2_NULL'
            rec.nombre_completo = f"{rec.name} {rec.apellido1} {ap2}".strip()

    def name_get(self):
        result = []
        for rec in self:
            result.append((rec.id, rec.nombre_completo))
        return result