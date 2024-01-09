import time

from flask import request
from flask_restful import Resource, reqparse
from werkzeug.exceptions import BadRequest

from Backend.FlaskServer.Models.user import UserModel
from Backend.Queues.RequestPacket import RequestPacket


class GameResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("data", type=dict)
    parser.add_argument("request_type_num", type=int)
    parser.add_argument("game_id", type=int)
    parser.add_argument("player_id", type=int)

    def __init__(self, request_queue, response_queue):
        self.request_queue = request_queue
        self.response_queue = response_queue

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
        response = self.create_and_send_request_packet("PUT")
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
