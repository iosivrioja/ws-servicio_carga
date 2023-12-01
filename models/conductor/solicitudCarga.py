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
        

    def listar(self,id):
        #Abrir la conexión a la BD
        con = db().open

        #Crear un cursor
        cursor = con.cursor()

        #Preparar la sentencia SQL
        sql = """
           SELECT 
                s.id,
                s.descripcion_carga,
                c.nombre AS categoria,
                s.direccion_partida,
                s.fecha_partida,
                s.hora_partida
            FROM
                solicitudcarga s 
                INNER JOIN categoriacarga c ON (s.id_categoria_carga = c.id)
                INNER JOIN usuario u ON (s.id_usuario_cliente = u.id)
                INNER JOIN asignacionvehiculoconductor a ON (s.id = a.id_solicitud)
            WHERE
                a.id_usuario_conductor = %s
            """
        
        #Ejecutar la sentencia
        cursor.execute(sql,(id,))
        
        #Recuperar los datos y almacenarlos en la variable "datos"
        datos = cursor.fetchall()

        #Cerrar el cursor y la conexión
        cursor.close()
        con.close()

        #Retornar los resultados
        if datos:
            return json.dumps({'status': True, 'data': datos, 'message': 'Lista de Solicitudes'},cls=CustomJsonEncoder)
        else:
            return json.dumps({'status': False, 'data': [], 'message': 'Sin registros'})
        

    def listaractual(self, id):

        #Abrir la conexión a la BD
        con = db().open

        #Crear un cursor
        cursor = con.cursor()

        #Preparar la sentencia SQL
        sql = """
          SELECT 
                s.id,
                s.descripcion_carga,
                c.nombre AS categoria, 
                s.fecha_partida,
                s.fecha_llegada,
                e.nombre AS estado,
                p.nombres AS cliente,
                p.telefono AS telefono_cleinte    
            FROM
                solicitudcarga s 
                INNER JOIN categoriacarga c ON (s.id_categoria_carga = c.id)
                INNER JOIN usuario u ON (s.id_usuario_cliente = u.id)
                INNER JOIN asignacionvehiculoconductor a ON (s.id = a.id_solicitud)
                INNER JOIN estadosolicitud es ON (s.id = es.id_solicitud)
                INNER JOIN persona p ON (s.id_usuario_cliente = p.id)
                INNER JOIN estado e ON (es.id_estado = e.id)
            WHERE
                es.id_estado NOT IN ('1','4','11','12') AND  a.id_usuario_conductor = %s            """
        
        #Ejecutar la sentencia
        cursor.execute(sql,(id,))
        
        #Recuperar los datos y almacenarlos en la variable "datos"
        datos = cursor.fetchall()

        #Cerrar el cursor y la conexión
        cursor.close()
        con.close()

        #Retornar los resultados
        if datos:
            return json.dumps({'status': True, 'data': datos, 'message': 'Lista de Solicitudes actuales'},cls=CustomJsonEncoder)
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
                        
                        INSERT INTO estadosolicitud (
                                                    id_solicitud,
                                                    id_usuario_registro,
                                                    id_estado,
                                                    fecha_hora_registro,
                                                    observacion
                                                    )
                                        VALUES 
                                                (%s,%s,%s,%s,%s)
                    """
            #Ejecutar la sentencia sql
            self.fecha_hora_registro=datetime.datetime.now()
            cursor.execute(sql, [self.id_solicitud, self.id_usuario_registro,self.id_estado, self.fecha_hora_registro,self.observacion])

            #Confirmar la sentencia
            con.commit()
            #Retornar un mensaje
            return json.dumps({'status': True, 'data': None, 'message': 'Estado de vehiculo registrado correctamente'})

        except con.Error as error:
            #Revocar la operación en la base de datos
            con.rollback()

            return json.dumps({'status': False, 'data': None, 'message': format(error)})
        finally:
            cursor.close()
            con.close()




        
        
        
