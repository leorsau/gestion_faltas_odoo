from odoo import models, fields, api
from odoo.exceptions import UserError
import base64
import lxml.etree as etree

class XmlImportWizard(models.TransientModel):
    _name='xml.import.wizard'
    _description='wizard para importar datos XML'

    name=fields.Char(string="Nombre")
    file_name=fields.Char(string="Nombre del archivo")
    xml_file=fields.Binary(string="Archivo XML", required=True)

    def action_import_xml(self):
        self.ensure_one()
        if not self.xml_file:
            raise UserError(("Por favor, seleccione un archivo Xml"))
        

        try:
            xml_data=base64.b64decode(self.xml_file)
            root=etree.fromstring(xml_data)

        except Exception as e:
            raise UserError(("Error al leer el archivo XML:%s")%str(e))
        
        if root.xpath('//grupo'):
            for grupo in root.xpath('//grupo'):  
                vals = {}

                vals["codigo"] = grupo.get("codigo", "").strip()
                vals["nombre"] = grupo.get("nombre", "").strip()

                grupo_existente = self.env["gestion_faltas.grupo"].search(
                    [("codigo", "=", vals["codigo"])], limit=1
                )

                if grupo_existente:
                    grupo_existente.write(vals)
                else:
                    self.env["gestion_faltas.grupo"].create(vals)



        if root.xpath('//alumno'):
            for alumno in root.xpath('//alumno'):
                vals = {}

                vals["nia"] = alumno.get("NIA", "").strip()
                vals["name"] = alumno.get("nombre", "").strip()
                vals["apellido1"] = alumno.get("apellido1", "").strip()
                vals["apellido2"] = alumno.get("apellido2", "").strip()
                vals["grupo_id"] = alumno.get("grupo", "").strip()


                codigo_grupo = alumno.get("grupo", "").strip()

                grupo = self.env["gestion_faltas.grupo"].search(
                    [("codigo", "=", codigo_grupo)], limit=1
                )

                if grupo:
                    vals["grupo_id"] = grupo.id
                else:
                    vals["grupo_id"] = False

                self.env["gestion_faltas.alumno"].create(vals)



        if root.xpath('//docente'):

            for docente in root.xpath('//docente'):
                vals = {}

                vals["name"] = docente.get("nombre", "").strip()
                vals["apellido1"] = docente.get("apellido1", "").strip()
                vals["apellido2"] = docente.get("apellido2", "").strip()

                profesor_existente = self.env["gestion_faltas.profesor"].search([
                    ("name", "=", vals["name"]),
                    ("apellido1", "=", vals["apellido1"]),
                    ("apellido2", "=", vals["apellido2"]),
                ], limit=1)

                if not profesor_existente:
                    self.env["gestion_faltas.profesor"].create(vals)

        if not (root.xpath('//grupo') or root.xpath('//alumno') or root.xpath('//docente')):
            raise UserError("El XML no contiene grupos, alumnos ni docentes.")

        return {'type': 'ir.actions.act_window_close'}

