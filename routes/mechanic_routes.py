from sqlalchemy.exc import IntegrityError
from flask import Blueprint, jsonify, request
from models.db import db
from models.mechanic import Mechanic
from datetime import datetime, date


mechanic = Blueprint('mechanic', __name__)

#get all mechanics
@mechanic.route('/api/mechanics')
def get_mechanics():
    mechanic=Mechanic.query.all()
    return jsonify([mechanics.serialize() for mechanics in mechanic])

def calculate_age(fecha_nacimiento_str):
    fecha_nacimiento = datetime.strptime(fecha_nacimiento_str, "%Y-%m-%d").date()
    hoy = date.today()
    edad = hoy.year - fecha_nacimiento.year - ((hoy.month, hoy.day) < (fecha_nacimiento.month, fecha_nacimiento.day))
    return edad

#create mechanic 
@mechanic.route('/api/add_mechanic', methods=['POST'])
def add_mechanic():
    data = request.get_json()
    
    if not data or not all(key in data for key in ['first_name', 'last_name', 'dni','date_of_birth','email','phone']):
        return jsonify({'error': 'Required data is missing'}), 400

    try:
        print(f"Data received: {data}")
        
        # Calcular edad automáticamente
        age_calculate = calculate_age(data['date_of_birth'])

        # Crear nuevo mecánico con edad calculada
        new_mechanic = Mechanic(
            data['first_name'],
            data['last_name'],
            data['dni'],
            data['date_of_birth'],
            data['email'],
            data['phone'],
            age_calculate
        )

        db.session.add(new_mechanic)
        db.session.commit()
        return jsonify({
            'message': 'Mechanic successfully created',
            'mechanic': new_mechanic.serialize()
        }), 201

    except IntegrityError:
        db.session.rollback()
        return jsonify({'error': 'The email is already registered'}), 400

    except Exception as e:
        db.session.rollback()
        print(f"Unexpected error: {e}")
        return jsonify({'error': 'Error adding mechanic'}), 500
    
#delete mechanic
@mechanic.route('/api/delete_mechanic/<int:id>', methods=['DELETE'])
def delete_cliente(id):
    mechanic = Mechanic.query.get(id)
    if not mechanic:
        return jsonify({'message':'Mechanic not found'}),404
    try:
        db.session.delete(mechanic)
        db.session.commit()
        return jsonify({'message':'Mechanic delete successfully'}),200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error':str(e)}), 500
    
#edit mechanic
@mechanic.route('/api/edit_mechanic/<int:id>', methods=['PUT'])
def edit_mechanic(id):
    data=request.get_json()
    if not data:
        return jsonify({'error':'No data received'}, 400)
    mechanic = Mechanic.query.get(id)
    if not mechanic:
        return jsonify({'message':'Mechanic not found'}),404
    try:
        if 'first_name' in data:
            mechanic.first_name=data['first_name']
        if 'last_name' in data:
            mechanic.last_name=data['last_name']
        if 'dni' in data:
            mechanic.dni=data['dni']
        if 'date_of_birth' in data:
            mechanic.date_of_birth=data['date_of_birth']
        if 'email' in data:
            mechanic.email=data['email']
        if 'phone' in data:
            mechanic.phone=data['phone']
        if 'age' in data:
            mechanic.age=data['age']
        db.session.commit()
        return jsonify({'message':'Mechanic updated correctly','mechanic':mechanic.serialize()}),200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
    
#edit a mechanic attribute
@mechanic.route('/api/update_mechanic/<int:id>', methods=['PATCH'])
def update_mechanic(id):
    data=request.get_json()
    if not data:
        return jsonify({'error':'No data received'}, 400)
    mechanic = Mechanic.query.get(id)
    if not mechanic:
        return jsonify({'message':'Mechanic not found'}),404
    try:
        if 'first_name' in data:
            mechanic.first_name=data['first_name']
        if 'last_name' in data:
            mechanic.last_name=data['last_name']
        if 'dni' in data:
            mechanic.dni=data['dni']
        if 'date_of_birth' in data:
            mechanic.date_of_birth=data['date_of_birth']
        if 'email' in data:
            mechanic.email=data['email']
        if 'phone' in data:
            mechanic.phone=data['phone']
        if 'age' in data:
            mechanic.age=data['age']
        db.session.commit()
        return jsonify({'message':'Mechanic updated correctly','mechanic':mechanic.serialize()}),200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500