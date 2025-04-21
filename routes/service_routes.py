from sqlalchemy.exc import IntegrityError
from flask import Blueprint, jsonify, request
from models.db import db
from models.service import Service

client = Blueprint('service', __name__)



@client.route('/api/service')
def get_service():
    services = Service.query.all()
    return jsonify([services.serialize() for serv in services])


@client.route('/api/add_service', methods=['POST'])
def add_service():
    data = request.get_json()

    if not data or not all(key in data for key in ['name', 'cost', 'datail_service','status_service','paid_method','priority']):
        return jsonify({'error': 'Faltan datos requeridos'}), 400

    try:
        print(f"Datos recibidos: {data}")  

        new_service = Service(data['name'], data['cost'], data['datail_service'],data['status_service'],data['paid_method'],data['priority'])
        print(f"Creando nuevo servicio: {new_service.name}, {new_service.cost}, {new_service.detail_service}")

        db.session.add(new_service)
        db.session.commit()

        return jsonify({'Respuesta': 'Servicio creado exitosamente', 'servicio': new_service.serialize()}), 201

    except Exception as e:
        db.session.rollback()
        print(f"Error inesperado: {e}") 
        return jsonify({'error': 'Error al crear el servicio'}), 500

@client.route("/api/del_service/<int:id>", methods=['DELETE'])
def delete_service(id):
    service = Service.query.get(id)
    
    if not service: 
        return jsonify({'message':'Servicio no encontrado'}), 404 
    try:
        db.session.delete(service)
        db.session.commit()
        return jsonify({'mensaje': 'Servico elimado correctamente!'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error':str(e)}), 500

@client.route('/api/up_service/<int:id>', methods=['PUT'])
def update_service(id):

    data = request.get_json()

    if not data:
        return jsonify({'error':'No se recibieron datos'}, 400)
    
    service = Service.query.get(id)

    if not service:
        return jsonify({'error': 'Servicio no encontrado'}), 404
    
    try:
        if "name" in data:
            service.name = data['name']
        if 'cost' in data:
            service.cost = data['cost']
        if 'datail_service' in data:
            service.datail_service = data['datail_service']
        if 'status_service' in data:
            service.status_service = data['status_service']
        if 'paid_method' in data:
            service.paid_method = data['paid_method']
        if 'priority' in data:
            service.priority = data['priority']

        db.session.commit()

        return jsonify({'Mensaje':'Servicio actulizado correctamente', 'servicio': service.serialize()}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
    

@client.route('/api/update_service/<int:id>', methods=['PATCH'])
def patch_service(id):
    data = request.get_json()

    if not data:
        return jsonify({'error': 'No se recibieron datos'}), 400

    service = Service.query.get(id)
    
    if not service:
        return jsonify({'error': 'Servicio no encontrado'}), 404

    try:
        if 'name' in data and data['name']:
            service.name = data['name']
        if 'cost' in data and data['cost']:
            service.cost = data['cost']
        if 'datail_service' in data and data['datail_service']:
            service.datail_service = data['datail_service']
        if 'status_service' in data and data['status_service']:
            service.status_service = data['status_service']
        if 'paid_method' in data and data['paid_method']:
            service.paid_method = data['paid_method']
        if 'priority' in data and data['priority']:
            service.priority = data['priority']

        db.session.commit()
        return jsonify({'Mensaje': 'Servicio actualizado correctamente', 'Servicio': service.serialize()}), 200

   
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500