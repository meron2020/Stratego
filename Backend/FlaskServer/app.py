from flask import Flask
from flask_restful import Api

from Backend.FlaskServer.Resources.AuthResource import Auth
from Backend.FlaskServer.Resources.GameResource import GameResource
from Backend.FlaskServer.Resources.UserResource import UserResource
from db import db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True

api = Api(app)


# @app.before_first_request
# def create_tables():
#     db.init_app(app)
#     db.create_all()


# push context manually to app
with app.app_context():
    db.init_app(app)
    db.create_all()

# @app.route("/")
# def hello_world():
#     return "Hello, World!"


api.add_resource(UserResource, "/users")
api.add_resource(GameResource, "/games")
api.add_resource(Auth, "/auth")

if __name__ == '__main__':
    app.run(port=5000, debug=True)
