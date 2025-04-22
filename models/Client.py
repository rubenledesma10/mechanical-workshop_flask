from models.db import db

class Client(db.Model):
    __tablename__ = 'client'

    id_client = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    cuit = db.Column(db.Integer(50), unique=True, nullable=False)
    type_invoice = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    phone = db.Column(db.Integer(20), unique=True, nullable=False)
    address = db.Column(db.String(250), nullable=False)
