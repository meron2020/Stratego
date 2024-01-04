from Backend.GameFunctionality.Game import Game


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

    def piece_action(self, game_id, data):
        game = self.games[game_id]
        game.piece_act(data["piece_id"], data["new_pos"])
        return game.get_board()

    def get_board(self, game_id):
        game = self.games[game_id]
        return {"pieces_dict": game.pieces_dict, "board": game.get_board()}

    @staticmethod
    def quit_game(color, game):
        result_dict = game.end_game(color)
        return result_dict

    @staticmethod
    def set_color_pieces(game, pieces_to_pos_dict):
        game.set_color_pieces(pieces_to_pos_dict)
        return True

    @staticmethod
    def check_if_player_turn(game, player_id):


    def return_piece_options(self, game_id, piece_id):
        game = self.games[game_id]
        return {"piece_id": piece_id, "possible_options": game.return_piece_options(piece_id)}

    def execute_request(self):
        request = self.request_queue.get()
        game = self.games[request.game_id]
        data_to_return = None
        if request.request_type[0] == "POST":
            
        if request.request_type[0] == "PUT":
            if request.request_type[1] == 1:
                data_to_return = game.set_color_pieces(request.data["pieces_to_pos_dict"])
            elif request.request_type[1] == 2:
                data_to_return = game.piece_act(request.data["piece_id", request.data["new_pos"]])

        if request.request_type[0] == "GET":
            if request.request_type[1] == 1:
                data_to_return = {"pieces_dict": game.pieces_dict, "board": game.get_board()}
            elif request.request_type[1] == 2:
                data_to_return =
