import asyncio
import sys

import pygame

from Frontend.Game.Board import Board
from Frontend.Game.PieceSprite import SpriteCreator
from Frontend.Game.PlayerHandler import PlayerHandler
from Frontend.ServerCommunications.GameHTTPHandler import GameHTTPHandler


class GameHandler:
    def __init__(self, game_id, player_id):
        self.screen = None
        self.board = None
        self.player_id = player_id
        self.is_player_turn = True
        self.sprite_group = None
        self.game_id = game_id
        self.httpHandler = GameHTTPHandler("http://127.0.0.1:5000")
        self.create_game_infrastructure()
        self.player_handler = PlayerHandler(player_id, self.board, self.screen, self.httpHandler, self.game_id)

    def create_game_infrastructure(self):
        pygame.init()

        # Initialize the screen in full-screen mode
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        pygame.display.set_caption("Stratego")

        # Create a Board instance with a fixed margin
        self.board = Board(self.screen, margin_percentage=0.05)

    def run_setup_loop(self):
        sprite_group = SpriteCreator.create_player_sprites(1, self.board, self.screen)
        # Game loop
        self.player_handler.player_set_pieces(sprite_group)

        piece_to_pos_dict = self.board.create_piece_to_pos_dict()
        response = self.httpHandler.send_starting_positions(self.game_id, piece_to_pos_dict, 1)
        print(response)
        # Quit Pygame
        pygame.quit()
        sys.exit()

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

    # Function to handle pygame events while awaiting players turn. Freezes the game.
    def await_turn_event_handling(self):
        while not self.is_player_turn:
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
    async def await_my_turn(self):
        while True:
            my_turn = self.httpHandler.check_if_my_turn(self.game_id, self.player_id)["request_owner_turn"]
            if my_turn:
                self.is_player_turn = True
                return
            else:
                await asyncio.sleep(1)

    async def game_loop(self):
        self.sprite_group = self.display_board()
        await self.await_my_turn()
        running = True
        while running:
            self.sprite_group = self.display_board()
            if self.is_player_turn:
                self.get_user_piece_act()
                self.is_player_turn = False
            else:
                asyncio.create_task(self.await_my_turn())
                self.await_turn_event_handling()
                await asyncio.sleep(0)

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


if __name__ == "__main__":
    handler = GameHandler(1)
