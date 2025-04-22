from flask import Flask
from config.config import DATABASE_CONNECTION_URI
from models.db import db

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"]= DATABASE_CONNECTION_URI
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)


from routes.routes.service_routes import client  
app.register_blueprint(client, url_prefix="/service")

with app.app_context():
    from models.mechanic import Mechanic
    db.create_all()

if __name__ == '__main__':
    print("estoy ejecutando la aplicacion")
    app.run(debug=True)



