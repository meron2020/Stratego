from flask_restful import Resource, reqparse

from Backend.FlaskServer.api.Users.UserHandler import UserHandler
from Backend.GamesAPI.GameHandler.GamesHandler import GamesHandler


class GameResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("data", type=dict, required=False)
    parser.add_argument("request_type_num", type=int, required=False)
    parser.add_argument("game_id", type=int, required=False)
    parser.add_argument("player_id", type=int)

    def __init__(self):
        self.game_handler = GamesHandler()

    # HTTP Get method. According to request, uses the GameHandler to return the relevant response.
    def get(self):
        http_request_data = GameResource.parser.parse_args()
        response = GamesHandler.get(http_request_data["game_id"], http_request_data["request_type_num"],
                                    http_request_data["player_id"], http_request_data["data"])
        return response

    # HTTP Post method. Uses the GameHandler to connect to an existing game or create a new game and returns response.
    def post(self):
        http_request_data = GameResource.parser.parse_args()
        response = self.game_handler.post(http_request_data["player_id"])
        return response

    # HTTP PUT Method. Updates the relevant game depending on the request and if needed the UserDB.
    def put(self):
        http_request_data = GameResource.parser.parse_args()
        response = self.game_handler.put(http_request_data)
        if "return_type" in response:
            if response["return_type"] == 1:
                winner = UserHandler.find_by_id(response.data["winner"])
                UserHandler.add_win_to_user(winner)
                loser = UserHandler.find_by_id(response.data["loser"])
                UserHandler.add_loss_to_user(loser)
            elif response["return_type"] == 2:
                for player_id in response["data"]["player_ids"]:
                    player = UserHandler.find_by_id(player_id)
                    UserHandler.add_tie_to_user(player)

        elif "game_state" in response:
            if http_request_data["player_id"] == response["winner"]:
                return {"game_status": "Ended. You have won."}
            else:
                return {"game_status": "Ended. You have lost."}
        return response

    # HTTP Delete method. Uses the GameHandler to update the relevant game and updates the UserDB.
    def delete(self):
        http_request_data = GameResource.parser.parse_args()
        response = self.game_handler.delete(http_request_data["game_id"], http_request_data["player_id"])
        winner = UserHandler.find_by_id(response.data["winner"])
        UserHandler.add_win_to_user(winner)
        loser = UserHandler.find_by_id(response.data["loser"])
        UserHandler.add_loss_to_user(loser)

        if response.data.has_key("game_status"):
            return {"game_status": "Ended. You have won."}

        else:
            return {"game_status": "Ended. You have lost."}
