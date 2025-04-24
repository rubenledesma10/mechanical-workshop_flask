from sqlalchemy.exc import IntegrityError
from flask import Blueprint, jsonify, request
from models.db import db
from models.service import Service

service_rp = Blueprint('service', __name__)


@service_rp.route('/api/service')
def get_service():
    services = Service.query.all()
    if not services:
        return jsonify({'message':'There are no mechanics registered'}),200
    return jsonify([serv.serialize() for serv in services])


@service_rp.route('/api/get_service/<int:id>')
def get_id_service(id):
    id_service=Service.query.get(id)
    if not id_service:
        return jsonify({'message':'Service not found'}),404
    return jsonify(id_service.serialize()),200

@service_rp.route('/api/add_service', methods=['POST'])
def add_service_rp():
    data = request.get_json()

    if not data or not all(key in data for key in ['name', 'cost', 'detail_service', 'status_service', 'paid_method', 'priority']):
        return jsonify({'error': 'Required data is missing'}), 400

    try:
        print(f"Data received: {data}")
        new_service = Service(
            data['name'],
            data['cost'],
            data['detail_service'],
            data['status_service'],
            data['paid_method'],
            data['priority']
        )
        print(f"Creating new service: {new_service.name}, {new_service.cost}, {new_service.detail_service}")

        db.session.add(new_service)
        db.session.commit()

        return jsonify({'Response': 'Service created successfully', 'servicio': new_service.serialize()}), 201

    except Exception as e:
        db.session.rollback()
        print(f"Unexpected error: {e}") 
        return jsonify({'error': f'Error creating service: {str(e)}'}), 500


@service_rp.route("/api/del_service/<int:id>", methods=['DELETE'])
def delete_service(id):
    service = Service.query.get(id)

    if not service_rp:
        return jsonify({'message': 'Service not found'}), 404
    try:
        db.session.delete(service)
        db.session.commit()
        return jsonify({'message': 'Service successfully removed!'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@service_rp.route('/api/up_service/<int:id>', methods=['PUT'])
def update_service_rp(id):
    data = request.get_json()

    if not data:
        return jsonify({'error': 'No data received'}), 400

    service = Service.query.get(id)

    if not service:
        return jsonify({'error': 'Service not found'}), 404

    try:
        for field in ['name', 'cost', 'detail_service', 'status_service', 'paid_method', 'priority']:
            if field in data:
                setattr(service, field, data[field])

        db.session.commit()
        return jsonify({'message': 'Service updated successfully', 'servicio': service.serialize()}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@service_rp.route('/api/update_service/<int:id>', methods=['PATCH'])
def patch_service_rp(id):
    data = request.get_json()

    if not data:
        return jsonify({'error': 'No data received'}), 400

    service = Service.query.get(id)

    if not service:
        return jsonify({'error': 'Service not found'}), 404

    try:
        for field in ['name', 'cost', 'detail_service', 'status_service', 'paid_method', 'priority']:
            if field in data and data[field]:
                setattr(service, field, data[field])

        db.session.commit()
        return jsonify({'message': 'Service updated successfully', 'Servicio': service.serialize()}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
