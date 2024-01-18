import time

from flask import request
from flask_restful import Resource, reqparse
from werkzeug.exceptions import BadRequest
from Backend.GamesAPI.GameHandler.GameHandler import GameHandler
from Backend.FlaskServer.Models.user import UserModel
from Backend.Queues.RequestPacket import RequestPacket


class GameResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("data", type=dict)
    parser.add_argument("request_type_num", type=int)
    parser.add_argument("game_id", type=int)
    parser.add_argument("player_id", type=int)

    def __init__(self, game_handler):
        self.game_handler = game_handler

    def create_and_send_request_packet(self, request_type):
        http_request_data = GameResource.parser.parse_args()
        try:
            game_id = http_request_data.game_id
        except BadRequest:
            game_id = None
        try:
            data = http_request_data.data
        except BadRequest:
            data = None

        request_packet = RequestPacket(tuple((request_type, http_request_data.request_type_num)), request.remote_addr,
                                       http_request_data.player_id, game_id, data)
        self.request_queue.put(request_packet)
        return http_request_data

    def execute_request(self):

        request = self.request_queue.get()
        data_to_return = None
        if request.request_type[0] == "POST":
            connected = self.games[-1].connect_to_game(request.player_id)
            if not connected:
                game = self.games[self.create_game()]
                game.connect_to_game(request.player_id)
                data_to_return = {"status": "awaiting opposing player connection"}
            else:
                data_to_return = {"status": "game ready to play"}

        game = self.games[request.game_id]
        if game.check_game_still_running():
            if request.request_type[0] == "PUT":
                if request.request_type[1] == 1:
                    data_to_return = {"pieces_set": game.set_color_pieces(request.data["pieces_to_pos_dict"])}
                elif request.request_type[1] == 2:
                    action_response = game.piece_act(request.data["piece_id", request.data["new_pos"]])
                    if not action_response:
                        data_to_return = {"pieces_dict": game.pieces_dict, "board": game.get_board(), "return_type": 0}
                    else:
                        data_to_return = action_response.update({"return_type": 1})

            elif request.request_type[0] == "GET":
                if request.request_type[1] == 1:
                    data_to_return = {"pieces_dict": game.pieces_dict, "board": game.get_board()}
                elif request.request_type[1] == 2:
                    data_to_return = {"request_owner_turn": game.turn_id == request.player_id}
                elif request.request_type[1] == 3:
                    data_to_return = {"piece_options": game.return_piece_options(request.data["piece_id"])}
                elif request.request_type[1] == 4:
                    data_to_return = {"board_ready": game.board_ready_to_play()}

            elif request.request_type[0] == "DELETE":
                data_to_return = game.end_game(request.player_id)
                self.games.remove(game)
        else:
            data_to_return = {"game_status": "Ended"}

        return_packet = ResponsePacket(data_to_return, request.return_address)
        self.response_queue.put(return_packet)

    def await_response(self):
        while True:
            # Check if the queue is not empty
            if not self.response_queue.empty():
                # Get the top element without removing it
                top_response = self.response_queue.queue[0]

                # Check if the top element is what you are looking for
                if top_response.response_packet == request.remote_addr:
                    # Remove the top element from the queue
                    response = self.response_queue.get()
                    return response
                else:
                    # If the top element is not what you are looking for, wait for some time
                    time.sleep(1)
            else:
                # If the queue is empty, wait for some time
                time.sleep(1)

    def get(self):
        self.create_and_send_request_packet("GET")
        return self.await_response()

    def post(self):
        self.create_and_send_request_packet("POST")
        return self.await_response()

    def put(self):
        http_request_data = GameResource.parser.parse_args()
        game = GameHandler.get_from_json(http_request_data["game_id"])
        if http_request_data["request_type_num"] == 1:
            data_to_return = {"pieces_set": game.set_color_pieces(http_request_data["data"]["pieces_to_pos_dict"])}
        elif http_request_data["request_type_num"] == 2:
            action_response = game.piece_act(http_request_data["data"]["piece_id", http_request_data["data"]["new_pos"]])
            if not action_response:
                data_to_return = {"pieces_dict": game.pieces_dict, "board": game.get_board(), "return_type": 0}
            else:
                data_to_return = action_response.update({"return_type": 1})
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

    def delete(self):
        response = self.create_and_send_request_packet("DELETE")
        winner = UserModel.find_by_id(response.data["winner"])
        winner.add_win()
        loser = UserModel.find_by_id(response.data["loser"])
        loser.add_loss()

        if response.data.has_key("game_status"):
            return {"game_status": "Ended. You have won."}

        else:
            return {"game_status": "Ended. You have lost."}
