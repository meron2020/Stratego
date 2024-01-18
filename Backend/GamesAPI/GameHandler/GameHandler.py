import os

from Backend.GamesAPI.Game.Game import Game
from Backend.Queues.ResponsePacket import ResponsePacket
from Backend.GamesAPI.Game.GameBoard import GameBoard
import time
import json


class GameHandler:
    @staticmethod
    def create_game(game_id):
        game = Game(game_id)
        GameHandler.turn_to_json(game)
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

    @staticmethod
    def turn_to_json(game):
        object_string = json.dumps(game)
        with open("GamesJson/" + str(game.game_id) + ".json", "w") as outfile:
            outfile.write(object_string)

        outfile.close()

    @staticmethod
    def get_from_json(game_id):
        with open("GamesJson/" + str(game_id) + ".json", 'r') as openfile:
            # Reading from json file
            json_object = json.load(openfile)
            game_board = GameBoard(json_object["board"]["_board_matrix"])
            openfile.close()
            return Game(json_object["game_id"], game_board, json_object["pieces_dict"], json_object["turn"],
                        json_object["player_to_color_dict"], json_object["players"], json_object["turn_id"],
                        json_object["turn_color"], json_object["game_state"], json_object["two_players_connected"])

    @staticmethod
    def delete_game(game_id):
        os.remove("GamesJson/" + str(game_id) + ".json")
        return True
