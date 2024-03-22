import os
import sys
from Frontend.ServerCommunications.GameHTTPHandler import GameHTTPHandler
import pygame

from Testing.sprite_testing import PieceSprite
from board_test import Board

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = pygame.display.Info().current_w, pygame.display.Info().current_h

# Initialize the screen in full-screen mode
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption("Stratego")

# Create a Board instance with a fixed margin
board = Board(screen, margin_percentage=0.05)

# Create a DraggableSquare instance
square_size = board.square_size
current_script_directory = os.path.dirname(os.path.abspath(__file__))

# Navigate up the directory structure four times to get to the desired directory
four_levels_up = os.path.abspath(os.path.join(current_script_directory, '../../'))
image_path = "C:\\Users\\yoavm\\PycharmProjects\\Stratego\\Frontend\\GUI\\Sprite_Images\\soldier.png"
square_color = (255, 0, 0)  # Red
# sprite = PieceSprite(image, 1, 2, board)
sprite_group = pygame.sprite.Group()
for i in range(10):
    for j in range(4):
        sprite_group.add(PieceSprite(image_path, i, j - 4, board, screen, 100 + j*10 + i))

# sprite_group.add(sprite)
# Game loop
running = True
clicked_sprite = None

httpHandler = GameHTTPHandler("http://127.0.0.1:5000")
game_id = httpHandler.join_game(1)["game_id"]
httpHandler.join_game(2)

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
                piece_to_pos_dict = board.create_piece_to_pos_dict()
                response = httpHandler.send_starting_positions(game_id, piece_to_pos_dict, 1)
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
    if board.is_bottom_rows_filled():
        print("Bottom row filled")
        # Display "Finish set up" button in the bottom right corner
        finish_button_rect = pygame.Rect(
            pygame.display.get_window_size()[0] - 300,
            pygame.display.get_window_size()[1] - 150,
            175, 50
        )

        pygame.draw.rect(screen, (0, 0, 255), finish_button_rect)
        font = pygame.font.Font(None, 36)
        text = font.render("Finish set up", True, (255, 255, 255))
        screen.blit(text, finish_button_rect.move(10, 5))
        pygame.display.flip()

    # sprite.drag(pygame.mouse.get_pos())
    screen.fill((255, 255, 255))

    # Draw the board and pieces
    board.draw_board()
    sprite_group.draw(screen)

    # Draw the square
    # screen.blit(sprite.image, sprite.rect.topleft)

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()
