from Backend.FlaskServer.api.Models.user import UserModel


def authenticate(username, password):
    user = UserModel.find_by_name(username)
    if user and user.password_hash == hash(password):
        return user
