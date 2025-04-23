
from flask import Flask   #importamos flask
from config.config import DATABASE_CONNECTION_URI #importamos la variable de conexion a la bd
from models.db import db #importamos db que nos va a permitir definir los modelos, tablas, etc.
from routes.mechanic_routes import mechanic #importamos donde estan las rutas 
from routes.car_routes import car
from routes.service_routes import service 
from routes.client_route import client_bp

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"]= DATABASE_CONNECTION_URI
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False



app = Flask(__name__) #creamos la aplicacion
app.register_blueprint(mechanic) #registramos las rutas de mechanic a la aplicacion
app.register_blueprint(car)
app.register_blueprint(client_bp)
app.register_blueprint(service) 

app.config["SQLALCHEMY_DATABASE_URI"]= DATABASE_CONNECTION_URI #es para saber a que bd conectar y como
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False #desactivamos el sistema que rastrea automaticamente los cambios

db.init_app(app) #inicializamos SQLAlchemy con la app de Flask

with app.app_context():
    from models.mechanic import Mechanic

    from models.service import Service
    from models.car import Car

    from models.Client import Client
    # db.drop_all() #elimina todas las tablas

    db.create_all() #crea las tablas si no existen

    
if __name__ == '__main__': #ejecutamos la app en modo debug para ver errores fácilmente durante el desarrollo.
    print("bienvenido a nuestra app")
    app.run(debug=True)


