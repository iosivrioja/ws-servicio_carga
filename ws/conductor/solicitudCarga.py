from flask import Blueprint, request, jsonify
from models.conductor.solicitudCarga import SolicitudCarga,EstadoSolicitud
import json


ws_solicitud_conductor = Blueprint('ws_solicitud_conductor', __name__)

@ws_solicitud_conductor.route('/conductor/solicitud/<int:id>', methods=['GET'])
def listar(id):
    if request.method == 'GET':
        #Instanciar a la clase Cliente
        obj = SolicitudCarga()

        #Ejecutar al método catalogoCliente()
        resultadoJSON = obj.listar(id)

        #Convertir el resultado JSON(String) a JSON(Object)
        resultadoJSONObject = json.loads(resultadoJSON)

        if resultadoJSONObject['status'] == True:
            return jsonify(resultadoJSONObject), 200 #OK
        else:
            return jsonify(resultadoJSONObject), 205 #No content
        

@ws_solicitud_conductor.route('/conductor/solicitud/actual/<int:id>', methods=['GET'])
def listaractual(id):
    if request.method == 'GET':
        #Instanciar a la clase Cliente
        obj = SolicitudCarga()

        #Ejecutar al método catalogoCliente()
        resultadoJSON = obj.listaractual(id)

        #Convertir el resultado JSON(String) a JSON(Object)
        resultadoJSONObject = json.loads(resultadoJSON)

        if resultadoJSONObject['status'] == True:
            return jsonify(resultadoJSONObject), 200 #OK
        else:
            return jsonify(resultadoJSONObject), 205 #No content
        

@ws_solicitud_conductor.route('/conductor/solicitud/estado', methods=['POST'])
def registrar():
    if request.method == 'POST':
        if 'id_solicitud' not in request.form or 'id_usuario_registro' not in request.form or 'id_estado' not in request.form or 'observacion' not in request.form:
            return jsonify({'status': False, 'data': None, 'message': 'Falta parámetros'}), 400
        
        #Leer el parámetro de entrada
        id_solicitud = request.form['id_solicitud']
        id_usuario_registro = request.form['id_usuario_registro']
        id_estado = request.form['id_estado']
        observacion = request.form['observacion']

        #Instanciar a la clase Cliente
        obj = EstadoSolicitud(None, id_solicitud, id_usuario_registro, id_estado, observacion=observacion)

        #Ejecutar al método insertar()
        resultadoJSON = obj.reportar()

        #Convertir el resultado JSON(String) a JSON(Object)
        resultadoJSONObject = json.loads(resultadoJSON)

        if resultadoJSONObject['status'] == True:
            return jsonify(resultadoJSONObject), 200 #OK
        else:
            return jsonify(resultadoJSONObject), 500 #Error
    
