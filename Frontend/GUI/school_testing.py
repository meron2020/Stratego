import sys

import pygame

from Frontend.Game.PieceSprite import PieceSprite
from Frontend.Game.Board import Board

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
BOARD_SIZE = 10
SQUARE_SIZE = 50
MARGIN = 5
PIECE_POOL_WIDTH = 200
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Initialize the screen
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption("Stratego")

# Create the game board
board = Board(screen)
board.create_board(WHITE)  # Initialize the board with a background color

# Create a pool of pieces for setting up
piece_pool = []

# Create sprite groups
all_sprites = pygame.sprite.Group()
piece_pool_sprites = pygame.sprite.Group()

# Create pieces for the pool
for i in range(5):  # Assuming 5 pieces in the pool for this example
    piece = PieceSprite("C:\\Users\\yoavm\\PycharmProjects\\Stratego\\Frontend\\GUI\\Sprite_Images\\soldier.png", 0, i,
                        board, screen)  # Replace with the actual image path
    piece_pool.append(piece)
    piece_pool_sprites.add(piece)

all_sprites.add(piece_pool_sprites)

# Game loop
running = True
dragging_piece = None

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                for piece in piece_pool_sprites:
                    if piece.rect.collidepoint(event.pos):
                        dragging_piece = piece
                        dragging_piece.start_drag(event.pos)


        elif event.type == pygame.MOUSEBUTTONUP:

            if event.button == 1 and dragging_piece is not None:

                # Check if the piece is dropped on a valid board position

                for row in range(BOARD_SIZE):

                    for col in range(BOARD_SIZE):

                        if board.piece_id_matrix[row][col].colliderect(dragging_piece.rect):
                            # You may add additional logic here based on your game rules

                            dragging_piece.set_new_pos(row, col)

                dragging_piece.stop_drag()

                dragging_piece = None

        elif event.type == pygame.MOUSEMOTION:
            if dragging_piece is not None:
                dragging_piece.drag(event.rel)

        elif event.type == pygame.KEYDOWN and event.key == pygame.K_F11:
            # Toggle fullscreen mode
            pygame.display.toggle_fullscreen()

    all_sprites.update()

    # Draw the board
    board.create_board(WHITE)

    # Draw the pieces
    all_sprites.draw(screen)

    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()
