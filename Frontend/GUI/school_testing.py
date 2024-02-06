import pygame
import time

from PieceSprite import PieceSprite
from board import Board

color = (255, 255, 255)
pygame.init()

screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

board = Board(screen)
board.create_board(color)
board.color_movement_options([(0, 0)], [(4, 4)])

soldier_image = "Sprite_Images/soldier.png"

# Create piece instances
soldier = PieceSprite(soldier_image, 4, 4, board, screen)

# Create sprite group
all_sprites = pygame.sprite.Group()
all_sprites.add(soldier)
all_sprites.draw(screen)

pygame.display.flip()

board.create_board(color)
time.sleep(1)
soldier.moveDown(1)
screen.blit(soldier.image, soldier.rect.topleft)
pygame.display.flip()

time.sleep(1)
soldier.moveLeft(1)
screen.blit(soldier.image, soldier.rect.topleft)
pygame.display.flip()

time.sleep(1)
soldier.moveUp(1)
screen.blit(soldier.image, soldier.rect.topleft)
pygame.display.flip()

time.sleep(1)
soldier.moveRight(1)
screen.blit(soldier.image, soldier.rect.topleft)
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
