from models.db import db

class Client(db.Model):
    __tablename__ = 'client'

    id_client = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    cuit = db.Column(db.String(50), unique=True, nullable=False)
    type_invoice = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    phone = db.Column(db.String(20), unique=True, nullable=False)
    address = db.Column(db.String(250), nullable=False)

    def __init__(self, first_name,last_name, cuit, type_invoice, email, phone, address):
        self.first_name = first_name
        self.last_name = last_name
        self.cuit = cuit
        self.type_invoice = type_invoice
        self.email = email
        self.phone = phone
        self.address = address
        

    def serialize(self):
        return {
            'id_client': self.id_client,
            'first_name':self.first_name,
            'last_name':self.last_name,
            'cuit': self.cuit,
            'type_invoice':self.type_invoice,
            'email':self.email,
            'phone':self.phone,
            'address':self.address
        }    

