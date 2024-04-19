import pygame
import sys

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FONT_SIZE = 32

# Set up the Pygame window in fullscreen mode
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
SCREEN_WIDTH, SCREEN_HEIGHT = pygame.display.get_surface().get_size()
pygame.display.set_caption("Simple App Front Page")


# Function to draw text on the screen
def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect()
    text_rect.center = (x, y)
    surface.blit(text_obj, text_rect)


# Function to get text input from the user
def get_text_input(prompt):
    text = ""
    active = True
    while active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    active = False
                elif event.key == pygame.K_BACKSPACE:
                    text = text[:-1]
                elif event.key == pygame.K_ESCAPE:
                    return ""
                else:
                    text += event.unicode

        screen.fill(WHITE)
        draw_text(prompt, pygame.font.Font(None, FONT_SIZE), BLACK, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50)
        draw_text(text, pygame.font.Font(None, FONT_SIZE), BLACK, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        pygame.display.flip()

    return text


# Main loop
def main():
    signup_mode = False
    username = ""
    password = ""
    confirm_password = ""

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if signup_button.collidepoint(mouse_pos):
                    signup_mode = True
                elif login_button.collidepoint(mouse_pos):
                    if signup_mode:
                        if password == confirm_password:
                            print("Sign Up clicked")
                            print("Username:", username)
                            print("Password:", password)
                            signup_mode = False
                        else:
                            print("Passwords do not match")
                    else:
                        print("Login clicked")
                        # Handle login functionality here

        screen.fill(WHITE)

        # Draw title
        draw_text("Welcome!", pygame.font.Font(None, FONT_SIZE * 2), BLACK, screen, SCREEN_WIDTH // 2,
                  SCREEN_HEIGHT // 4)

        if signup_mode:
            # Username input
            username_prompt = "Enter username:"
            username = get_text_input(username_prompt)

            # Password input
            password_prompt = "Enter password:"
            password = get_text_input(password_prompt)

            # Confirm Password input
            confirm_password_prompt = "Confirm password:"
            confirm_password = get_text_input(confirm_password_prompt)

            # Draw signup button
            signup_button_text = "Sign Up"
        else:
            # Draw login button
            signup_button_text = "Sign Up" if signup_mode else "Login"

        signup_button = pygame.Rect(SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2, SCREEN_WIDTH // 4, SCREEN_HEIGHT // 8)
        pygame.draw.rect(screen, BLACK, signup_button, 2)
        draw_text(signup_button_text, pygame.font.Font(None, FONT_SIZE), BLACK, screen, signup_button.centerx,
                  signup_button.centery)

        login_button = pygame.Rect(SCREEN_WIDTH // 2 + SCREEN_WIDTH // 8, SCREEN_HEIGHT // 2, SCREEN_WIDTH // 4,
                                   SCREEN_HEIGHT // 8)
        pygame.draw.rect(screen, BLACK, login_button, 2)
        draw_text("Login", pygame.font.Font(None, FONT_SIZE), BLACK, screen, login_button.centerx, login_button.centery)

        pygame.display.flip()


if __name__ == "__main__":
    print(hash("yoav"))
