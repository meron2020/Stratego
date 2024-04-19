from flask_restful import reqparse, Resource

from Backend.FlaskServer.api.Users.UserHandler import UserHandler


class UserResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username',
                        type=str)
    parser.add_argument("password",
                        type=str)

    @classmethod
    def get(cls):
        arguments = UserResource.parser.parse_args()
        return UserHandler.get_stats(arguments["username"])

    @classmethod
    def post(cls):
        arguments = UserResource.parser.parse_args()
        created_user = UserHandler.create_new_user(arguments["username"], arguments["password"])
        if created_user:
            return {"message": "User created", "PlayerId": UserHandler.get_player_id(arguments["username"])}
        else:
            return {"message": "Username already exists"}

    @classmethod
    def delete(cls):
        arguments = UserResource.parser.parse_args()
        return UserHandler.delete_user(arguments["username"])
