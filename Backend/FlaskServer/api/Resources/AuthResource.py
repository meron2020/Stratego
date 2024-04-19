from flask_restful import Resource, reqparse

from Backend.FlaskServer.api.Users.UserHandler import UserHandler
from Backend.FlaskServer.security import authenticate


class Auth(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username',
                        type=str)

    parser.add_argument('password',
                        type=str)

    @classmethod
    def post(cls):
        data = Auth.parser.parse_args()
        authenticated = authenticate(data['username'], data['password'])

        if authenticated:
            return {'message': 'User authenticated successfully.',
                    "PlayerId": UserHandler.get_player_id(data["username"])}, 201
        else:
            return {'message': "Not authenticated"}, 401
