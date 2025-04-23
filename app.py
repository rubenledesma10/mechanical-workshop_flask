
from flask import Flask
from config.config import DATABASE_CONNECTION_URI
from models.db import db
from models.service import Service
from routes.service_routes import service 


app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"]= DATABASE_CONNECTION_URI
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

app = Flask(__name__) #creamos la aplicacion
app.register_blueprint(mechanic) #registramos las rutas de mechanic a la aplicacion
app.register_blueprint(car)
app.register_blueprint(service) 
app.config["SQLALCHEMY_DATABASE_URI"]= DATABASE_CONNECTION_URI #es para saber a que bd conectar y como
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False #desactivamos el sistema que rastrea automaticamente los cambios

db.init_app(app) #inicializamos SQLAlchemy con la app de Flask

with app.app_context():
    from models.mechanic import Mechanic
    from models.service import Service
    from models.car import Car
    db.create_all()
    
if __name__ == '__main__': #ejecutamos la app en modo debug para ver errores fácilmente durante el desarrollo.
    print("estoy ejecutando la entidad mechanic")
    app.run(debug=True)


