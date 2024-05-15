from flask_restful import Resource, reqparse

# Importing UserHandler for handling user-related operations
from Backend.FlaskServer.api.Users.UserHandler import UserHandler
from Backend.FlaskServer.authenticator import Authenticator
# Importing GamesHandler for handling game-related operations
from Backend.GamesAPI.GameHandler.GamesHandler import GamesHandler


class GameResource(Resource):
    # RequestParser for parsing incoming request data
    parser = reqparse.RequestParser()
    # Adding arguments for various data related to the game
    parser.add_argument("data", type=dict, required=False)
    parser.add_argument("game_id", type=int, required=False)
    parser.add_argument("player_id", type=int)

    def __init__(self):
        # Initializing GamesHandler instance to handle game-related operations
        self.game_handler = GamesHandler()

    # HTTP Get method. Retrieves game-related information based on the request.
    def get(self, request_type):
        # Parsing the incoming request data
        http_request_data = GameResource.parser.parse_args()
        # Calling GamesHandler to process the GET request and return the response
        response = GamesHandler.get(http_request_data["game_id"], request_type,
                                    http_request_data["player_id"], http_request_data["data"])
        return response

    # HTTP Post method. Handles the creation or connection of a game.
    def post(self, request_type):
        # Parsing the incoming request data
        http_request_data = GameResource.parser.parse_args()
        # Calling GamesHandler to process the POST request and return the response
        response = self.game_handler.post(http_request_data["player_id"])
        return response

    # HTTP PUT Method. Updates game state and possibly user information.
    def put(self, request_type):
        # Parsing the incoming request data
        http_request_data = GameResource.parser.parse_args()
        # Calling GamesHandler to process the PUT request and return the response
        response = self.game_handler.put(http_request_data, request_type)

        # Handling additional actions based on the response
        if "return_type" in response:
            if response["return_type"] == 1:
                # Updating user information in case of a win
                UserHandler.add_win_to_user(response["winner"])
                UserHandler.add_loss_to_user(response["loser"])
            elif response["return_type"] == 2:
                # Updating user information in case of a tie
                for player_id in response["data"]["player_ids"]:
                    UserHandler.add_tie_to_user(player_id)
        elif "game_state" in response:
            # Handling game end state
            if http_request_data["player_id"] == response["winner"]:
                return {"game_status": "Ended. You have won."}
            else:
                return {"game_status": "Ended. You have lost."}
        return response

    # HTTP Delete method. Handles deletion of a game and updates user information.
    def delete(self, request_type):
        # Parsing the incoming request data
        http_request_data = GameResource.parser.parse_args()
        # Calling GamesHandler to process the DELETE request and return the response
        response = self.game_handler.delete(http_request_data["game_id"], http_request_data["player_id"])

        # Updating user information based on game outcome
        winner = UserHandler.find_by_id(response.data["winner"])
        UserHandler.add_win_to_user(winner)
        loser = UserHandler.find_by_id(response.data["loser"])
        UserHandler.add_loss_to_user(loser)

        # Handling game end state
        if response.data.has_key("game_status"):
            return {"game_status": "Ended. You have won."}
        else:
            return {"game_status": "Ended. You have lost."}
