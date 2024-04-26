from Backend.FlaskServer.api.Users.UserHandler import UserHandler


class Authenticator:
    @classmethod
    def authenticate(cls, username, password):
        # Retrieve user data from JSON file based on the provided username
        user = UserHandler.get_user_from_json(username)

        # Check if user exists and password matches
        if user and user.password == password:
            return True
        return False
