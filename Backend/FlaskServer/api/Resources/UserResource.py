import datetime

from flask_restful import reqparse, Resource

# Importing UserHandler for handling user-related operations
from Backend.FlaskServer.api.Users.UserHandler import UserHandler
from Backend.FlaskServer.authenticator import Authenticator


class UserResource(Resource):
    # RequestParser for parsing incoming request data
    parser = reqparse.RequestParser()
    # Adding arguments for username and password to the parser
    parser.add_argument('username', type=str)
    parser.add_argument("password", type=str)

    @classmethod
    #@Authenticator.jwt_required
    def get(cls):
        # Parsing the incoming request data
        arguments = UserResource.parser.parse_args()
        # Calling UserHandler to retrieve statistics for the specified user
        return UserHandler.get_stats(arguments["username"])

    @classmethod
    def post(cls):
        # Parsing the incoming request data
        arguments = UserResource.parser.parse_args()
        # Creating a new user using the provided username and password
        created_user = UserHandler.create_new_user(arguments["username"], arguments["password"])
        # If user creation is successful, return success message along with PlayerId
        if created_user:
            last_activity = datetime.datetime.utcnow().timestamp()
            #token = Authenticator.create_token(UserHandler.get_user(arguments['username']).id, last_activity)
            return {"message": "User created", "PlayerId": UserHandler.get_player_id(arguments["username"]),
                    "token": "hello"}
        else:
            # If username already exists, return error message
            return {"message": "Username already exists"}

    @classmethod
    def delete(cls):
        # Parsing the incoming request data
        arguments = UserResource.parser.parse_args()
        # Calling UserHandler to delete the specified user
        return UserHandler.delete_user(arguments["username"])
