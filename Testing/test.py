from Frontend.GUI.GUIHandler import GUIHandler
from Frontend.ServerCommunications.GameHTTPHandler import GameHTTPHandler

import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Set up the screen
WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dodge the Enemy")

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Player settings
player_width = 50
player_height = 50
player_x = WIDTH // 2 - player_width // 2
player_y = HEIGHT - player_height - 20
player_speed = 5

# Enemy settings
enemy_width = 50
enemy_height = 50
enemy_x = random.randint(0, WIDTH - enemy_width)
enemy_y = -enemy_height
enemy_speed = 3

# Game variables
score = 0
font = pygame.font.SysFont(None, 36)


def draw_text(text, font, color, x, y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.center = (x, y)
    screen.blit(text_surface, text_rect)


def game_over():
    draw_text("Game Over", font, RED, WIDTH // 2, HEIGHT // 2)
    draw_text("Press SPACE to play again", font, RED, WIDTH // 2, HEIGHT // 2 + 40)
    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                main()


def main():
    global player_x, player_y, enemy_x, enemy_y, score

    # Reset game variables
    score = 0
    player_x = WIDTH // 2 - player_width // 2
    player_y = HEIGHT - player_height - 20
    enemy_x = random.randint(0, WIDTH - enemy_width)
    enemy_y = -enemy_height

    clock = pygame.time.Clock()

    running = True
    while running:
        screen.fill(WHITE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player_x -= player_speed
        if keys[pygame.K_RIGHT]:
            player_x += player_speed

        # Update enemy position
        enemy_y += enemy_speed
        if enemy_y > HEIGHT:
            enemy_x = random.randint(0, WIDTH - enemy_width)
            enemy_y = -enemy_height
            score += 1

        # Check for collision
        player_rect = pygame.Rect(player_x, player_y, player_width, player_height)
        enemy_rect = pygame.Rect(enemy_x, enemy_y, enemy_width, enemy_height)
        if player_rect.colliderect(enemy_rect):
            game_over()

        # Draw player and enemy
        pygame.draw.rect(screen, GREEN, (player_x, player_y, player_width, player_height))
        pygame.draw.rect(screen, RED, (enemy_x, enemy_y, enemy_width, enemy_height))

        # Draw score
        draw_text(f"Score: {score}", font, RED, 50, 20)

        pygame.display.update()
        clock.tick(60)


if __name__ == "__main__":
    main()
