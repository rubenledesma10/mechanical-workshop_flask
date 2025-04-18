from models.db import db

class Mechanic(db.Model):
    __tablename__ = 'mechanic'

    id_mechanic= db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), unique=True, nullable=False)
    dni = db.Column(db.String(20), unique=True, nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)
    email = db.Column(db.String(20), unique=True, nullable=False)
    phone= db.Column(db.String(20), unique=True, nullable=False)
    age = db.Column(db.Integer, nullable = False)

    def __init__(self, first_name, last_name, dni,date_of_birth,email,phone,age):
        self.first_name = first_name
        self.last_name = last_name
        self.dni = dni
        self.date_of_birth=date_of_birth
        self.email=email
        self.phone=phone
        self.age=age


    def serialize(self):
        return {
            'id_mechanical': self.id_mechanic,
            'first_name':self.first_name,
            'last_name': self.last_name,
            'dni': self.dni,
            'date_of_birth':self.date_of_birth,
            'email':self.email,
            'phone':self.phone,
            'age':self.age
        }    



