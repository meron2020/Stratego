from Backend.FlaskServer.api.Users.UserHandler import UserHandler


def authenticate(username, password):
    user = UserHandler.get_user_from_json(username)
    if user and user.password == password:
        return True
    return False
