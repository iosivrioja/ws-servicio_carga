from conexionDB import Conexion as db
from util import CustomJsonEncoder
import json,datetime

class SolicitudCarga():
    def __init__(self, id=None, id_usuario_cliente=None, descripcion_carga=None, id_clase_carga=None, id_tipo_carga=None, id_categoria_carga=None, peso_kg=None, fecha_partida=None, hora_partida=None, fecha_llegada=None,hora_llegada=None,direccion_partida=None,direccion_llegada=None,monto_pagar=None):

        self.id = id
        self.id_usuario_cliente = id_usuario_cliente
        self.descripcion_carga= descripcion_carga
        self.id_clase_carga = id_clase_carga
        self.id_tipo_carga = id_tipo_carga
        self.id_categoria_carga = id_categoria_carga
        self.peso_kg = peso_kg
        self.fecha_partida = fecha_partida
        self.hora_partida = hora_partida
        self.fecha_llegada = fecha_llegada
        self.hora_llegada = hora_llegada
        self.direccion_partida = direccion_partida
        self.direccion_llegada = direccion_llegada
        self.monto_pagar = monto_pagar


    def registrar(self):
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
                        INSERT INTO solicitudcarga (
                                                    id_usuario_cliente,
                                                    descripcion_carga,
                                                    id_clase_carga,
                                                    id_tipo_carga,
                                                    id_categoria_carga,
                                                    peso_kg,
                                                    direccion_partida,
                                                    direccion_llegada,
                                                    monto_pagar
                                                    )
                                        VALUES 
                                                (%s,%s,%s,%s,%s,%s,%s,%s,%s)
                    """
            #Ejecutar la sentencia sql
            cursor.execute(sql, [self.id_usuario_cliente, self.descripcion_carga,self.id_clase_carga, self.id_tipo_carga, self.id_categoria_carga,self.peso_kg,self.direccion_partida,self.direccion_llegada,self.monto_pagar])

            sql = "insert into estadosolicitud(id_solicitud,id_cliente_registro,id_estado,fecha_hora_registro) values (%s,%s,%s,%s)"
            #Obtener el id_persona, id_rol de la tabla PERSONA
            id_solicitud = con.insert_id()
            fecha_hora_registro = datetime.datetime.now()
            #fecha_hora_registro_str=fecha_hora_registro.strftime(("%Y-%m-%d %H:%M:%S") )
            cursor.execute(sql,[id_solicitud,self.id_usuario_cliente,6,fecha_hora_registro])
            #Confirmar la sentencia
            con.commit()
            #Retornar un mensaje
            return json.dumps({'status': True, 'data': None, 'message': 'Solicitud n° ' + str(id_solicitud) + ' registrado correctamente'})

        except con.Error as error:
            #Revocar la operación en la base de datos
            con.rollback()

            return json.dumps({'status': False, 'data': None, 'message': format(error)})
        finally:
            cursor.close()
            con.close()


    def consultar(self, id):

        #Abrir la conexión a la BD
        con = db().open

        #Crear un cursor
        cursor = con.cursor()

        #Preparar la sentencia SQL
        sql = """
            SELECT u.id AS id, p.nombres AS cliente, u.email 
                FROM usuario u INNER JOIN persona p ON (u.id_persona = p.id)
                WHERE u.id = %s AND u.id_rol = 2

            """
        
        #Ejecutar la sentencia
        cursor.execute(sql, [id])

        #Recuperar los datos y almacenarlos en la variable "datos"
        solicitudes = cursor.fetchall()

        #Declarar una variable para preparar el resultado
        resultado = [] #Array
        for solicitud in solicitudes:
            cliente = solicitud["cliente"]
            email = solicitud["email"]
            id_usuario_cliente = solicitud['id']

            sql_detalle_solicitud = """
                                    select 
                                        s.id,
                                        s.descripcion_carga,
                                        c.nombre AS categoria, 
                                        s.fecha_partida,
                                        s.fecha_llegada 
                                    FROM
                                        solicitudcarga s inner join categoriacarga c on (s.id_categoria_carga = c.id)
                                        INNER JOIN usuario u ON (s.id_usuario_cliente = u.id)
                                    where
                                        s.id_usuario_cliente = %s
                                """
            cursor.execute(sql_detalle_solicitud, [id_usuario_cliente])
            detalle_solicitud = cursor.fetchall()
            detalle_solicitud = [{'solicitud_id': detalle['id'], 'descripcion_carga': detalle['descripcion_carga'], 'categoria': detalle['categoria'], 'fecha_partida': detalle['fecha_partida'], 'fecha_llegada': detalle['fecha_llegada']} for detalle in detalle_solicitud ]
            resultado.append(
                {
                    'cliente': cliente,
                    'email': email,
                    'id_usuario': id_usuario_cliente,
                    'solicitudes': detalle_solicitud
                }
            )

        #Cerrar el cursor y la conexión
        cursor.close()
        con.close()

        #Retornar los resultados
        if solicitudes:
            return json.dumps({'status': True, 'data': resultado, 'message': 'Lista de solicitudes'}, cls=CustomJsonEncoder)
        else:
            return json.dumps({'status': False, 'data': [], 'message': 'Sin registros'})
        

    def consultarestado(self,id):
        #Abrir la conexión a la BD
        con = db().open

        #Crear un cursor
        cursor = con.cursor()

        #Preparar la sentencia SQL
        sql = """
            SELECT
                    s.id as id_Solicitud,
                    s.descripcion_carga,
                    e.nombre AS estado,
                    es.fecha_hora_registro,
                    es.observacion
            FROM 
                estadosolicitud es
                INNER JOIN solicitudcarga s ON (es.id_solicitud = s.id)
                INNER JOIN estado e ON (es.id_estado = e.id)
                
            WHERE
                    s.id=%s
            """
        
        #Ejecutar la sentencia
        cursor.execute(sql, [id])
        
        #Recuperar los datos y almacenarlos en la variable "datos"
        datos = cursor.fetchall()

        #Cerrar el cursor y la conexión
        cursor.close()
        con.close()

        #Retornar los resultados
        if datos:
            return json.dumps({'status': True, 'data': datos, 'message': 'Estados de sus Solicitudes de carga'},cls=CustomJsonEncoder)
        else:
            return json.dumps({'status': False, 'data': None, 'message': 'Cliente no encontrado'})
        

    def consultardetalle(self, id):

        #Abrir la conexión a la BD
        con = db().open

        #Crear un cursor
        cursor = con.cursor()

        #Preparar la sentencia SQL
        sql = """
            SELECT 
                    sc.id, 
                    sc.descripcion_carga, 
                    cc.nombre AS clase_carga,
                    tc.nombre AS tipo_carga,
                    ct.nombre AS categoria,
                    sc.peso_kg,
                    sc.fecha_partida,
                    sc.hora_partida,
                    sc.fecha_llegada,
                    sc.hora_llegada
            FROM 
                solicitudcarga sc
            INNER JOIN  
                clasecarga cc ON (sc.id_clase_carga = cc.id)
            INNER JOIN  
                tipocarga tc ON (sc.id_tipo_carga = tc.id)
            INNER JOIN  
                categoriacarga ct ON (sc.id_categoria_carga = ct.id)
            WHERE 
                sc.id=%s

            """
        
        #Ejecutar la sentencia
        cursor.execute(sql, [id])

        #Recuperar los datos y almacenarlos en la variable "datos"
        detalle_solicitud = cursor.fetchall()

        #Declarar una variable para preparar el resultado
        resultado = [] #Array
        for solicitud in detalle_solicitud:
            descripcion_carga = solicitud["descripcion_carga"]
            clase_carga = solicitud["clase_carga"]
            tipo_carga = solicitud['tipo_carga']
            categoria = solicitud['categoria']
            peso_kg = solicitud['peso_kg']
            fecha_partida = solicitud['fecha_partida']
            hora_partida = solicitud['hora_partida']
            fecha_llegada = solicitud['fecha_llegada']
            hora_llegada = solicitud['hora_llegada']
            id_solicitud_carga = solicitud['id']




            sql_detalle_solicitud = """
                                    SELECT 
                                            a.id_solicitud AS solicitud,
                                            v.modelo,
                                            v.placa,
                                            p.nombres AS conductor,
                                            p.numero_documento,
                                            p.telefono,
                                            p.licencia_conducir
                                            
                                    FROM 
                                        asignacionvehiculoconductor a
                                    INNER JOIN 
                                        vehiculo v ON (a.id_vehiculo = v.id)
                                    INNER JOIN 
                                        usuario u ON (a.id_usuario_conductor = u.id)
                                    INNER JOIN 
                                        persona p ON (p.id=u.id_persona)
                                    WHERE
                                        a.id_solicitud=%s
                                """
            cursor.execute(sql_detalle_solicitud, [id_solicitud_carga])
            solicitud_detalle = cursor.fetchall()
            solicitud_detalle = [{'solicitud_id': detalle['solicitud'], 'modelo_vehiculo': detalle['modelo'], 'placa_vehiculo': detalle['placa'], 'conductor': detalle['conductor'], 'documento_conductor': detalle['numero_documento'],'telefono_conductor': detalle['telefono'], 'licencia_conducir': detalle['licencia_conducir']} for detalle in solicitud_detalle ]
            resultado.append(
                {   
                    'id_solicitud_carga':id_solicitud_carga,
                    'descripcion_carga': descripcion_carga,
                    'clase_carga': clase_carga,
                    'tipo_carga': tipo_carga,
                    'categoria': categoria,
                    'peso_kg': peso_kg,
                    'fecha_partida': fecha_partida,
                    'hora_partida': hora_partida,
                    'fecha_llegada': fecha_llegada,
                    'hora_llegada': hora_llegada,
                    'detalle_solitud':solicitud_detalle
                }
            )

        #Cerrar el cursor y la conexión
        cursor.close()
        con.close()

        #Retornar los resultados
        if detalle_solicitud:
            return json.dumps({'status': True, 'data': resultado, 'message': 'Detalle de solicitud'}, cls=CustomJsonEncoder)
        else:
            return json.dumps({'status': False, 'data': [], 'message': 'Sin registros'})


class EstadoSolicitud():
    def __init__(self, id=None, id_solicitud=None, id_usuario_registro=None, id_estado=None, fecha_hora_registro=None, observacion=None):

        self.id = id
        self.id_solicitud = id_solicitud
        self.id_usuario_registro = id_usuario_registro
        self.id_estado= id_estado
        self.fecha_hora_registro = fecha_hora_registro
        self.observacion = observacion

    def anular(self):
        #Abrir conexión a la BD
        con = db().open

        #Configurar para que los cambios de escritura en la BD se confirmen de manera manual
        con.autocommit = False

        #Crear un cursor
        cursor = con.cursor()

        #Preparar la sentencia para actualizar el token
        sql = "UPDATE estadosolicitud SET id_estado = 11  WHERE id_solicitud=%s  AND id_estado = 6"

        try:

            #Ejecutar la sentencia sql
            cursor.execute(sql, [self.id_solicitud])

            #Confirmar la sentencia de actualización
            con.commit()

            #Retornar un mensaje
            return json.dumps({'status': True, 'data': None, 'message': 'SoliIcitud de carga ANULADA'})

        except con.Error as error:
            #Revocar la operación en la base de datos
            con.rollback()

            return json.dumps({'status': False, 'data': None, 'message': format(error)})
        finally:
            cursor.close()
            con.close()


class Asignacion():
    def __init__(self, id=None, id_solicitud=None, id_vehiculo=None, id_usuario_conductor=None, id_usuario_registro=None):

        self.id = id
        self.id_solicitud = id_solicitud
        self.id_vehiculo= id_vehiculo
        self.id_usuario_conductor = id_usuario_conductor
        self.id_usuario_registro = id_usuario_registro


    def consultar(self, id):

        #Abrir la conexión a la BD
        con = db().open

        #Crear un cursor
        cursor = con.cursor()

        #Preparar la sentencia SQL
        sql = """
                   SELECT 
                            id AS solicitud_id,
                            descripcion_carga
                    FROM 
                        solicitudcarga 
                    WHERE
                        id=%s
            """
        
        #Ejecutar la sentencia
        cursor.execute(sql, [id])

        #Recuperar los datos y almacenarlos en la variable "datos"
        ubicaciones = cursor.fetchall()

        #Declarar una variable para preparar el resultado
        resultado = [] #Array
        for solicitud in ubicaciones:
            descripcion_carga = solicitud["descripcion_carga"]
            solicitud_id = solicitud['solicitud_id']

            sql_detalle_ubicacion = """
                                    SELECT 
                                            ub.id_vehiculo,
                                            ub.latitud,
                                            ub.longitud
                                    FROM 
                                        ubicacion ub
                                    INNER JOIN 
                                        vehiculo v ON (ub.id_vehiculo = v.id)
                                    INNER JOIN 
                                        asignacionvehiculoconductor a ON (ub.id_vehiculo = a.id_vehiculo)
                                    WHERE 
                                        a.id_solicitud = %s
                                """
            cursor.execute(sql_detalle_ubicacion, [solicitud_id])
            detalle_ubicacion = cursor.fetchall()
            detalle_ubicacion = [{'id_vehiculo': detalle['id_vehiculo'], 'latitud': detalle['latitud'], 'longitud': detalle['longitud']} for detalle in detalle_ubicacion ]
            resultado.append(
                {
                    'id_solicitud': solicitud_id,
                    'descripcion_carga': descripcion_carga,
                    'ubicaciones': detalle_ubicacion
                }
            )

        #Cerrar el cursor y la conexión
        cursor.close()
        con.close()

        #Retornar los resultados
        if ubicaciones:
            return json.dumps({'status': True, 'data': resultado, 'message': 'Lista de solicitudes'}, cls=CustomJsonEncoder)
        else:
            return json.dumps({'status': False, 'data': [], 'message': 'Sin registros'})


        
        
        
