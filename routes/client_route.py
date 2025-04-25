from sqlalchemy.exc import IntegrityError
from flask import Blueprint, jsonify, request
from models.db import db
from models.Client import Client



client_bp = Blueprint('client', __name__)

@client_bp.route('/api/client')
def get_clients():
    client=Client.query.all() 
    if not client:
        return jsonify({'message':'There are no clients registered'}),200
    return jsonify([clients.serialize() for clients in client])

@client_bp.route('/api/get_client/<int:id>')
def get_client_id(id):
    client_bp=Client.query.get(id)
    if not client_bp:
        return jsonify({'message':'Client not found'}),404
    return jsonify(client_bp.serialize()),200

@client_bp.route('/api/clients', methods=['POST'])
def add_client():
    data = request.get_json()

    required_fields = ['first_name', 'last_name', 'cuit', 'type_invoice', 'email', 'phone', 'address'] #Carga de un cliente nuevo
    if not data or not all(key in data for key in required_fields):
        return jsonify({'error': 'Required data is missing'}), 400
        
    for field in required_fields:
        if not str(data.get(field, '')).strip():  
            return jsonify({'error': f'{field.title()} is required and cannot be empty'}), 400


    try:

        print(f"Data received: {data}")

        new_client = Client(
            first_name=data['first_name'],
            last_name=data ['last_name'],
            cuit=data['cuit'],
            type_invoice=data['type_invoice'],
            email=data['email'],
            phone=data['phone'],
            address=data['address']
        )

    
        print(f"Creating Client: {new_client.first_name}, {new_client.last_name}, {new_client.cuit}, {new_client.type_invoice}, "
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


@client_bp.route("/api/get_client/<int:id>", methods=['DELETE'])
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

@client_bp.route('/api/up_client/<int:id>', methods=['PUT'])
def update_cliente(id):

    data = request.get_json()

    if not data:
        return jsonify({'error':'No data received'}, 400) # No se recibio nungun dato 
    
    client = Client.query.get(id)

    if not client:
        return jsonify({'error': 'Client not found'}), 404 # No se encontro al Cliente 
    
    try:
        if "first_name" in data:
            client.first_name = data['first_name']
        if 'last_name' in data:
            client.last_name = data['last_name']
        if 'cuit' in data:
            client.cuit = data['cuit']
        if 'last_name' in data:
            client.type_invoyce = data['type_invoice']
        if 'email' in data:
            client.email = data['email']
        if 'last_name' in data:
            client.phone = data['phone']
        if 'last_name' in data:
            client.address = data['address']
           

        db.session.commit()

        return jsonify({'message':'Updated client', 'client': client.serialize()}), 200 # se pudo actualizar el cliente 
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
    

@client_bp.route('/api/update_client/<int:id>', methods=['PATCH'])
def patch_client(id):
    data = request.get_json()

    if not data:
        return jsonify({'error': 'No data received'}), 400 #  no se recibio ningun dato

    client = Client.query.get(id)
    
    if not client:
        return jsonify({'error': 'Cliente no encontrado'}), 404

    try:
        if "first_name" in data:
            client.first_name = data['first_name']
        if 'last_name' in data:
            client.last_name = data['last_name']
        if 'cuit' in data:
            client.cuit = data['cuit']
        if 'type_invoice' in data:
            client.type_invoyce = data['type_invoice']
        if 'email' in data:
            client.email = data['email']
        if 'phone' in data:
            client.phone = data['phone']
        if 'address' in data:
            client.address = data['address']
        
        db.session.commit()
        return jsonify({'message': 'Updated client', 'client': client.serialize()}), 200

   
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500