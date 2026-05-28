# -*- coding: utf-8 -*-
from odoo import models, fields, api

class Grupo(models.Model):
    _name = 'gestion_faltas.grupo'
    _description = 'Grupo'

    name = fields.Char(string='Grupo', compute="_compute_name", store=True, readonly=True)

    codigo=fields.Char(string='Código de grupo')
    nombre=fields.Char(string='Nombre del grupo')

    etapa = fields.Selection([
    ('ESO', 'ESO'),
    ('FPB', 'FP Básica'),
    ('CICLOS', 'Ciclos Formativos'),
    ('BACH', 'Bachillerato'),
    ], string='Etapa escolar')

    parte_ids = fields.One2many(
        'gestion_faltas.parte',
        'grupo_id',
        string='Partes del grupo'
    )


    
    _sql_constraints = [
        ('grupo_unique', 'unique(name)', 'Este grupo ya existe.'),
    ]

    
    @api.depends('codigo', 'nombre')
    def _compute_name(self):
        for rec in self:
            if rec.codigo and rec.nombre:
                nombre=rec.nombre.lower()
                rec.name = f"{rec.codigo} – {nombre}"
            else:
                rec.name=False      