from models.db import db

class Car(db.Model):
    __tablename__ = "Car"
    
    id_car= db.Column(db.Integer, primary_key= True)
    brand=  db.Column(db.String(50), nullable= False)
    model= db.Column(db.String(50), nullable= False)
    year= db.Column(db.Integer, nullable= False)
    number_of_doors= db.Column(db.Integer, nullable= False)
    patent= db.Column (db.String(10),unique=True, nullable= False)
    engine= db.Column (db.String(10), nullable= False)
    valves= db.Column (db.String(10), nullable= False)
    fuel_type= db.Column (db.String(10), nullable= False)
    
    def __init__(self,brand,model,year,number_of_doors,patent,engine,valves,fuel_type):
        self.brand= brand
        self.model= model
        self.year= year
        self.number_of_doors= number_of_doors
        self.patent= patent
        self.engine= engine
        self.valves= valves
        self.fuel_type= fuel_type
        
    def serialize(self):
        return{
            'id_car': self.id_car,
            'brand': self.brand,
            'model': self.model,
            'year': self.year,
            'number_of_doors': self.number_of_doors,
            'patent': self.patent,
            'engine': self.engine,
            'valves': self.valves,
            'fuel_type': self.fuel_type
        }