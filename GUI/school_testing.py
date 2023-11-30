from PieceSprite import PieceSprite
from board import Board
import pygame

color = (255, 255, 255)
pygame.init()

screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

board = Board(screen)
board.create_board(color)

soldier_image = "Sprite_Images/soldier.png"

# Create piece instances
soldier = PieceSprite(soldier_image, 4, 4, board)

# Create sprite group
all_sprites = pygame.sprite.Group(soldier)
all_sprites.draw(screen)

pygame.display.flip()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN and event.key == pygame.K_F11:
            # Toggle fullscreen mode
            pygame.display.toggle_fullscreen()
pygame.quit()
