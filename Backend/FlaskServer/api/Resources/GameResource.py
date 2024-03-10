from flask_restful import Resource, reqparse
from Backend.FlaskServer.api.Models.user import UserModel


class GameResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("data", type=dict)
    parser.add_argument("request_type_num", type=int)
    parser.add_argument("game_id", type=int)
    parser.add_argument("player_id", type=int)

    def __init__(self, game_handler):
        self.game_handler = game_handler

    # HTTP Get method. According to request, uses the GameHandler to return the relevant response.
    def get(self):
        http_request_data = GameResource.parser.parse_args()
        response = self.game_handler.get(http_request_data["game_id"], http_request_data["request_type"],
                                         http_request_data["player_id", http_request_data["data"]])
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
        if response.data.has_key("return_type"):
            if response.data["return_type"] == 1:
                winner = UserModel.find_by_id(response.data["winner"])
                winner.add_win()
                loser = UserModel.find_by_id(response.data["loser"])
                loser.add_loss()
            elif response.data["return_type"] == 2:
                for player_id in response.data["player_ids"]:
                    player = UserModel.find_by_id(player_id)
                    player.add_tie()
        else:
            if response.data.has_key("game_status"):
                return {"game_status": "Ended. You have won."}

            else:
                return {"game_status": "Ended. You have lost."}
        return response

    # HTTP Delete method. Uses the GameHandler to update the relevant game and updates the UserDB.
    def delete(self):
        http_request_data = GameResource.parser.parse_args()
        response = self.game_handler.delete(http_request_data["game_id"], http_request_data["player_id"])
        winner = UserModel.find_by_id(response.data["winner"])
        winner.add_win()
        loser = UserModel.find_by_id(response.data["loser"])
        loser.add_loss()

        if response.data.has_key("game_status"):
            return {"game_status": "Ended. You have won."}

        else:
            return {"game_status": "Ended. You have lost."}
