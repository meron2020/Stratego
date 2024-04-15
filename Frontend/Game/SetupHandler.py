import threading
import time
from GameHandler import GameHandler
from PieceSprite import SpriteCreator


class SetupHandler:
    def __init__(self, player_id, screen_handler, board, game_id, player_handler, http_handler):
        self.player_id = player_id
        self.screen_handler = screen_handler
        self.board = board
        self.game_id = game_id
        self.player_handler = player_handler
        self.http_handler = http_handler
        self.opponent_finished_setup = False

    # Function for the setup phase of the game in which the player places his pieces in their starting positions.
    def run_setup_loop(self):
        sprite_group = SpriteCreator.create_player_sprites(self.player_id, self.board, self.screen_handler.screen)
        # Game loop
        self.player_handler.player_set_pieces(sprite_group)

        piece_to_pos_dict = self.board.create_piece_to_pos_dict()
        response = self.http_handler.send_starting_positions(self.game_id, piece_to_pos_dict, self.player_id)
        if response["pieces_set"]:
            return

    # Function sends request checking if the opponent has finished setting up and the game can begin.
    def opponent_setup_request(self):
        while True:
            response = self.http_handler.get_game_state(self.game_id)
            if response["game_state"] == "Awaiting Opponent Player Setup":
                time.sleep(2)
                continue
            else:
                break
        self.opponent_finished_setup = True
        return

    # Function that is run once the player has finished his setup. It awaits a message from the server
    # that tells it the opponent has finished his setup and the game can begin.
    def await_opponent_player_setup(self):
        # Starts thread with function that sends the server the get requests.
        check_thread = threading.Thread(target=self.opponent_setup_request)
        check_thread.daemon = True  # Daemonize the thread so it terminates when the main program exits
        check_thread.start()

        # Function for handling the pygame while awaiting the server response.
        while not self.opponent_finished_setup:
            GameHandler.event_handling_when_waiting()
