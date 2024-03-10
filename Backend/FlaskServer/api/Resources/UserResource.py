from flask_restful import reqparse, Resource

from Backend.FlaskServer.api.Models.user import UserModel


class UserResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username',
                        type=str)
    parser.add_argument("password",
                        type=str)

    @classmethod
    def get(cls):
        arguments = UserResource.parser.parse_args()
        return UserModel.get_stats(arguments["username"])

    @classmethod
    def post(cls):
        arguments = UserResource.parser.parse_args()
        return UserModel.create_new_user(arguments["username"], hash(arguments["password"]))

    @classmethod
    def delete(cls):
        arguments = UserResource.parser.parse_args()
        return UserModel.delete_user(arguments["username"])
