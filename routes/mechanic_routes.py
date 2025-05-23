from sqlalchemy.exc import IntegrityError #para capturar errores en la bd
from flask import Blueprint, jsonify, request #blueprint -> modularizar las rutas, jsonify ->para convertir a json, request->para acceder a los datos que llegan en la solicitud
from models.db import db #para hacer las operaciones en la bd
from models.mechanic import Mechanic
from datetime import datetime, date #para manejar fechas y calcular edad


mechanic = Blueprint('mechanic', __name__) #creamos blueprint

#get all mechanics
@mechanic.route('/api/mechanics')
def get_mechanics():
    mechanic=Mechanic.query.all() #llamamos a todos los mecanicos que hay en la bd
    if not mechanic:
        return jsonify({'message':'There are no mechanics registered'}),200
    return jsonify([mechanics.serialize() for mechanics in mechanic])

#get mechanic by id
@mechanic.route('/api/get_mechanic/<int:id>')
def get_mechanic_id(id):
    mechanic=Mechanic.query.get(id)
    if not mechanic:
        return jsonify({'message':'Mechanic not found'}),404
    return jsonify(mechanic.serialize()),200

def calculate_age(date_birth_str): #funcion para calcular la edad a traves de la fecha de nacimiento
    date_birth = datetime.strptime(date_birth_str, "%Y-%m-%d").date()
    today = date.today()
    age = today.year - date_birth.year - ((today.month, today.day) < (date_birth.month, date_birth.day))
    return age

#create mechanic 
@mechanic.route('/api/add_mechanic', methods=['POST'])
def add_mechanic():
    data = request.get_json() #contiene los datos que recibimos

    
    required_fields = ['first_name', 'last_name', 'dni', 'date_of_birth', 'email', 'phone'] #verificamos si estan todos los datos requeridos
    

    if not data or not all(key in data for key in required_fields): #verificamos que todos los campos esten presentes y no vacios
        return jsonify({'error': 'Required data is missing'}), 400 

    for field in required_fields:
        if not str(data.get(field, '')).strip():  # verificamos que los campos no esten vacios
            return jsonify({'error': f'{field.title()} is required and cannot be empty'}), 400

    try:
        print(f"Data received: {data}")

        # calculamos la edad
        age_calculate = calculate_age(data['date_of_birth'])

        # creamos nuevo mecanico
        new_mechanic = Mechanic(
            data['first_name'],
            data['last_name'],
            data['dni'],
            data['date_of_birth'],
            data['email'],
            data['phone'],
            age_calculate
        )

        db.session.add(new_mechanic) #agregamos al nuevo mecanico que hemos creado
        db.session.commit() #guardamos y confirmamos los cambios en la bd
        return jsonify({
            'message': 'Mechanic successfully created',
            'mechanic': new_mechanic.serialize()
        }), 201

    except IntegrityError as e:
        db.session.rollback() #deshacemos cualquier cambio que haya hecho SQLAlchemy en la bd
        error_msg = str(e.orig).lower() #convertimos el error en un string
    #validamos que no se ingresen datos que ya existen
        if 'email' in error_msg:
            return jsonify({'error': 'The email is already registered'}), 400
        elif 'phone' in error_msg:
            return jsonify({'error': 'The phone number is already registered'}), 400
        elif 'dni' in error_msg:
            return jsonify({'error': 'The DNI is already registered'}), 400
        else:
            return jsonify({'error': 'Integrity constraint violated'}), 400

    except Exception as e: #para captar errores que pueden ocurrir (errores de conexion, logica, etc.)
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
        db.session.delete(mechanic) #eliminamos el mecanico de la bd
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
    required_fields = ['first_name', 'last_name', 'dni', 'date_of_birth', 'email', 'phone']
    for field in required_fields:
            if not str(data.get(field, '')).strip():  
                return jsonify({'error': f'{field.title()} is required and cannot be empty'}), 400

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
    except IntegrityError as e:
        db.session.rollback()
        error_msg = str(e.orig).lower()
        if 'email' in error_msg:
            return jsonify({'error': 'The email is already registered'}), 400
        elif 'phone' in error_msg:
            return jsonify({'error': 'The phone number is already registered'}), 400
        elif 'dni' in error_msg:
            return jsonify({'error': 'The DNI is already registered'}), 400
        else:
            return jsonify({'error': 'Integrity constraint violated'}), 400
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
    
    except IntegrityError as e:
            db.session.rollback()
            error_msg = str(e.orig).lower()

            if 'email' in error_msg:
                return jsonify({'error': 'The email is already registered'}), 400
            elif 'phone' in error_msg:
                return jsonify({'error': 'The phone number is already registered'}), 400
            elif 'dni' in error_msg:
                return jsonify({'error': 'The DNI is already registered'}), 400
            else:
                return jsonify({'error': 'Integrity constraint violated'}), 400

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
    

