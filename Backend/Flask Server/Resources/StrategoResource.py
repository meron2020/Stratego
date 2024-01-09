from flask_restful import Resource, reqparse
from flask import Flask, request
from Backend.Queues.ResponsePacket import ResponsePacket
from Backend.Queues.RequestPacket import RequestPacket
import time


class StrategoResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("data", type=dict)
    parser.add_argument("request_type_num", type=int)
    parser.add_argument("game_id", type=int)
    parser.add_argument("player_id", type=int)

    def __init__(self, request_queue, response_queue):
        self.request_queue = request_queue
        self.response_queue = response_queue

    def create_and_send_request_packet(self, request_type):
        http_request_data = StrategoResource.parser.parse_args()
        request_packet = RequestPacket(tuple((request_type, http_request_data.request_type_num)), request.remote_addr,
                                       http_request_data.player_id, http_request_data.game_id, http_request_data.data)
        self.request_queue.put(request_packet)
        return http_request_data

    def get(self):
        self.create_and_send_request_packet("GET")
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

    def post(self):
        http_request_data = self.create_and_send_request_packet("POST")

