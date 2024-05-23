import os

from flask import Flask
from flask_restful import Api

# Importing resources and handlers
from Backend.FlaskServer.api.Resources.AuthResource import Auth
from Backend.FlaskServer.api.Resources.GameResource import GameResource
from Backend.FlaskServer.api.Resources.UserResource import UserResource
from Backend.FlaskServer.db import db


def create_directory():
    # Get the directory of the current script
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    # Define the target directory relative to the base directory
    target_dir = os.path.join(base_dir, "GamesAPI", "GamesJson")

    # Check if the directory does not exist
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
        print(f"Directory '{target_dir}' created.")
    else:
        print(f"Directory '{target_dir}' already exists.")


# Creating Flask application
app = Flask(__name__)
app.secret_key = "yoav_key"
# Configuration settings
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True

# Creating RESTful API
api = Api(app)

# Creating username to ID JSON and creating test users
with app.app_context():
    db.init_app(app)
    db.create_all()
    create_directory()

# Adding resources to API routes
api.add_resource(UserResource, "/users")
api.add_resource(GameResource, "/games/<string:request_type>")
api.add_resource(Auth, "/auth")

# Running the Flask application
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
