import json
import os

from Backend.FlaskServer.api.Users.User import User


class UserHandler:
    @staticmethod
    def create_username_id_json():
        path = UserHandler.create_path_to_users_dir() + "username_to_id.json"
        with open(path, "w") as outfile:
            json_object = json.dumps({})
            outfile.write(json_object)
            return

    @staticmethod
    def create_path_to_users_dir():
        script_directory = os.path.dirname(os.path.abspath(__file__))

        # Go up three levels to reach the project directory
        project_directory = os.path.abspath(os.path.join(script_directory, '../../..'))
        path = project_directory + "\\FlaskServer\\api\\UserJsons\\"
        return path

    @staticmethod
    def add_user_to_u_i_json(username, player_id):
        path = UserHandler.create_path_to_users_dir() + "username_to_id.json"
        with open(path, 'r') as openfile:
            # Reading from json file
            user_to_id_dict = json.load(openfile)
            user_to_id_dict[player_id] = username
        openfile.close()
        with open(path, "w") as outfile:
            json_object = json.dumps(user_to_id_dict)
            outfile.write(json_object)
        outfile.close()

    @staticmethod
    def save_to_db(user):
        object_string = json.dumps(user, default=lambda obj: obj.__dict__)
        file_path = UserHandler.create_user_db_paths(user.username)
        with open(file_path, "w") as outfile:
            outfile.write(object_string)

        outfile.close()

    @staticmethod
    def get_player_id(username):
        user = UserHandler.get_user_from_json(username)
        return user.player_id

    @staticmethod
    def create_user_db_paths(username):
        path = UserHandler.create_path_to_users_dir() + username + ".json"
        return path

    @staticmethod
    def get_user_from_json(username):
        try:
            with open(UserHandler.create_user_db_paths(username), 'r') as openfile:
                # Reading from json file
                json_object = json.load(openfile)
                return User(json_object["player_id"], json_object["username"], json_object["password"],
                            json_object["wins"],
                            json_object["losses"], json_object["ties"])
        except OSError:
            print("Os Error")
            return False

    @staticmethod
    def check_user_exists(username):
        return os.path.exists(UserHandler.create_user_db_paths(username))

    @staticmethod
    def add_win_to_user(username):
        user = UserHandler.get_user_from_json(username)
        user.add_win()
        UserHandler.save_to_db(user)

    @staticmethod
    def add_loss_to_user(username):
        user = UserHandler.get_user_from_json(username)
        user.add_loss()
        UserHandler.save_to_db(user)

    @staticmethod
    def add_tie_to_user(username):
        user = UserHandler.get_user_from_json(username)
        user.add_tie()
        UserHandler.save_to_db(user)

    @staticmethod
    def get_stats(username):
        user = UserHandler.get_user_from_json(username)
        return {"wins": user.wins, "losses": user.losses, "ties": user.ties}

    @staticmethod
    def create_new_user(username, password):
        path = UserHandler.create_path_to_users_dir()
        lst = os.listdir(path)  # your directory path
        for user_json in lst:
            if username in user_json:
                return False
        number_files = len(lst)
        user = User(number_files, username, password)
        UserHandler.save_to_db(user)
        UserHandler.add_user_to_u_i_json(username, number_files)
        return True

    @classmethod
    def find_by_id(cls, player_id):
        path = UserHandler.create_path_to_users_dir()
        with open(path, "r") as file:
            u_to_i_dict = json.load(file)
            return u_to_i_dict[player_id]

    @staticmethod
    def delete_user(username):
        os.remove(UserHandler.create_user_db_paths(username))
        return True

    @staticmethod
    def check_auth(username, password):
        if UserHandler.check_user_exists(username):
            user = UserHandler.get_user_from_json(username)
            if user.username == username and user.password == password:
                return True
            return False
