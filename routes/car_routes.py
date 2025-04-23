from sqlalchemy.exc import IntegrityError #para capturar errores en la bd
from flask import Blueprint, jsonify, request #blueprint -> modularizar las rutas, jsonify ->para convertir a json, request->para acceder a los datos que llegan en la solicitud
from models.db import db #para hacer las operaciones en la bd
from models.car import Car
from datetime import datetime, date #para manejar fechas y calcular edad


car = Blueprint('car', __name__) #creamos blueprint

#get all cars
@car.route('/api/car')
def get_cars():
    car=Car.query.all() #llamamos a todos los mecanicos que hay en la bd
    if not car:
        return jsonify({'message':'There are no mechanics registered'}),200
    return jsonify([cars.serialize() for cars in car])

#get car by id
@car.route('/api/get_car/<int:id>')
def get_car_id(id):
    car=Car.query.get(id)
    if not car:
        return jsonify({'message':'Car not found'}),404
    return jsonify(car.serialize()),200

#create car 
@car.route('/api/add_car', methods=['POST'])
def add_car():
    data = request.get_json() #contiene los datos que recibimos

    
    required_fields = ['brand', 'model', 'patent', 'engine', 'valves', 'fuel_type'] #verificamos si estan todos los datos requeridos
    

    if not data or not all(key in data for key in required_fields): #verificamos que todos los campos esten presentes y no vacios
        return jsonify({'error': 'Required data is missing'}), 400 

    for field in required_fields:
        if not str(data.get(field, '')).strip():  # verificamos que los campos no esten vacios
            return jsonify({'error': f'{field.title()} is required and cannot be empty'}), 400

    try:
        print(f"Data received: {data}")

        # creamos nuevo auto
        new_car = Car(
            data['brand'],
            data['model'],
            data['patent'],
            data['engine'],
            data['valves'],
            data['fuel_type'],
        )

        db.session.add(new_car) #agregamos al nuevo mecanico que hemos creado
        db.session.commit() #guardamos y confirmamos los cambios en la bd
        return jsonify({
            'message': 'Car successfully created',
            'mechanic': new_car.serialize()
        }), 201

    except IntegrityError as e:
        db.session.rollback() #deshacemos cualquier cambio que haya hecho SQLAlchemy en la bd
        error_msg = str(e.orig).lower() #convertimos el error en un string
    #validamos que no se ingresen datos que ya existen
        if 'brand' in error_msg:
            return jsonify({'error': 'The brand is already registered'}), 400
        elif 'patent' in error_msg:
            return jsonify({'error': 'The patent number is already registered'}), 400
        elif 'model' in error_msg:
            return jsonify({'error': 'The model is already registered'}), 400
        else:
            return jsonify({'error': 'Integrity constraint violated'}), 400

    except Exception as e: #para captar errores que pueden ocurrir (errores de conexion, logica, etc.)
        db.session.rollback()
        print(f"Unexpected error: {e}")
        return jsonify({'error': 'Error adding car'}), 500
        
#delete car
@car.route('/api/delete_car/<int:id>', methods=['DELETE'])
def delete_car(id):
    car = Car.query.get(id)
    if not car:
        return jsonify({'message':'Car not found'}),404
    try:
        db.session.delete(car) #eliminamos el auto de la bd     
        db.session.commit()
        return jsonify({'message':'Car delete successfully'}),200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error':str(e)}), 500
    
#edit car
@car.route('/api/edit_car/<int:id>', methods=['PUT'])
def edit_car(id):
    data=request.get_json()
    if not data:
        return jsonify({'error':'No data received'}, 400)
    
    car = Car.query.get(id)
    if not car:
        return jsonify({'message':'Car not found'}),404
    required_fields = ['brand', 'model', 'patent', 'engine', 'valves', 'fuel_type']
    for field in required_fields:
            if not str(data.get(field, '')).strip():  
                return jsonify({'error': f'{field.title()} is required and cannot be empty'}), 400

    try:
        if 'brand' in data:
            car.brand=data['brand']
        if 'model' in data:
            car.model=data['model']
        if 'year' in data:
            car.year=data['year']
        if 'number_of_doors' in data:
            car.number_of_doors=data['number_of_doors']
        if 'patent' in data:
            car.patent=data['patent']
        if 'engine' in data:
            car.engine=data['engine']
        if 'valves' in data:
            car.valves=data['valves']
        if 'fuel_type' in data:
            car.fuel_type=data['fuel_type']
        db.session.commit()
        return jsonify({'message':'Car updated correctly','car':car.serialize()}),200
    except IntegrityError as e:
        db.session.rollback()
        error_msg = str(e.orig).lower()
        if 'brand' in error_msg:
            return jsonify({'error': 'The brand is already registered'}), 400
        elif 'model' in error_msg:
            return jsonify({'error': 'The model is already registered'}), 400
        elif 'year' in error_msg:
            return jsonify({'error': 'The year is already registered'}), 400
        else:
            return jsonify({'error': 'Integrity constraint violated'}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
    
#edit a car attribute
@car.route('/api/update_car/<int:id>', methods=['PATCH'])
def update_car(id):
    data=request.get_json()
    if not data:
        return jsonify({'error':'No data received'}, 400)
    car = Car.query.get(id)
    if not car:
        return jsonify({'message':'Car not found'}),404
    
    try:
        if 'brand' in data:
            car.brand=data['brand']
        if 'model' in data:
            car.model=data['model']
        if 'year' in data:
            car.year=data['year']
        if 'number_of_doors' in data:
            car.number_of_doors=data['number_of_doors']
        if 'patent' in data:
            car.patent=data['patent']
        if 'engine' in data:
            car.engine=data['engine']
        if 'valves' in data:
            car.valves=data['valves']
        if 'fuel_type' in data:
            car.fuel_type=data['fuel_type']
        db.session.commit()
        return jsonify({'message':'Car updated correctly','car':car.serialize()}),200
    
    except IntegrityError as e:
            db.session.rollback()
            error_msg = str(e.orig).lower()

            if 'brand' in error_msg:
                return jsonify({'error': 'The brand is already registered'}), 400
            elif 'model' in error_msg:
                return jsonify({'error': 'The model number is already registered'}), 400
            elif 'year' in error_msg:
                return jsonify({'error': 'The year is already registered'}), 400
            else:
                return jsonify({'error': 'Integrity constraint violated'}), 400

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
