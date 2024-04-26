import threading
import time

import pygame

from Frontend.App.ScreenHandler import ScreenHandler
from Frontend.Game.PieceSprite import SpriteCreator


class PlayThroughHandler:
    def __init__(self, http_handler, board, game_id, player_handler, player_id, screen):
        self.screen = screen
        self.http_handler = http_handler
        self.player_id = player_id
        self.board = board
        self.game_id = game_id
        self.player_handler = player_handler
        self.is_player_turn = False
        self.sprite_group = None

    # Function tasked with displaying a selected piece's moving options.
    # Sends get request to server and per the response, colors the board squares. Returns list of available options for
    # movement.
    def display_piece_options(self, piece):
        response = self.http_handler.check_piece_options(self.game_id, piece.piece_id)
        options = response["piece_options"]
        for option in options:
            self.board.color_square(option, (0, 255, 0))
        return options

    def set_sprite_group(self, sprite_group):
        self.sprite_group = sprite_group

    # Function to handle the users action when it is the player's turn.
    # The player's action choice is sent to the server and the updated board and pieces are received.
    def get_user_piece_act(self):
        selected_square, clicked_piece = self.player_handler.user_act(self.sprite_group)
        response = self.http_handler.piece_act(self.game_id, clicked_piece.piece_id, selected_square)
        if "winner" in response:
            if response["winner"] == self.player_id:
                return True, "winner"
            elif response["loser"] == self.player_id:
                return True, "loser"
            else:
                return True, "tie"
        response = self.http_handler.get_board(self.game_id)
        self.board.piece_id_matrix = response["board"]
        return False, None

    # Function sends get request to server to check if it's the players turn.
    def await_turn_request(self):
        while True:
            # Requests are sent once a second
            my_turn = self.http_handler.check_if_my_turn(self.game_id, self.player_id)["request_owner_turn"]
            if my_turn:
                # once the response is True, the player_turn var is set to True and the function returns.
                self.is_player_turn = True
                return
            else:
                time.sleep(2)

    def await_my_turn(self):
        # Starts thread with function that sends the server the get requests.
        check_thread = threading.Thread(target=self.await_turn_request)
        check_thread.daemon = True  # Daemonize the thread so it terminates when the main program exits
        check_thread.start()

        # Function for handling the pygame while awaiting the server response.
        while not self.is_player_turn:
            ScreenHandler.event_handling_when_waiting()

    # Function tasked with displaying the current board setup.
    # Request is sent to the server for the board setup and the response is shown to the user.
    def display_board(self):
        response = self.http_handler.get_board(self.game_id)
        self.board.pieces = []
        self.board.piece_id_matrix = response["board"]
        sprite_group = SpriteCreator.create_pieces_sprites_from_get_request(response["pieces_dict"], self.board,
                                                                            self.screen, self.player_id)
        self.screen.fill((255, 255, 255))
        self.board.draw_board()
        sprite_group.draw(self.screen)

        pygame.display.flip()

        self.sprite_group = sprite_group

    def run_play_through_loop(self):
        self.display_board()
        self.await_my_turn()
        running = True
        while running:
            self.display_board()
            if self.is_player_turn:
                game_ended, result = self.get_user_piece_act()
                if game_ended:
                    return result
                self.is_player_turn = False
                continue
            else:
                self.await_my_turn()
                continue
