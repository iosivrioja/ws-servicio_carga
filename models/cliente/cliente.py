from conexionDB import Conexion as db
import json

class Cliente():
    def __init__(self, id=None, id_tipo_doc=None ,numero_documento=None, nombres=None, direccion=None, email=None, clave=None, img=None, telefono=None):
        self.id = id
        self.id_tipo_doc= id_tipo_doc
        self.numero_documento = numero_documento
        self.nombres= nombres
        self.direccion = direccion
        self.email = email
        self.clave = clave
        self.img = img
        self.telefono = telefono

    def registrar(self):
        #Abrir conexión a la BD
        con = db().open
        #Configurar para que los cambios de escritura en la DB se confirmen de manera manual
        con.autocommit = False
        #Crear un cursor
        cursor = con.cursor()

        try:
            #1 Registrar Persona Cliente
            #Preparar la sentencia SQL
            sql =   """INSERT 
                            INTO persona
                                    (
                                        id_tipo_doc,
                                        numero_documento,
                                        nombres,
                                        direccion,
                                        email,
                                        clave,
                                        img,
                                        telefono
                                    )
                            VALUES 
                                    (%s,%s,%s,%s,%s,%s,%s,%s)
                    """
            #Ejecutar la sentencia sql
            cursor.execute(sql, [self.id_tipo_doc, self.numero_documento, self.nombres, self.direccion,self.email,self.clave,self.img,self.telefono])


            sql = "insert into usuario(id_persona,id_rol,email,clave,id_estado) values (%s,%s,%s,%s,%s)"
            #Obtener el id_persona, id_rol de la tabla PERSONA
            id_persona = con.insert_id()
            cursor.execute(sql,[id_persona,2,self.email,self.clave,1])
            #Confirmar la sentencia
            con.commit()
            #Retornar un mensaje
            return json.dumps({'status': True, 'data': None, 'message': 'Usuario CLIENTE: '+ self.email + ' registrado correctamente'})

        except con.Error as error:
            #Revocar la operación en la base de datos
            con.rollback()

            return json.dumps({'status': False, 'data': None, 'message': format(error)})
        finally:
            cursor.close()
            con.close()



