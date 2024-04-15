import sys

import pygame

from ScreenHandler import ScreenHandler


class SignUpPage:
    def __init__(self, screen_handler):
        self.screen_handler = screen_handler

    def create_signup_day(self):
        self.screen_handler.screen.fill(self.screen_handler.WHITE)

        # Draw title
        self.screen_handler.draw_text("Sign Up", pygame.font.Font(None, self.screen_handler.FONT_SIZE * 2),
                                      self.screen_handler.BLACK, self.screen_handler.screen,
                                      self.screen_handler.SCREEN_WIDTH // 2,
                                      self.screen_handler.SCREEN_HEIGHT // 4)

        # Input fields
        username_input = pygame.Rect(self.screen_handler.SCREEN_WIDTH // 4, self.screen_handler.SCREEN_HEIGHT // 2 - 30,
                                     self.screen_handler.SCREEN_WIDTH // 2,
                                     40)
        password_input = pygame.Rect(self.screen_handler.SCREEN_WIDTH // 4, self.screen_handler.SCREEN_HEIGHT // 2 + 30,
                                     self.screen_handler.SCREEN_WIDTH // 2,
                                     40)
        password_confirm_input = pygame.Rect(self.screen_handler.SCREEN_WIDTH // 4,
                                             self.screen_handler.SCREEN_HEIGHT // 2 + 90,
                                             self.screen_handler.SCREEN_WIDTH // 2, 40)
        pygame.draw.rect(self.screen_handler.screen, self.screen_handler.BLACK, username_input, 2)
        pygame.draw.rect(self.screen_handler.screen, self.screen_handler.BLACK, password_input, 2)
        pygame.draw.rect(self.screen_handler.screen, self.screen_handler.BLACK, password_confirm_input, 2)

        # Draw labels
        self.screen_handler.draw_text("Username:", pygame.font.Font(None, self.screen_handler.FONT_SIZE),
                                      self.screen_handler.BLACK, self.screen_handler.screen,
                                      self.screen_handler.SCREEN_WIDTH // 4 - 100,
                                      self.screen_handler.SCREEN_HEIGHT // 2 - 30)
        self.screen_handler.draw_text("Password:", pygame.font.Font(None, self.screen_handler.FONT_SIZE),
                                      self.screen_handler.BLACK, self.screen_handler.screen,
                                      self.screen_handler.SCREEN_WIDTH // 4 - 100,
                                      self.screen_handler.SCREEN_HEIGHT // 2 + 30)
        self.screen_handler.draw_text("Confirm Password:", pygame.font.Font(None, self.screen_handler.FONT_SIZE),
                                      self.screen_handler.BLACK, self.screen_handler.screen,
                                      self.screen_handler.SCREEN_WIDTH // 4 - 100,
                                      self.screen_handler.SCREEN_HEIGHT // 2 + 90)

        # Sign Up button
        signup_button = pygame.Rect(self.screen_handler.SCREEN_WIDTH // 4, self.screen_handler.SCREEN_HEIGHT // 2 + 160,
                                    self.screen_handler.SCREEN_WIDTH // 4, 50)
        pygame.draw.rect(self.screen_handler.screen, self.screen_handler.BLACK, signup_button, 2)
        self.screen_handler.draw_text("Sign Up", pygame.font.Font(None, self.screen_handler.FONT_SIZE),
                                      self.screen_handler.BLACK, self.screen_handler.screen, signup_button.centerx,
                                      signup_button.centery)

        pygame.display.flip()

        # Event handling
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if signup_button.collidepoint(mouse_pos):
                        if password == password_confirm:
                            print("Sign Up clicked")
                            print("Username:", username)
                            print("Password:", password)
                            return
                        else:
                            print("Passwords do not match")
                    elif username_input.collidepoint(mouse_pos):
                        username = self.get_text_input("Enter username:")
                    elif password_input.collidepoint(mouse_pos):
                        password = self.get_text_input("Enter password:", True)
                    elif password_confirm_input.collidepoint(mouse_pos):
                        password_confirm = self.get_text_input("Confirm password:", True)

    # Function to get text input from the user
    def get_text_input(self, prompt, password=False):
        text = ""
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        return text
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    elif event.key == pygame.K_ESCAPE:
                        return ""
                    else:
                        text += event.unicode if not password else "*"

            self.screen_handler.screen.fill(self.screen_handler.WHITE)
            self.screen_handler.draw_text(prompt, pygame.font.Font(None, self.screen_handler.FONT_SIZE),
                                          self.screen_handler.BLACK, self.screen_handler.screen,
                                          self.screen_handler.SCREEN_WIDTH // 2, self.screen_handler.SCREEN_HEIGHT // 2)
            self.screen_handler.draw_text(text, pygame.font.Font(None, self.screen_handler.FONT_SIZE),
                                          self.screen_handler.BLACK, self.screen_handler.screen,
                                          self.screen_handler.SCREEN_WIDTH // 2,
                                          self.screen_handler.SCREEN_HEIGHT // 2 + 50)
            pygame.display.flip()


if __name__ == "__main__":
    screenHandler = ScreenHandler()
    screenHandler.setup_app_infrastructure()
    signUpPage = SignUpPage(screenHandler)
    signUpPage.create_signup_day()
