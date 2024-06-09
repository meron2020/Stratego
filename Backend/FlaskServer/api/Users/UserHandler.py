from Backend.FlaskServer.api.Users.User import User


class UserHandler:

    @staticmethod
    def get_player_id(username):
        # Retrieve the player ID associated with a username.
        user = User.find_by_username(username)
        return user.id

    @staticmethod
    def get_user(username):
        # Retrieve user data from a JSON file.
        return User.find_by_username(username)

    @staticmethod
    def add_win_to_user(user_id):
        # Increment the win count for a user.
        user = User.find_by_id(user_id)
        user.add_win()
        user.save_to_db()

    @staticmethod
    def add_loss_to_user(user_id):
        # Increment the loss count for a user and save user to DB.
        user = User.find_by_id(user_id)
        user.add_loss()
        user.save_to_db()

    @staticmethod
    def add_tie_to_user(user_id):
        # Increment the tie count for a user and save user to DB.
        user = User.find_by_id(user_id)
        user.add_tie()
        user.save_to_db()

    @staticmethod
    def get_stats(username):
        # Retrieve user statistics (wins, losses, ties).
        user = User.find_by_username(username)
        return {"wins": user.wins, "losses": user.losses, "ties": user.ties}

    @staticmethod
    def create_new_user(username, password):
        user = User(username, password)
        user.save_to_db()
        return True
