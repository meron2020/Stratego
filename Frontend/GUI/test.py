import sys

import pygame

pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FONT_SIZE = 32

# Set up the Pygame window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Simple App Front Page")

# Function to draw text on the screen
def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect()
    text_rect.center = (x, y)
    surface.blit(text_obj, text_rect)

# Main loop
def main():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if signup_button.collidepoint(mouse_pos):
                    print("Sign Up clicked")
                elif login_button.collidepoint(mouse_pos):
                    print("Login clicked")

        screen.fill(WHITE)

        # Draw title
        draw_text("Welcome!", pygame.font.Font(None, FONT_SIZE * 2), BLACK, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4)

        # Draw signup button
        signup_button = pygame.Rect(SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2, SCREEN_WIDTH // 4, SCREEN_HEIGHT // 8)
        pygame.draw.rect(screen, BLACK, signup_button, 2)
        draw_text("Sign Up", pygame.font.Font(None, FONT_SIZE), BLACK, screen, signup_button.centerx, signup_button.centery)

        # Draw login button
        login_button = pygame.Rect(SCREEN_WIDTH // 2 + SCREEN_WIDTH // 8, SCREEN_HEIGHT // 2, SCREEN_WIDTH // 4, SCREEN_HEIGHT // 8)
        pygame.draw.rect(screen, BLACK, login_button, 2)
        draw_text("Login", pygame.font.Font(None, FONT_SIZE), BLACK, screen, login_button.centerx, login_button.centery)

        pygame.display.flip()

if __name__ == "__main__":
    main()