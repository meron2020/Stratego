import threading
import time

import pygame

from Frontend.App.ScreenHandler import ScreenHandler
from Frontend.Game.PieceSprite import SpriteCreator


class PlayThroughHandler:
    def __init__(self, http_handler, board, game_id, player_handler, player_id, screen_handler):
        # Initialize the PlayThroughHandler with necessary parameters
        self.screen_handler = screen_handler
        self.game_over = False
        self.http_handler = http_handler
        self.player_id = player_id
        self.board = board
        self.game_id = game_id
        self.player_handler = player_handler
        self.is_player_turn = False
        self.sprite_group = None

    def check_if_game_over(self):
        # Check if the game is over by requesting the game state from the server
        response = self.http_handler.get_game_state(self.game_id)
        if response["game_state"] == "Awaiting opponent disconnect":
            return True
        return False

    # Function to handle the user's action when it is the player's turn.
    # The player's action choice is sent to the server and the updated board and pieces are received.
    def get_user_piece_act(self):
        # Get the selected square and the piece the player clicked on
        result = self.player_handler.user_act(self.sprite_group)
        if len(result) == 1:
            result = result[0]
            if result == "Opponent Quit":
                return True, "winner"
            else:
                return True, "loser"
        else:
            selected_square, clicked_piece = result[0], result[1]

        # Send the piece action to the server
            response = self.http_handler.piece_act(self.game_id, clicked_piece.piece_id, selected_square)

            # If the response includes an attacked piece, show the attacked piece
            if "attacked_piece" in response and response["attacked_piece"] is not None:
                self.show_attacked_piece(response["attacked_piece"], selected_square)
                time.sleep(1.5)

            # Check if the response includes a winner
            if "winner" in response:
                if response["winner"] == self.player_id:
                    return True, "winner"
                elif response["loser"] == self.player_id:
                    return True, "loser"
                else:
                    return True, "tie"

            # Update the board with the new state
            response = self.http_handler.get_board(self.game_id)
            self.board.piece_id_matrix = response["board"]
            return False, None

    # Function sends GET request to server to check if it's the player's turn.
    def await_turn_request(self):
        while True:
            # Requests are sent once every 2 seconds
            try:
                my_turn = self.http_handler.check_if_my_turn(self.game_id, self.player_id)["request_owner_turn"]
                if my_turn:
                    # Once the response is True, the player_turn variable is set to True and the function returns.
                    self.is_player_turn = True
                    return
                else:
                    time.sleep(5)
            except KeyError:
                self.game_over = True
                return

    def await_my_turn(self):
        # Start a thread with a function that sends the server the GET requests.
        check_thread = threading.Thread(target=self.await_turn_request)
        check_thread.daemon = True  # Daemonize the thread so it terminates when the main program exits
        check_thread.start()

        # Function for handling pygame events while awaiting the server response.
        while (not self.is_player_turn) and (not self.game_over):
            result = self.screen_handler.event_handling_when_waiting(True)
            if result == "Opponent Quit":
                return True
            if result is not None:
                self.http_handler.quit_game(self.game_id, self.player_id)
                return False

    # Function tasked with displaying the current board setup.
    # Request is sent to the server for the board setup and the response is shown to the user.
    def display_board(self):
        # Get the board state from the server
        self.screen_handler.create_quit_button()
        response = self.http_handler.get_board(self.game_id)
        self.board.pieces = []
        self.board.piece_id_matrix = response["board"]

        # Create sprites for the pieces on the board
        sprite_group = SpriteCreator.create_pieces_sprites_from_get_request(response["pieces_dict"], self.board,
                                                                            self.screen_handler.screen, self.player_id)
        # Fill the screen with white color
        self.screen_handler.screen.fill((255, 255, 255))

        # Draw the board and the pieces
        self.board.draw_board()
        sprite_group.draw(self.screen_handler.screen)

        self.screen_handler.present_quit_button()

        # self.screen_handler.draw_button("Quit Game",
        #                                 pygame.font.Font(None, self.screen_handler.FONT_SIZE),
        #                                 self.screen_handler.WHITE,
        #                                 self.screen_handler.SCREEN_WIDTH // 2,
        #                                 self.screen_handler.SCREEN_HEIGHT * 16 // 17, 200, 75)

        pygame.display.flip()

        self.sprite_group = sprite_group

    def show_attacked_piece(self, attacked_piece, square):
        # Show the attacked piece on the board
        folder_path = "Game/Sprite_Images/"
        file_name = attacked_piece + ".png"
        image_path = folder_path + file_name

        # Update the sprite image for the attacked piece
        for sprite_piece in self.sprite_group:
            if sprite_piece.row == square[0] and sprite_piece.column == square[1]:
                sprite_piece.image = pygame.transform.scale(pygame.image.load(image_path),
                                                            (int(self.board.square_size) - 10,
                                                             int(self.board.square_size) - 10))

        self.sprite_group.draw(self.screen_handler.screen)
        pygame.display.flip()

    def run_play_through_loop(self):
        # Main loop for the play through
        self.display_board()
        result = self.await_my_turn()
        if result is not None:
            return False, True
        if self.game_over:
            return False, False
        running = True
        while running:
            try:
                self.display_board()
            except TypeError:
                return False, True
            if self.is_player_turn:
                game_ended, result = self.get_user_piece_act()
                if game_ended:
                    return result, False
                self.is_player_turn = False
                continue
            else:
                if self.game_over:
                    return False
                result = self.await_my_turn()
                if result:
                    return True, True
                if result is not None:
                    return False, True
                continue
