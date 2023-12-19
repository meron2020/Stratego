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

    
