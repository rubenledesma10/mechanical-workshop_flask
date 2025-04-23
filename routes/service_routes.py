from sqlalchemy.exc import IntegrityError
from flask import Blueprint, jsonify, request
from models.db import db
from models.service import Service

service = Blueprint('service', __name__)


@service.route('/api/service')
def get_service():
    services = Service.query.all()
    return jsonify([serv.serialize() for serv in services])

@service.route('/api/add_service', methods=['POST'])
def add_service():
    data = request.get_json()

    if not data or not all(key in data for key in ['name', 'cost', 'detail_service', 'status_service', 'paid_method', 'priority']):
        return jsonify({'error': 'Faltan datos requeridos'}), 400

    try:
        print(f"Datos recibidos: {data}")
        new_service = Service(
            data['name'],
            data['cost'],
            data['detail_service'],
            data['status_service'],
            data['paid_method'],
            data['priority']
        )
        print(f"Creando nuevo servicio: {new_service.name}, {new_service.cost}, {new_service.detail_service}")

        db.session.add(new_service)
        db.session.commit()

        return jsonify({'Respuesta': 'Servicio creado exitosamente', 'servicio': new_service.serialize()}), 201

    except Exception as e:
        db.session.rollback()
        print(f"Error inesperado: {e}") 
        return jsonify({'error': f'Error al crear el servicio: {str(e)}'}), 500


@service.route("/api/del_service/<int:id>", methods=['DELETE'])
def delete_service(id):
    service = Service.query.get(id)

    if not service:
        return jsonify({'message': 'Servicio no encontrado'}), 404
    try:
        db.session.delete(service)
        db.session.commit()
        return jsonify({'mensaje': 'Servicio eliminado correctamente!'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@service.route('/api/up_service/<int:id>', methods=['PUT'])
def update_service(id):
    data = request.get_json()

    if not data:
        return jsonify({'error': 'No se recibieron datos'}), 400

    service = Service.query.get(id)

    if not service:
        return jsonify({'error': 'Servicio no encontrado'}), 404

    try:
        for field in ['name', 'cost', 'detail_service', 'status_service', 'paid_method', 'priority']:
            if field in data:
                setattr(service, field, data[field])

        db.session.commit()
        return jsonify({'Mensaje': 'Servicio actualizado correctamente', 'servicio': service.serialize()}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@service.route('/api/update_service/<int:id>', methods=['PATCH'])
def patch_service(id):
    data = request.get_json()

    if not data:
        return jsonify({'error': 'No se recibieron datos'}), 400

    service = Service.query.get(id)

    if not service:
        return jsonify({'error': 'Servicio no encontrado'}), 404

    try:
        for field in ['name', 'cost', 'detail_service', 'status_service', 'paid_method', 'priority']:
            if field in data and data[field]:
                setattr(service, field, data[field])

        db.session.commit()
        return jsonify({'Mensaje': 'Servicio actualizado correctamente', 'Servicio': service.serialize()}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
