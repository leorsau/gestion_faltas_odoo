# -*- coding: utf-8 -*-
from odoo import models, fields, api


class Parte(models.Model):
    _name = 'gestion_faltas.parte'
    _description = 'Parte disciplinario'
    name = fields.Char(string="Nombre", compute="_compute_name", store=True, readonly=True)

    numero_Parte = fields.Integer(string="Nº de parte nuevo = ", readonly=True)

    fecha_Creacion_parte=fields.Date(string="fecha de creación del parte",default=fields.Date.today, readonly=True)

    grupo_id = fields.Many2one('gestion_faltas.grupo', string='Grupo', required=True)
    alumno_id = fields.Many2one('gestion_faltas.alumno', string='Alumno', required=True)
    profesor_id = fields.Many2one('gestion_faltas.profesor',string='Profesor', required=True)
    asignatura_id = fields.Many2one('gestion_faltas.asignatura', string='Asignatura', required=True)
    fecha_hora = fields.Datetime(string='Fecha y hora del incidente', default=fields.Datetime.now, required=True)
    lugar = fields.Many2one('gestion_faltas.lugar',string='Lugar',required=True)
    motivo_id = fields.Many2one('gestion_faltas.motivo', string='Motivo', required=True)
    descripcion = fields.Text(string='Descripción',required=True)
    acciones_inmediatas = fields.Text(string='Acciones inmediatas')
    etapa = fields.Selection(related='grupo_id.etapa', store=True)


    llamada1=fields.Selection(
        [
            ('contesta','Contesta'),
            ('no_contesta','No contesta')
        ]
    )
    llamada2=fields.Selection(
        [
            ('contesta','Contesta'),
            ('no_contesta','No contesta')
        ]
    )

    llamada3=fields.Selection(
        [
            ('contesta','Contesta'),
            ('no_contesta','No contesta')
        ]
    )

    llamada1_fecha = fields.Datetime(string="Fecha llamada 1", readonly=True)
    llamada2_fecha = fields.Datetime(string="Fecha llamada 2", readonly=True)
    llamada3_fecha = fields.Datetime(string="Fecha llamada 3", readonly=True)




    estado = fields.Selection([
        ('pendiente_contactar_padres', 'Pendiente_Contactar'),
        ('contactado_padres', 'Contactado_Padres'),
        ('cerrado', 'Cerrado'),
    ], string='Estado', default='pendiente_contactar_padres')

    observaciones=fields.Text(string='Indique observaciones del caso')

    @api.model
    def create(self, vals):
        ultimo_parte = self.search([], order='numero_Parte desc', limit=1)

        if ultimo_parte:
            vals['numero_Parte'] = ultimo_parte.numero_Parte + 1
        else:
            vals['numero_Parte'] = 1

        return super().create(vals)
    
    @api.onchange('llamada1', 'llamada2', 'llamada3')
    def _onchange_llamadas(self):
        if 'contesta' in [self.llamada1, self.llamada2, self.llamada3]:
            self.estado = 'contactado_padres'
            return {
                'warning': {
                    'title': "Aviso!!",
                    'message': "Has marcado 'contesta'. Recuerda guardar el registro para actualizar el estado del Parte.",
                }
            }    

        elif'no_contesta' in [self.llamada1, self.llamada2, self.llamada3]:
            return {
                'warning': {
                    'title': "Aviso!!",
                    'message': "Has marcado 'No contesta'. Recuerda guardar el parte para que se guarde la hora de la llamada.",
                }
        }
        
        
    def write(self, vals):

        soy_el_boton = vals.get('action_cerrar')
        
        ahora = fields.Datetime.now()

                
        if vals.get('llamada1'):
            vals['llamada1_fecha'] = ahora
        

        if vals.get('llamada2'):
            vals['llamada2_fecha'] = ahora
            

        if vals.get('llamada3'):
            vals['llamada3_fecha'] = ahora

        l1 = vals.get('llamada1', self.llamada1)
        l2 = vals.get('llamada2', self.llamada2)
        l3 = vals.get('llamada3', self.llamada3)



        if soy_el_boton:
            vals['estado'] = 'cerrado'
            del vals['action_cerrar']
        else:
            if 'contesta' in [l1, l2, l3]:
                vals['estado'] = 'contactado_padres'

        return super(Parte, self).write(vals)





    
    def action_cerrar_parte(self):
        for rec in self:
            if rec.estado == 'contactado_padres':
                rec.write({'estado': 'cerrado', 'action_cerrar':True})


    def action_reabrir_parte(self):
        for rec in self:
            if rec.estado == 'cerrado':
                rec.write({'estado': 'pendiente_contactar_padres'})

    
    @api.depends('numero_Parte', 'fecha_Creacion_parte')
    def _compute_name(self):
        for rec in self:
            if rec.numero_Parte and rec.fecha_Creacion_parte:
                rec.name = f"Parte Nº {rec.numero_Parte} – {rec.fecha_Creacion_parte}"
            else:
                rec.name = "Nuevo Parte"







