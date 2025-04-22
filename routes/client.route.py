from sqlalchemy.exc import IntegrityError
from flask import Blueprint, jsonify, request
from models.db import db
from client import db

from flask import Blueprint, request, jsonify
from sqlalchemy.exc import IntegrityError
from models.db import db
from models.client import Client  # Asegúrate de tener estos campos en tu modelo

client_bp = Blueprint('client', __name__)

@client_bp.route('/clients', methods=['POST'])
def create_client():
    data = request.get_json()

    required_fields = ['first_name', 'cuit', 'type_invoice', 'email', 'phone', 'address']
    if not data or not all(key in data for key in required_fields):
        return jsonify({'error': 'Required data is missing'}), 400

    try:

        print(f"Data received: {data}")

        new_client = Client(
            first_name=data['first_name'],
            cuit=data['cuit'],
            type_invoice=data['type_invoice'],
            email=data['email'],
            phone=data['phone'],
            address=data['address']
        )

    
        print(f"Creating Client: {new_client.first_name}, {new_client.cuit}, {new_client.type_invoice}, "
              f"{new_client.email}, {new_client.phone}, {new_client.address}")

        db.session.add(new_client)
        db.session.commit()

        return jsonify({'message': 'Client created!'}), 201

    except IntegrityError as e:
        db.session.rollback()
        return jsonify({'error': f'Possible duplicate issue: {str(e)}'}), 400


    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500


@Client.route("/api/del_client/<int:id>", methods=['DELETE'])
def delete_client(id):
    client = Client.query.get(id)
    
    if not client: 
        return jsonify({'message':'Cliente not found'}), 404 # mensaje que retorna cuando no encuetra cliente para eliminar 
    try:
        db.session.delete(client)
        db.session.commit()
        return jsonify({'message': 'Client delete'}), 200 # mensaje que retorna cuuando elimina al cliente
    except Exception as e:
        db.session.rollback()
        return jsonify({'error':str(e)}), 500

@Client.route('/api/up_client/<int:id>', methods=['PUT'])
def update_cliente(id):

    data = request.get_json()

    if not data:
        return jsonify({'error':'No data received'}, 400) # No se recibio nungun dato 
    
    client = Client.query.get(id)

    if not client:
        return jsonify({'error': 'Client not found'}), 404 # No se encontro al Cliente 
    
    try:
        if "name" in data:
            client.name = data['name']
        if 'email' in data:
            client.email = data['email']
        if 'phone' in data:
            client.phone = data['phone']

        db.session.commit()

        return jsonify({'message':'Updated client', 'client': client.serialize()}), 200 # se pudo actualizar el cliente 
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
    

@Client.route('/api/update_client/<int:id>', methods=['PATCH'])
def patch_client(id):
    data = request.get_json()

    if not data:
        return jsonify({'error': 'No data received'}), 400 #  no se recibio ningun dato

    client = Client.query.get(id)
    
    if not client:
        return jsonify({'error': 'Cliente no encontrado'}), 404

    try:
        if 'name' in data and data['name']:
            client.name = data['name']
        if 'email' in data and data['email']:
            client.email = data['email']
        if 'phone' in data and data['phone']:
            client.phone = data['phone']

        db.session.commit()
        return jsonify({'message': 'Updated client', 'client': client.serialize()}), 200

   
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500