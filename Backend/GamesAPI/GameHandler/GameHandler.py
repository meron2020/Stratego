from Backend.GamesAPI.Game.Game import Game
from Backend.Queues.ResponsePacket import ResponsePacket
import time


class GameHandler:
    def __init__(self, request_queue, response_queue):
        self.games = []
        self.request_queue = request_queue
        self.response_queue = response_queue

    def create_game(self):
        game_id = len(self.games)
        game = Game(game_id)
        self.games.append(game)
        return game_id

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

    def run_handler(self):
        while True:
            if not self.request_queue.empty():
                self.execute_request()
                continue
            else:
                time.sleep(1)
                continue
