import sys

import pygame

from ScreenHandler import ScreenHandler


class WelcomePage:
    def __init__(self, screen_handler):
        self.screen_handler = screen_handler

    def create_page(self):
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

            self.screen_handler.screen.fill(self.screen_handler.WHITE)

            # Draw title
            self.screen_handler.draw_text("Welcome!", pygame.font.Font(None, self.screen_handler.FONT_SIZE * 2),
                                          self.screen_handler.BLACK, self.screen_handler.screen, 950, 200)

            # Draw signup button
            signup_button = pygame.Rect(1050, 400, 200, 100)
            pygame.draw.rect(self.screen_handler.screen, self.screen_handler.BLACK, signup_button, 2)
            self.screen_handler.draw_text("Sign Up", pygame.font.Font(None, self.screen_handler.FONT_SIZE),
                                          self.screen_handler.BLACK, self.screen_handler.screen, signup_button.centerx,
                                          signup_button.centery)

            # Draw login button
            login_button = pygame.Rect(650, 400, 200, 100)
            pygame.draw.rect(self.screen_handler.screen, self.screen_handler.BLACK, login_button, 2)
            self.screen_handler.draw_text("Login", pygame.font.Font(None, self.screen_handler.FONT_SIZE),
                                          self.screen_handler.BLACK, self.screen_handler.screen, login_button.centerx,
                                          login_button.centery)

            pygame.display.flip()


if __name__ == "__main__":
    screenHandler = ScreenHandler()
    screenHandler.setup_app_infrastructure()
    appHandler = WelcomePage(screenHandler)
