from conexionDB import Conexion as db
import json, datetime
from flask import jsonify

class Conductor():
    def __init__(self, id=None, id_sede=None,id_tipo_doc=None ,numero_documento=None, nombres=None, direccion=None, email=None, clave=None, img=None, telefono=None,licencia_conducir=None):
        self.id = id
        self.id_sede = id_sede
        self.id_tipo_doc= id_tipo_doc
        self.numero_documento = numero_documento
        self.nombres= nombres
        self.direccion = direccion
        self.email = email
        self.clave = clave
        self.img = img
        self.telefono = telefono
        self.licencia_conducir = licencia_conducir

    def registrar(self):
        #Abrir conexión a la BD
        con = db().open
        #Configurar para que los cambios de escritura en la DB se confirmen de manera manual
        con.autocommit = False
        #Crear un cursor
        cursor = con.cursor()

        try:
            #1 Registrar Persona Conductor
            #Preparar la sentencia SQL
            sql =   """INSERT 
                            INTO persona
                                    (
                                        id_sede,
                                        id_tipo_doc,
                                        numero_documento,
                                        nombres,
                                        direccion,
                                        email,
                                        clave,
                                        img,
                                        telefono,
                                        licencia_conducir
                                    )
                            VALUES 
                                    (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                    """
            #Ejecutar la sentencia sql
            cursor.execute(sql, [self.id_sede,self.id_tipo_doc, self.numero_documento, self.nombres, self.direccion,self.email,self.clave,self.img,self.telefono,self.licencia_conducir])


            sql = "insert into usuario(id_persona,id_rol,email,clave,id_estado) values (%s,%s,%s,%s,%s)"
            #Obtener el id_persona de la tabla PERSONA
            id_persona = con.insert_id()
            cursor.execute(sql,[id_persona,3,self.email,self.clave,2])
            #Confirmar la sentencia
            con.commit()
            #Retornar un mensaje
            return json.dumps({'status': True, 'data': None, 'message': ' Usuario CONDUCTOR: ' + self.email +   ' registrado correctamente'})

        except con.Error as error:
            #Revocar la operación en la base de datos
            con.rollback()

            return json.dumps({'status': False, 'data': None, 'message': format(error)})
        finally:
            cursor.close()
            con.close()


class EstadoVehiculo():
    def __init__(self, id=None, id_vehiculo=None, id_estado=None, fecha_hora_registro=None, observacion=None):

        self.id = id
        self.id_vehiculo = id_vehiculo
        self.id_estado= id_estado
        self.fecha_hora_registro = fecha_hora_registro
        self.observacion = observacion


    def reportar(self):
        #Abrir conexión a la BD
        con = db().open
        #Configurar para que los cambios de escritura en la DB se confirmen de manera manual
        con.autocommit = False
        #Crear un cursor
        cursor = con.cursor()

        try:
            #1 Registrar Solictud de Carga
            #Preparar la sentencia SQL
            sql =   """
                        
                        INSERT INTO estadovehiculo (
                                                    id_vehiculo,
                                                    id_estado,
                                                    fecha_hora_registro,
                                                    observacion
                                                    )
                                        VALUES 
                                                (%s,%s,%s,%s)
                    """
            #Ejecutar la sentencia sql
            self.fecha_hora_registro=datetime.datetime.now()
            cursor.execute(sql, [self.id_vehiculo,self.id_estado, self.fecha_hora_registro,self.observacion])

            #Confirmar la sentencia
            con.commit()
            #Retornar un mensaje
            return json.dumps({'status': True, 'data': None, 'message': 'Estado de Vehiculo registrado correctamente'})

        except con.Error as error:
            #Revocar la operación en la base de datos
            con.rollback()

            return json.dumps({'status': False, 'data': None, 'message': format(error)})
        finally:
            cursor.close()
            con.close()


class Ubicacion():
    def __init__(self, id=None, id_vehiculo=None, latitud=None, longitud=None, hora_ubicacion=None):

        self.id = id
        self.id_vehiculo = id_vehiculo
        self.latitud= latitud
        self.longitud = longitud
        self.hora_ubicacion = hora_ubicacion


    def reportarubicacion(self):
        #Abrir conexión a la BD
        con = db().open
        #Configurar para que los cambios de escritura en la DB se confirmen de manera manual
        con.autocommit = False
        #Crear un cursor
        cursor = con.cursor()

        try:
            #1 Registrar Solictud de Carga
            #Preparar la sentencia SQL
            sql =   """
                        
                        INSERT INTO ubicacion (
                                                    id_vehiculo,
                                                    latitud,
                                                    longitud,
                                                    hora_ubicacion
                                                    )
                                        VALUES 
                                                (%s,%s,%s,%s)
                    """
            #Ejecutar la sentencia sql
            self.hora_ubicacion=datetime.datetime.now()
            cursor.execute(sql, [self.id_vehiculo,self.latitud, self.longitud,self.hora_ubicacion])

            #Confirmar la sentencia
            con.commit()
            #Retornar un mensaje
            return jsonify({'status': True, 'data': None, 'message': 'Reporte de ubicacion registrado correctamente'})

        except con.Error as error:
            #Revocar la operación en la base de datos
            con.rollback()

            return jsonify({'status': False, 'data': None, 'message': format(error)})
        finally:
            cursor.close()
            con.close()
