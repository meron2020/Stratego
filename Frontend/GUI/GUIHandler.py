import json
import sys
import time

import pygame

from Frontend.GUI.Board import Board
from Frontend.GUI.PieceSprite import PieceSprite
from Frontend.ServerCommunications.GameHTTPHandler import GameHTTPHandler
from Frontend.GUI.PlayerHandler import PlayerHandler


class GUIHandler:
    def __init__(self):
        self.screen = None
        self.board = None
        self.color = (255, 255, 255)
        self.player_id = None
        self.in_setup_mode = True
        self.sprite_group = None
        self.game_id = None
        self.httpHandler = GameHTTPHandler("http://127.0.0.1:5000")
        self.create_game_infrastructure()
        self.player_one_handler = PlayerHandler(1, self.board, self.screen)
        self.player_two_handler = PlayerHandler(2, self.board, self.screen)
        # self.setup_ui()
        # self.run_game_loop(self.create_player_sprites(2))

    def set_setup_mode(self, setup_mode):
        self.in_setup_mode = setup_mode

    def create_game_infrastructure(self):
        pygame.init()

        # Initialize the screen in full-screen mode
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        pygame.display.set_caption("Stratego")

        # Create a Board instance with a fixed margin
        self.board = Board(self.screen, margin_percentage=0.05)

    def run_setup_loop(self):
        sprite_group = self.create_player_sprites(1)
        # Game loop
        self.player_one_handler.player_set_pieces(sprite_group)

        piece_to_pos_dict = self.board.create_piece_to_pos_dict()
        response = self.httpHandler.send_starting_positions(self.game_id, piece_to_pos_dict, 1)
        print(response)
        # Quit Pygame
        pygame.quit()
        sys.exit()

    def game_loop(self):
        self.httpHandler.get_board(self.game_id)
        self.player_one_handler.user_act()

    def run_game_loop(self):
        running = True
        possible_options = None
        clicked_piece = None
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    selected_square = self.board.get_clicked_square(
                        event.pos)  # Implement this method to get the square position
                    if not possible_options:
                        clicked_piece = Board.get_clicked_sprite_and_position(self.sprite_group, event.pos)
                    else:
                        if selected_square in possible_options:
                            self.httpHandler.piece_act(self.game_id, clicked_piece.piece_id, selected_square)
                            response = self.httpHandler.get_board(self.game_id)
                            self.board.piece_id_matrix = response["board"]
                            self.sprite_group = self.create_pieces_sprites_from_get_request(response["pieces_dict"])
                        else:
                            clicked_piece = Board.get_clicked_sprite_and_position(self.sprite_group, event.pos)

            self.screen.fill((255, 255, 255))
            self.board.draw_board()

            # Draw the pieces
            self.sprite_group.draw(self.screen)

            # Highlight possible moves if a piece is selected
            if clicked_piece:
                possible_options = self.display_piece_options(clicked_piece)

            pygame.display.flip()

    def setup_ui(self):
        pygame.init()

        # Initialize the screen in full-screen mode
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        pygame.display.set_caption("Stratego")

        # Create a Board instance with a fixed margin
        self.board = Board(self.screen, margin_percentage=0.05)

        # Navigate up the directory structure four times to get to the desired directory
        image_path = "C:\\Users\\user1\\PycharmProjects\\Stratego\\Frontend\\GUI\\Sprite_Images\\soldier.png"
        # sprite = PieceSprite(image, 1, 2, board)
        sprite_group = pygame.sprite.Group()
        for i in range(10):
            for j in range(4):
                sprite_group.add(PieceSprite(image_path, i, j - 4, self.board, self.screen, 101 + j * 10 + i, True))
        clicked_sprite = None

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # Check if any sprite is clicked
                    for sprite in sprite_group:
                        if sprite.rect.collidepoint(event.pos):
                            clicked_sprite = sprite
                            clicked_sprite.start_drag(event.pos)

                    finish_button_rect = pygame.Rect(
                        pygame.display.get_window_size()[0] - 300,
                        pygame.display.get_window_size()[1] - 150,
                        175, 50
                    )
                    if finish_button_rect.collidepoint(event.pos):
                        piece_to_pos_dict = self.board.create_piece_to_pos_dict()
                        response = self.httpHandler.send_starting_positions(self.game_id, piece_to_pos_dict, 1)
                        print(response)

                elif event.type == pygame.MOUSEBUTTONUP:
                    if clicked_sprite:
                        clicked_sprite.stop_drag(self.player_id)
                        clicked_sprite = None

            # Update the clicked sprite
            if clicked_sprite:
                clicked_sprite.update()

            # Update the other sprites in the group
            for sprite in sprite_group:
                if sprite != clicked_sprite:
                    sprite.update()

            # Check if bottom four rows are filled
            if self.board.setup_rows_filled(1):
                # Display "Finish set up" button in the bottom right corner
                finish_button_rect = pygame.Rect(
                    pygame.display.get_window_size()[0] - 300,
                    pygame.display.get_window_size()[1] - 150,
                    175, 50
                )

                pygame.draw.rect(self.screen, (0, 0, 255), finish_button_rect)
                font = pygame.font.Font(None, 36)
                text = font.render("Finish set up", True, (255, 255, 255))
                self.screen.blit(text, finish_button_rect.move(10, 5))
                pygame.display.flip()

            # sprite.drag(pygame.mouse.get_pos())
            self.screen.fill((255, 255, 255))

            # Draw the board and pieces
            self.board.draw_board()
            sprite_group.draw(self.screen)

            # Draw the square
            # screen.blit(sprite.image, sprite.rect.topleft)

            # Update the display
            pygame.display.flip()

    def await_my_turn(self):
        while True:
            my_turn = self.httpHandler.check_if_my_turn(self.game_id, self.player_id)
            if my_turn:
                return
            else:
                time.sleep(1)

    def create_player_sprites(self, player_id):
        image_path = "C:\\Users\\user1\\PycharmProjects\\Stratego\\Frontend\\GUI\\Sprite_Images\\soldier.png"
        sprite_group = pygame.sprite.Group()
        for i in range(10):
            for j in range(4):
                if player_id == 1:
                    sprite_group.add(
                        PieceSprite(image_path, i, j - 4, self.board, self.screen, player_id * 100 + 1 + j * 10 + i,
                                    True))
                else:
                    sprite_group.add(
                        PieceSprite(image_path, i, j + 10, self.board, self.screen, player_id * 100 + 1 + j * 10 + i,
                                    True))
        return sprite_group

    def create_pieces_sprites_from_get_request(self, pieces_dict):
        image_path = "C:\\Users\\user1\\PycharmProjects\\Stratego\\Frontend\\GUI\\Sprite_Images\\soldier.png"
        sprite_group = pygame.sprite.Group()
        for piece_id, piece_object in pieces_dict.items():
            piece_object = json.loads(piece_object)
            sprite_group.add(
                PieceSprite(image_path, int(piece_object["_position"][0]), int(piece_object["_position"][1]),
                            self.board, self.screen, int(piece_id), False))
        self.sprite_group = sprite_group
        return sprite_group

    def display_piece_options(self, piece):
        response = self.httpHandler.check_piece_options(self.game_id, piece.piece_id)
        options = response["piece_options"]
        for option in options:
            self.board.color_square(option, (0, 255, 0))
        # self.get_user_piece_act(options, self.sprite_group, piece)
        return options

    def get_user_piece_act(self, options, sprite_group, piece):
        move_option = self.player_one_handler.get_user_piece_act(options, sprite_group, piece)
        self.httpHandler.piece_act(self.game_id, piece.piece_id, move_option)
        response = self.httpHandler.get_board(self.game_id)
        self.board.piece_id_matrix = response["board"]
        return self.create_pieces_sprites_from_get_request(response["pieces_dict"])


if __name__ == "__main__":
    handler = GUIHandler(1)
