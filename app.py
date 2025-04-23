from flask import Flask
from config.config import DATABASE_CONNECTION_URI
from models.db import db
from models.service import Service
from routes.service_routes import service  

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"]= DATABASE_CONNECTION_URI
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

app.register_blueprint(service)  


with app.app_context():
    from models.mechanic import Mechanic
    from models.service import Service
    db.create_all()



if __name__ == '__main__':
    print("estoy ejecutando la aplicacion")
    app.run(debug=True)



