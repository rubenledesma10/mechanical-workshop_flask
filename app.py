from flask import Flask
from config.config import DATABASE_CONNECTION_URI
from models.db import db
from routes.client_route import client_bp

app = Flask(__name__)
app.register_blueprint(client_bp)
app.config["SQLALCHEMY_DATABASE_URI"]= DATABASE_CONNECTION_URI
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

with app.app_context():
    from models.mechanic import Mechanic
    from models.Client import Client
    # db.drop_all()
    db.create_all()

if __name__ == '__main__':
    print("estoy ejecutando la aplicacion")
    app.run(debug=True)



