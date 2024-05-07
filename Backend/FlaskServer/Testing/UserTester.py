from Backend.FlaskServer.api.Users.UserHandler import UserHandler


class UserTester:
    @classmethod
    def create_users(cls):
        UserHandler.create_new_user("yoav", "meron")
        UserHandler.create_new_user("yair", "meron")

