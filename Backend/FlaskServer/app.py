from datetime import timedelta

from flask import Flask
from flask_restful import Api

# Importing resources and handlers
from Backend.FlaskServer.api.Resources.AuthResource import Auth
from Backend.FlaskServer.api.Resources.GameResource import GameResource
from Backend.FlaskServer.api.Resources.UserResource import UserResource
from Backend.FlaskServer.db import db

# Creating Flask application
app = Flask(__name__)
app.secret_key = "yoav_key"
# Configuration settings
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['JWT_EXPIRATION_DELTA'] = timedelta(seconds=1800)

# Creating RESTful API
api = Api(app)

# Creating username to ID JSON and creating test users
with app.app_context():
    db.init_app(app)
    db.create_all()

# Adding resources to API routes
api.add_resource(UserResource, "/users")
api.add_resource(GameResource, "/games/<string:request_type>")
api.add_resource(Auth, "/auth")

# Running the Flask application
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
