import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up display
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Stratego Game")

# Define colors
WHITE = (255, 255, 255)


# Define piece classes
class Piece(pygame.sprite.Sprite):
    def __init__(self, image, x, y):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load(image), (50, 75))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)


# Define piece images
soldier_image = "soldier.png"

# Create piece instances
soldier = Piece(soldier_image, 100, 100)

# Create sprite group
all_sprites = pygame.sprite.Group(soldier)

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Clear the screen
    screen.fill(WHITE)

    # Draw all sprites
    all_sprites.draw(screen)

    # Update the display
    pygame.display.flip()
