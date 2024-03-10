from bidict import bidict
from Frontend.ServerCommunications.GameHTTPHandler import GameHTTPHandler


class GameHandler:
    def __init__(self, server_address, board, game_id):
        self.game_id = game_id
        self.server_address = server_address
        self.board = board
        self.http_handler = GameHTTPHandler(self.server_address)

    def send_setup(self):
        piece_to_pos_dict = self.board.create_piece_to_pos_dict()
        params = {"game_id": self.game_id, "data": {"piece_to_pos_dict": piece_to_pos_dict}, "request_type_num": 1}
        response = self.http_handler.send_request(params)
        print(response)
