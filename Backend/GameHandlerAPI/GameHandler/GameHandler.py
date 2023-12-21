from Backend.GameFunctionality.Game import Game


class GameHandler:
    def __init__(self, request_queue):
        self.games = []
        self.request_queue = request_queue

    def create_game(self):
        game_id = len(self.games)
        game = Game(game_id)
        self.games.append(game)
        return game_id

    def piece_action(self, game_id, data):
        game = self.games[game_id]
        game.piece_act(data["piece_id"], data["new_pos"])



    
