from sqlalchemy.exc import IntegrityError 
from flask import Blueprint, jsonify, request 
from models.db import db 
from models.car import Car

car = Blueprint('car', __name__) 

@car.route('/api/cars')
def get_cars():
    car=Car.query.all() 
    if not car:
        return jsonify({'message':'There are no cars registered'}),200
    return jsonify([cars.serialize() for cars in car])

@car.route('/api/get_car/<int:id>')
def get_car_id(id):
    car=Car.query.get(id)
    if not car:
        return jsonify({'message':'Car not found'}),404
    return jsonify(car.serialize()),200

#create car 
@car.route('/api/add_car', methods=['POST'])
def add_car():
    data = request.get_json() 

    
    required_fields = ['brand', 'model', 'patent',"year","number_of_doors", 'engine', 'valves', 'fuel_type'] 
    

    if not data or not all(key in data for key in required_fields): 
        return jsonify({'error': 'Required data is missing'}), 400 

    for field in required_fields:
        if not str(data.get(field, '')).strip():  
            return jsonify({'error': f'{field.title()} is required and cannot be empty'}), 400

    try:
        print(f"Data received: {data}")
        
        new_car = Car(
            data['brand'],
            data['model'],
            data['year'],
            data['number_of_doors'],
            data['patent'],
            data['engine'],
            data['valves'],
            data['fuel_type'],
        )

        db.session.add(new_car) 
        db.session.commit() 
        return jsonify({
            'message': 'Car successfully created',
            'car': new_car.serialize()
        }), 201

    except IntegrityError as e:
        db.session.rollback() 
        error_msg = str(e.orig).lower() 
    
        if 'brand' in error_msg:
            return jsonify({'error': 'The brand is already registered'}), 400
        elif 'patent' in error_msg:
            return jsonify({'error': 'The patent number is already registered'}), 400
        elif 'model' in error_msg:
            return jsonify({'error': 'The model is already registered'}), 400
        else:
            return jsonify({'error': 'Integrity constraint violated'}), 400

    except Exception as e: 
        db.session.rollback()
        print(f"Unexpected error: {e}")
        return jsonify({'error': 'Error adding car'}), 500
        
@car.route('/api/delete_car/<int:id>', methods=['DELETE'])
def delete_car(id):
    car = Car.query.get(id)
    if not car:
        return jsonify({'message':'Car not found'}),404
    try:
        db.session.delete(car)  
        db.session.commit()
        return jsonify({'message':'Car delete successfully'}),200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error':str(e)}), 500
    
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

