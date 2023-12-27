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
        return game.get_board()

    def quit_game(self, player_id, game_id):
        game = self.games[game_id]
        result_dict = game.end_game()
        return result_dict

    def set_color_pieces(self, player_id, game_id):

