from Backend.FlaskServer.api.Users.UserHandler import UserHandler


class UserTester:
    @classmethod
    def create_users(cls):
        UserHandler.add_user_to_u_i_json("yoav", 1)
        UserHandler.add_user_to_u_i_json("yair", 2)


UserTester.create_users()
