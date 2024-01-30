from Backend.FlaskServer.Models.user import UserModel
from flask_restful import reqparse


class UserResource:
    parser = reqparse.RequestParser()
    parser.add_argument('username',
                        type=str)
    parser.add_argument("password",
                        type=str)

    @staticmethod
    def get():
        arguments = UserResource.parser.parse_args()
        return UserModel.get_stats(arguments["username"])

    @staticmethod
    def post():
        arguments = UserResource.parser.parse_args()
        return UserModel.create_new_user(arguments["username"], hash(arguments["password"]))

    @staticmethod
    def delete():
        arguments = UserResource.parser.parse_args()
        return UserModel.delete_user(arguments["username"])

