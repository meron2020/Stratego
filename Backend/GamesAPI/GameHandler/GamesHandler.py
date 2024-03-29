import json
import os

from Backend.GamesAPI.Game.Game import Game
from Backend.GamesAPI.Game.GameBoard import GameBoard
from Backend.GamesAPI.Game.Piece import Piece


# GameHandler class handles communication between game objects and the flask resource.
class GamesHandler:
    # Put method updates the game object depending on request.
    @classmethod
    def put(cls, http_request_data):
        print("Game ID >> " + str(http_request_data["game_id"]))
        game = GamesHandler.get_from_json(http_request_data["game_id"])
        if game is not None and game.check_game_still_running():
            if http_request_data["request_type_num"] == 1:
                pieces_set = game.set_color_pieces(http_request_data["data"]["pieces_to_pos_dict"])
                GamesHandler.turn_to_json(game)
                return {"pieces_set": pieces_set}
            elif http_request_data["request_type_num"] == 2:
                action_response = game.piece_act(
                    http_request_data["data"]["piece_id"], http_request_data["data"]["new_pos"])
                if not action_response:
                    return {"pieces_dict": game.pieces_dict, "board": game.get_board(), "return_type": 0}
                else:
                    if "return_type" not in action_response:
                        return action_response.update({"return_type": 1})
                    return action_response
        return {"game_status": "Ended"}

    # Delete method ends game. This game is ended by forfeit and so it awaits opponent player checking the game state
    # to update him.
    @classmethod
    def delete(cls, game_id, player_id):
        game = GamesHandler.get_from_json(game_id)
        # If game is still running, the player is forfeiting.
        if game.check_game_still_running():
            data_to_return = game.end_game(player_id)
            return data_to_return
        # This is in case the player has forfeited after the opposing player, so he still wins.
        else:
            GamesHandler.delete_game(game_id)
            return {"game_status": "Ended", "player_status": "Won by forfeit"}

    # Post method checks if there is a game that can be connected to. If so, it connects the requesting player to
    # that game. If not, it creates a new game and connects the player to it.
    @classmethod
    def post(cls, player_id):
        game_amount = GamesHandler.current_game_amount()
        last_game = GamesHandler.get_from_json(game_amount)
        if not last_game:
            game = GamesHandler.create_game(game_amount + 1)
            game.connect_to_game(player_id)
            GamesHandler.turn_to_json(game)
            return {"status": "awaiting opposing player connection", "game_id": game_amount + 1}
        else:
            connected = last_game.connect_to_game(player_id)
            if not connected:
                game = GamesHandler.create_game(game_amount + 1)
                game.connect_to_game(player_id)
                GamesHandler.turn_to_json(game)
                return {"status": "awaiting opposing player connection", "game_id": game_amount + 1}
            else:
                GamesHandler.turn_to_json(last_game)
                return {"status": "game ready to play", "game_id": game_amount}

    # Get method runs checks get type and returns the answer accordingly.
    @classmethod
    def get(cls, game_id, request_type, player_id=None, data=None):
        game = GamesHandler.get_from_json(game_id)

        if game.check_game_still_running():
            if request_type == 1:
                pieces_dict = {}
                for piece_id, piece in game.pieces_dict.items():
                    pieces_dict[piece_id] = json.dumps(piece, default=lambda obj: obj.__dict__)
                return {"pieces_dict": pieces_dict, "board": game.get_board()}
            elif request_type == 2:
                return {"request_owner_turn": game.turn_id == player_id}
            elif request_type == 3:
                return {"piece_options": game.return_piece_options(data["piece_id"])}
            elif request_type == 4:
                if game.check_game_still_running() or game.get_state() == "Awaiting Opponent Player Connect":
                    return {"game_state": game.get_state()}
                else:
                    GamesHandler.delete_game(game_id)
                    return {"game_status": "Ended", "player_status": "Won by forfeit"}

    # Turns game object to json and writes it to database.
    @staticmethod
    def turn_to_json(game):
        object_string = json.dumps(game, default=lambda obj: obj.__dict__)
        file_path = GamesHandler.create_game_db_paths("f", game.game_id)
        with open(file_path, "w") as outfile:
            outfile.write(object_string)

        outfile.close()

    @staticmethod
    def create_game_db_paths(path_type, game_id=None):
        script_directory = os.path.dirname(os.path.abspath(__file__))

        # Go up three levels to reach the project directory
        project_directory = os.path.abspath(os.path.join(script_directory, '../../..'))
        if path_type == "f":
            relative_path = "Backend\\GamesAPI\\GamesJson\\" + str(game_id) + ".json"
        else:
            relative_path = "Backend\\GamesAPI\\GamesJson\\"
        return os.path.join(project_directory, relative_path)

    # Returns game file with parameter game_id as Game object

    @staticmethod
    def get_from_json(game_id):
        try:
            print(game_id)
            with open(GamesHandler.create_game_db_paths("f", game_id), 'r') as openfile:
                # Reading from json file
                json_object = json.load(openfile)
                game_board = GameBoard(json_object["board"]["_board_matrix"])
                pieces_dict = {}
                if "pieces_dict" in json_object:
                    for piece_num, pieceDict in json_object["pieces_dict"].items():
                        pieces_dict[piece_num] = Piece.create_piece_from_dict(pieceDict)
                    openfile.close()
                return Game(json_object["game_id"], json_object["players"], game_board, pieces_dict,
                            json_object["turn"], json_object["player_to_color_dict"], json_object["turn_id"],
                            json_object["turn_color"], json_object["game_state"], json_object["two_players_connected"])
        except OSError:
            print("Os Error")
            return False

    # Function removes game file with parameter number.
    @staticmethod
    def delete_game(game_id):
        os.remove(GamesHandler.create_game_db_paths("f", game_id))
        return True

    # Function returns the amount of games currently running.
    @classmethod
    def current_game_amount(cls):
        json_files_count = 0

        # Iterate over all files in the directory
        for filename in os.listdir(GamesHandler.create_game_db_paths("d")):
            file_path = os.path.join(GamesHandler.create_game_db_paths("d"), filename)

            # Check if it's a file and has a '.json' extension
            if os.path.isfile(file_path) and filename.endswith('.json'):
                json_files_count += 1

        return json_files_count

    # Creates game object and stores it in database. Returns the new game's id
    @staticmethod
    def create_game(game_id):
        game = Game(game_id)
        return game

    # Function iterates over database and checks for open name slot numbers.
    @staticmethod
    def check_for_open_game_slots(game_amount):
        try:
            file_number = 1
            for i in range(game_amount):
                file_name = GamesHandler.create_game_db_paths("f", file_number)

                if not os.path.exists(file_name):
                    return file_number

                file_number += 1
        except FileNotFoundError:
            print(f"Error: Directory not found at Backend\\FlaskServer\\GameDB")
            return None
