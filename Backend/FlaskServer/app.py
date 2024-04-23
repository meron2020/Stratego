from datetime import timedelta

from flask import Flask
from flask_restful import Api

from Backend.FlaskServer.api.Resources.AuthResource import Auth
from Backend.FlaskServer.api.Resources.GameResource import GameResource
from Backend.FlaskServer.api.Resources.UserResource import UserResource
from Backend.FlaskServer.api.Users.UserHandler import UserHandler
from Backend.FlaskServer.Testing.UserTester import UserTester


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['JWT_EXPIRATION_DELTA'] = timedelta(seconds=1800)

# app.secret_key = 'jose'
# CORS(app)
api = Api(app)
# push context manually to app
with app.app_context():
    UserHandler.create_username_id_json()
    UserTester.create_users()

api.add_resource(UserResource, "/users")
api.add_resource(GameResource, "/games")
api.add_resource(Auth, "/auth")

if __name__ == '__main__':
    app.run(port=5000, debug=False)
