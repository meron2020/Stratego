from flask_restful import Resource, reqparse

# Importing UserHandler for retrieving player information and Authenticator for authentication
from Backend.FlaskServer.api.Users.UserHandler import UserHandler
from Backend.FlaskServer.authenticator import Authenticator


class Auth(Resource):
    # RequestParser for parsing incoming request data
    parser = reqparse.RequestParser()

    # Adding arguments for username and password to the parser
    parser.add_argument('username', type=str)
    parser.add_argument('password', type=str)

    def __init__(self):
        self.authenticator = Authenticator()

    def post(self):
        # Parsing the incoming request data
        data = Auth.parser.parse_args()

        # Authenticating the user using the provided username and password
        authenticated = self.authenticator.authenticate(data['username'], data['password'])

        # If user is authenticated, return success message along with PlayerId
        if authenticated:
            return {'message': 'User authenticated successfully.',
                    "PlayerId": UserHandler.get_player_id(data["username"]), "token": "hello"}, 201
        else:
            # If authentication fails, return error message
            return {'message': "Not authenticated"}, 401
