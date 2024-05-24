import sys

import pygame

from Frontend.App.ScreenHandler import ScreenHandler


class WelcomePage:
    def __init__(self, screen_handler):
        # Initialize the WelcomePage with a reference to the screen handler object
        self.screen_handler = screen_handler

    def create_page(self):
        # Fill the screen with white color, using the predefined WHITE attribute from screen handler
        self.screen_handler.screen.fill(self.screen_handler.WHITE)

        # Create the title font and draw the title on the screen
        title_font = pygame.font.Font(None, self.screen_handler.FONT_SIZE * 2)
        self.screen_handler.draw_text("Welcome to Stratego", title_font, self.screen_handler.BLACK,
                                      self.screen_handler.SCREEN_WIDTH // 2, self.screen_handler.SCREEN_HEIGHT // 8)

        # Draw the 'Sign Up' button and store its rect for click detection
        signup_button_rect = self.screen_handler.draw_button("Sign Up",
                                                             pygame.font.Font(None, self.screen_handler.FONT_SIZE),
                                                             self.screen_handler.BLACK,
                                                             self.screen_handler.SCREEN_WIDTH // 4,
                                                             self.screen_handler.SCREEN_HEIGHT // 2, 300, 100)
        # Draw the 'Login' button and store its rect for click detection
        login_button_rect = self.screen_handler.draw_button("Login",
                                                            pygame.font.Font(None, self.screen_handler.FONT_SIZE),
                                                            self.screen_handler.BLACK,
                                                            self.screen_handler.SCREEN_WIDTH * 3 // 4,
                                                            self.screen_handler.SCREEN_HEIGHT // 2, 300, 100)

        # Update the display to show all changes
        pygame.display.flip()

        # Main event loop of the welcome page
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    # If the close button is clicked, exit the game
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Check if the left mouse button was pressed
                        mouse_pos = pygame.mouse.get_pos()  # Get the position of the mouse
                        if signup_button_rect.collidepoint(mouse_pos):
                            # If 'Sign Up' button is clicked, return "Sign Up" string
                            return "Sign Up"
                        elif login_button_rect.collidepoint(mouse_pos):
                            # If 'Login' button is clicked, return "Login" string
                            return "Login"


if __name__ == "__main__":
    # If the script is run directly, initialize the screen handler and welcome page
    screenHandler = ScreenHandler()
    screenHandler.setup_app_infrastructure()
    appHandler = WelcomePage(screenHandler)
    appHandler.create_page()
