import sys

import pygame

from Frontend.App.ScreenHandler import ScreenHandler


class WelcomePage:
    def __init__(self, screen_handler):
        self.screen_handler = screen_handler

    def create_page(self):
        self.screen_handler.screen.fill(self.screen_handler.WHITE)

        # Draw title
        title_font = pygame.font.Font(None, self.screen_handler.FONT_SIZE * 2)
        self.screen_handler.draw_text("Welcome to Stratego", title_font, self.screen_handler.BLACK,
                                      self.screen_handler.SCREEN_WIDTH // 2, self.screen_handler.SCREEN_HEIGHT // 8)

        # Draw buttons
        signup_button_rect = self.screen_handler.draw_button("Sign Up",
                                                             pygame.font.Font(None, self.screen_handler.FONT_SIZE),
                                                             self.screen_handler.BLACK,
                                                             self.screen_handler.SCREEN_WIDTH // 4,
                                                             self.screen_handler.SCREEN_HEIGHT // 2, 300, 100)
        login_button_rect = self.screen_handler.draw_button("Login",
                                                            pygame.font.Font(None, self.screen_handler.FONT_SIZE),
                                                            self.screen_handler.BLACK,
                                                            self.screen_handler.SCREEN_WIDTH * 3 // 4,
                                                            self.screen_handler.SCREEN_HEIGHT // 2, 300, 100)

        pygame.display.flip()

        # Main loop
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left mouse button
                        mouse_pos = pygame.mouse.get_pos()
                        if signup_button_rect.collidepoint(mouse_pos):
                            return "Sign Up"
                            # Handle sign up functionality here
                        elif login_button_rect.collidepoint(mouse_pos):
                            return "Login"
                            # Handle login functionality here


if __name__ == "__main__":
    screenHandler = ScreenHandler()
    screenHandler.setup_app_infrastructure()
    appHandler = WelcomePage(screenHandler)
    appHandler.create_page()
