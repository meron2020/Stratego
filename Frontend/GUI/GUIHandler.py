import sys

import pygame

from Frontend.GUI.Board import Board
from Frontend.ServerCommunications.GameHTTPHandler import GameHTTPHandler
from Testing.sprite_testing import PieceSprite


class GUIHandler:
    def __init__(self, player_id):
        self.screen = None
        self.board = None
        self.color = (255, 255, 255)
        self.player_id = player_id
        self.game_id = None
        self.httpHandler = GameHTTPHandler("http://127.0.0.1:5000")

    def run_game_loop(self, sprite_group):
        # Game loop
        running = True
        clicked_sprite = None
        bottom_rows_filled = False
        self.game_id = self.httpHandler.join_game(1)["game_id"]

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
                        clicked_sprite.stop_drag()
                        clicked_sprite = None

            # Update the clicked sprite
            if clicked_sprite:
                clicked_sprite.update()

            # Update the other sprites in the group
            for sprite in sprite_group:
                if sprite != clicked_sprite:
                    sprite.update()

            # Check if bottom four rows are filled
            if self.board.is_bottom_rows_filled() and not bottom_rows_filled:
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
                    sprite_group.add(PieceSprite(image_path, i, j - 4, self.board, self.screen, player_id * 100 + 1 + j * 10 + i))
                else:
                    sprite_group.add(PieceSprite(image_path, i, j + 4, self.board, self.screen, player_id * 100 + 1 + j * 10 + i))
        return sprite_group
