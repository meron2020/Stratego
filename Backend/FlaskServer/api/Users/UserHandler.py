import json
import os

from Backend.FlaskServer.api.Users.User import User


class UserHandler:
    @staticmethod
    def create_username_id_json():
        # Create a JSON file to store the mapping of player IDs to usernames.
        path = UserHandler.create_path_to_users_dir() + "id_to_username.json"
        with open(path, "w") as outfile:
            json_object = json.dumps({})
            outfile.write(json_object)
            return

    @staticmethod
    def create_path_to_users_dir():
        # Create the path to the directory where user JSON files are stored.
        script_directory = os.path.dirname(os.path.abspath(__file__))
        project_directory = os.path.abspath(os.path.join(script_directory, '../../..'))
        path = project_directory + "\\FlaskServer\\api\\UserJsons\\"
        return path

    @staticmethod
    def add_user_to_u_i_json(username, player_id):
        # Add a new user and their player ID to the JSON file.
        path = UserHandler.create_path_to_users_dir() + "id_to_username.json"
        # Load dict from json and add the new user
        with open(path, 'r') as openfile:
            user_to_id_dict = json.load(openfile)
            user_to_id_dict[player_id] = username
        openfile.close()
        # Save file back to DB
        with open(path, "w") as outfile:
            json_object = json.dumps(user_to_id_dict)
            outfile.write(json_object)
        outfile.close()

    @staticmethod
    def save_to_db(user):
        # Save user data to a JSON file.
        object_string = json.dumps(user, default=lambda obj: obj.__dict__)
        file_path = UserHandler.create_user_db_paths(user.username)
        with open(file_path, "w") as outfile:
            outfile.write(object_string)
        outfile.close()

    @staticmethod
    def get_player_id(username):
        # Retrieve the player ID associated with a username.
        user = UserHandler.get_user_from_json(username)
        return user.player_id

    @staticmethod
    def create_user_db_paths(username):
        # Create the file path for a user's JSON file.
        path = UserHandler.create_path_to_users_dir() + username + ".json"
        return path

    @staticmethod
    def get_user_from_json(username):
        # Retrieve user data from a JSON file.
        try:
            with open(UserHandler.create_user_db_paths(username), 'r') as openfile:
                json_object = json.load(openfile)
                return User(json_object["player_id"], json_object["username"], json_object["password"],
                            json_object["wins"],
                            json_object["losses"], json_object["ties"])
        # Return False if user does not exist
        except OSError:
            print("Os Error")
            return False

    @staticmethod
    def check_user_exists(username):
        # Check if a user exists based on their username.
        return os.path.exists(UserHandler.create_user_db_paths(username))

    @staticmethod
    def add_win_to_user(username):
        # Increment the win count for a user.
        user = UserHandler.get_user_from_json(username)
        user.add_win()
        UserHandler.save_to_db(user)

    @staticmethod
    def add_loss_to_user(username):
        # Increment the loss count for a user and save user to DB.
        user = UserHandler.get_user_from_json(username)
        user.add_loss()
        UserHandler.save_to_db(user)

    @staticmethod
    def add_tie_to_user(username):
        # Increment the tie count for a user and save user to DB.
        user = UserHandler.get_user_from_json(username)
        user.add_tie()
        UserHandler.save_to_db(user)

    @staticmethod
    def get_stats(username):
        # Retrieve user statistics (wins, losses, ties).
        user = UserHandler.get_user_from_json(username)
        return {"wins": user.wins, "losses": user.losses, "ties": user.ties}

    @staticmethod
    def create_new_user(username, password):
        # Create a new user with the provided username and password.
        path = UserHandler.create_path_to_users_dir()
        lst = os.listdir(path)
        for user_json in lst:
            if username in user_json:
                return False
        # Get the number of users in the DB.
        number_files = len(lst)
        user = User(number_files, username, password)
        UserHandler.save_to_db(user)
        UserHandler.add_user_to_u_i_json(username, number_files)
        return True

    @classmethod
    def find_by_id(cls, player_id):
        # Retrieve a username based on a player ID.
        path = UserHandler.create_path_to_users_dir() + "id_to_username.json"
        with open(path, 'r') as openfile:
            user_to_id_dict = json.load(openfile)
            username = user_to_id_dict[str(player_id)]
        openfile.close()
        return username

    @staticmethod
    def delete_user(username):
        # Delete a user and their associated JSON file.
        os.remove(UserHandler.create_user_db_paths(username))
        return True

    @staticmethod
    def check_auth(username, password):
        # Check if the provided username and password match an existing user.
        if UserHandler.check_user_exists(username):
            user = UserHandler.get_user_from_json(username)
            if user.username == username and user.password == password:
                return True
            return False
