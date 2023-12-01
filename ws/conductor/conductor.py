from flask import Blueprint, request, jsonify
from models.conductor.conductor import Conductor,EstadoVehiculo,Ubicacion
import json


ws_conductor = Blueprint('ws_conductor', __name__)

@ws_conductor.route('/conductor/registrar', methods=['POST'])
def registrar():
    if request.method == 'POST':
        if 'id_sede' not in request.form or 'numero_documento' not in request.form or 'nombres' not in request.form or 'direccion' not in request.form or 'email' not in request.form or 'clave' not in request.form or 'telefono' not in request.form or 'licencia_conducir' not in request.form:
            return jsonify({'status': False, 'data': None, 'message': 'Falta parámetros'}), 400
        
        #Leer el parámetro de entrada
        id_sede =request.form['id_sede']
        numero_documento = request.form['numero_documento']
        nombres = request.form['nombres']
        direccion = request.form['direccion']
        email = request.form['email']
        clave = request.form['clave']
        telefono = request.form['telefono']
        licencia_conducir = request.form['licencia_conducir']


        #Instanciar a la clase 
        obj = Conductor(None,id_sede,1,numero_documento, nombres, direccion,email,clave,None,telefono,licencia_conducir)

        #Ejecutar al método insertar()
        resultadoJSON = obj.registrar()

        #Convertir el resultado JSON(String) a JSON(Object)
        resultadoJSONObject = json.loads(resultadoJSON)

        if resultadoJSONObject['status'] == True:
            return jsonify(resultadoJSONObject), 200 #OK
        else:
            return jsonify(resultadoJSONObject), 500 #Error
        

@ws_conductor.route('/conductor/vehiculo/estado', methods=['POST'])
def reportarvehiculo():
    if request.method == 'POST':
        if 'id_vehiculo' not in request.form or 'id_estado' not in request.form or 'observacion' not in request.form:
            return jsonify({'status': False, 'data': None, 'message': 'Falta parámetros'}), 400
        
        #Leer el parámetro de entrada
        id_vehiculo = request.form['id_vehiculo']
        id_estado = request.form['id_estado']
        observacion = request.form['observacion']

        #Instanciar a la clase Cliente
        obj = EstadoVehiculo(None, id_vehiculo, id_estado, observacion=observacion)

        #Ejecutar al método insertar()
        resultadoJSON = obj.reportar()

        #Convertir el resultado JSON(String) a JSON(Object)
        resultadoJSONObject = json.loads(resultadoJSON)

        if resultadoJSONObject['status'] == True:
            return jsonify(resultadoJSONObject), 200 #OK
        else:
            return jsonify(resultadoJSONObject), 500 #Error
        

@ws_conductor.route('/conductor/vehiculo/ubicacion', methods=['POST'])
def reportarubicacion():
    if request.method == 'POST':
        if 'id_vehiculo' not in request.form or 'latitud' not in request.form or 'longitud' not in request.form:
            return jsonify({'status': False, 'data': None, 'message': 'Falta parámetros'}), 400
        
        #Leer el parámetro de entrada
        id_vehiculo = request.form['id_vehiculo']
        latitud = request.form['latitud']
        longitud = request.form['longitud']

        #Instanciar a la clase Cliente
        obj = Ubicacion(None, id_vehiculo, latitud, longitud)

        #Ejecutar al método insertar()
        resultadoJSON = obj.reportarubicacion()

        #Convertir el resultado JSON(String) a JSON(Object)
        return resultadoJSON