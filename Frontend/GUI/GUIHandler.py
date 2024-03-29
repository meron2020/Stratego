import json
import sys

import pygame

from Frontend.GUI.Board import Board
from Frontend.GUI.PieceSprite import PieceSprite
from Frontend.ServerCommunications.GameHTTPHandler import GameHTTPHandler


class GUIHandler:
    def __init__(self, player_id):
        self.screen = None
        self.board = None
        self.color = (255, 255, 255)
        self.player_id = player_id
        self.in_setup_mode = True
        self.sprite_group = None
        self.game_id = None
        self.httpHandler = GameHTTPHandler("http://127.0.0.1:5000")
        self.setup_ui()
        # self.run_game_loop(self.create_player_sprites(2))

    def set_setup_mode(self, setup_mode):
        self.in_setup_mode = setup_mode

    def run_setup_loop(self, sprite_group):
        # Game loop
        running = True
        clicked_sprite = None
        bottom_rows_filled = False
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
                        self.in_setup_mode = False
                        piece_to_pos_dict = self.board.create_piece_to_pos_dict()
                        response = self.httpHandler.send_starting_positions(self.game_id, piece_to_pos_dict, 1)
                        print(response)

                elif event.type == pygame.MOUSEBUTTONUP:
                    if clicked_sprite:
                        clicked_sprite.stop_drag(2)
                        clicked_sprite = None

            # Update the clicked sprite
            if clicked_sprite:
                clicked_sprite.update()

            # Update the other sprites in the group
            for sprite in sprite_group:
                if sprite != clicked_sprite:
                    sprite.update()

            # Check if bottom four rows are filled
            if self.board.setup_rows_filled(2) and not bottom_rows_filled:
                bottom_rows_filled = True
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

            # Update the display
            pygame.display.flip()

        # Quit Pygame
        pygame.quit()
        sys.exit()

    def run_game_loop(self, sprite_group):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    clicked_piece = Board.get_clicked_sprite_and_position(sprite_group, event.pos)
                    while True:
                        return_dict = self.display_piece_options(clicked_piece)
                        if "sprite" in return_dict:
                            clicked_piece = return_dict["sprite"]
                        else:
                            # sprite.drag(pygame.mouse.get_pos())
                            self.screen.fill((255, 255, 255))

                            # Draw the board and pieces
                            self.board.draw_board()
                            sprite_group.draw(self.screen)

                            # Update the display
                            pygame.display.flip()
            self.screen.fill((255, 255, 255))

            # Draw the board and pieces
            self.board.draw_board()
            sprite_group.draw(self.screen)

            # Update the display
            pygame.display.flip()

    def setup_ui(self):
        pygame.init()

        # Initialize the screen in full-screen mode
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        pygame.display.set_caption("Stratego")

        # Create a Board instance with a fixed margin
        self.board = Board(self.screen, margin_percentage=0.05)

        # Navigate up the directory structure four times to get to the desired directory
        image_path = "C:\\Users\\yoavm\\PycharmProjects\\Stratego\\Frontend\\GUI\\Sprite_Images\\soldier.png"
        # sprite = PieceSprite(image, 1, 2, board)

    def create_player_sprites(self, player_id):
        image_path = "C:\\Users\\yoavm\\PycharmProjects\\Stratego\\Frontend\\GUI\\Sprite_Images\\soldier.png"
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
        image_path = "C:\\Users\\yoavm\\PycharmProjects\\Stratego\\Frontend\\GUI\\Sprite_Images\\soldier.png"
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
        self.get_user_piece_act(options, self.sprite_group, piece)
        return options

    def get_user_piece_act(self, options, sprite_group, piece):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    for move_option in options:
                        rect = self.board.create_square_by_row_and_column(move_option[0], move_option[1])
                        if rect.collidepoint(event.pos):
                            self.httpHandler.piece_act(self.game_id, piece.piece_id, move_option)
                            response = self.httpHandler.get_board(self.game_id)
                            self.board.piece_id_matrix = response["board"]
                            return self.create_pieces_sprites_from_get_request(response["pieces_dict"])
                    for sprite in sprite_group:
                        if sprite.piece_id / 100 == self.player_id:
                            if sprite.rect.collidepoint(event.pos):
                                return {"sprite": sprite}

        pygame.quit()
        sys.exit()
