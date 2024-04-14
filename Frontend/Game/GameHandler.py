import sys
import threading
import time

import pygame

from Frontend.Game.Board import Board
from Frontend.Game.PieceSprite import SpriteCreator
from Frontend.Game.PlayerHandler import PlayerHandler
from Frontend.ServerCommunications.GameHTTPHandler import GameHTTPHandler


class GameHandler:
    def __init__(self, game_id, player_id):
        self.opponent_finished_setup = False
        self.screen = None
        self.board = None
        self.player_id = player_id
        self.is_player_turn = False
        self.sprite_group = None
        self.game_id = game_id
        self.httpHandler = GameHTTPHandler("http://127.0.0.1:5000")
        self.create_game_infrastructure()
        self.player_handler = PlayerHandler(player_id, self.board, self.screen, self.httpHandler, self.game_id)

    # Function sets up the pygame underlying infrastructure for the game.
    def create_game_infrastructure(self):
        pygame.init()

        # Initialize the screen in full-screen mode
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        pygame.display.set_caption("Stratego")

        # Create a Board instance with a fixed margin
        self.board = Board(self.screen, margin_percentage=0.05)

    # Function for the setup phase of the game in which the player places his pieces in their starting positions.
    def run_setup_loop(self):
        sprite_group = SpriteCreator.create_player_sprites(self.player_id, self.board, self.screen)
        # Game loop
        self.player_handler.player_set_pieces(sprite_group)

        piece_to_pos_dict = self.board.create_piece_to_pos_dict()
        response = self.httpHandler.send_starting_positions(self.game_id, piece_to_pos_dict, self.player_id)
        print(response)

    def opponent_setup_request(self):
        while True:
            response = self.httpHandler.get_game_state(self.game_id)
            if response["game_state"] == "Awaiting Opponent Player Setup":
                time.sleep(2)
                continue
            else:
                break
        self.opponent_finished_setup = True
        return

    # Function tasked with displaying the current board setup.
    # Request is sent to the server for the board setup and the response is shown to the user.
    def display_board(self):
        response = self.httpHandler.get_board(self.game_id)
        self.board.piece_id_matrix = response["board"]
        sprite_group = SpriteCreator.create_pieces_sprites_from_get_request(response["pieces_dict"], self.board,
                                                                            self.screen, self.player_id)
        self.screen.fill((255, 255, 255))
        self.board.draw_board()
        sprite_group.draw(self.screen)

        pygame.display.flip()
        return sprite_group

    # Function that is run once the player has finished his setup. It awaits a message from the server
    # that tells it the opponent has finished his setup and the game can begin.
    def await_opponent_player_setup(self):
        # Starts thread with function that sends the server the get requests.
        check_thread = threading.Thread(target=self.opponent_setup_request)
        check_thread.daemon = True  # Daemonize the thread so it terminates when the main program exits
        check_thread.start()

        # Function for handling the pygame while awaiting the server response.
        GameHandler.event_handling_when_waiting(self.opponent_finished_setup)

    # Function to handle pygame events while awaiting players turn. Freezes the game.
    @classmethod
    def event_handling_when_waiting(cls, waiting_parameter):
        while not waiting_parameter:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    continue
        return

    # Function sends get request to server to check if it's the players turn.
    # Requests are sent once a second and once the response is True, the player_turn var is set to True and
    # the function returns.
    def await_turn_request(self):
        while True:
            my_turn = self.httpHandler.check_if_my_turn(self.game_id, self.player_id)["request_owner_turn"]
            if my_turn:
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
        GameHandler.event_handling_when_waiting(self.is_player_turn)

    def game_loop(self):
        self.run_setup_loop()
        self.await_opponent_player_setup()
        self.sprite_group = self.display_board()
        self.await_my_turn()
        running = True
        while running:
            self.sprite_group = self.display_board()
            if self.is_player_turn:
                self.get_user_piece_act()
                self.is_player_turn = False
                continue
            else:
                self.await_my_turn()
                continue

    # Function tasked with displaying a selected piece's moving options.
    # Sends get request to server and per the response, colors the board squares. Returns list of available options for
    # movement.
    def display_piece_options(self, piece):
        response = self.httpHandler.check_piece_options(self.game_id, piece.piece_id)
        options = response["piece_options"]
        for option in options:
            self.board.color_square(option, (0, 255, 0))
        return options

    # Function to handle the users action when it is the player's turn.
    # The player's action choice is sent to the server and the updated board and pieces are received.
    def get_user_piece_act(self):
        selected_square, clicked_piece = self.player_handler.user_act(self.sprite_group)
        self.httpHandler.piece_act(self.game_id, clicked_piece.piece_id, selected_square)
        response = self.httpHandler.get_board(self.game_id)
        self.board.piece_id_matrix = response["board"]
