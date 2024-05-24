import sys

import pygame

from Frontend.App.ScreenHandler import ScreenHandler
from Frontend.ServerCommunications.UserHTTPHandler import UserHTTPHandler


class LoginPage:
    def __init__(self, screen_handler, http_handler):
        # Initialize HTTP handler
        self.http_handler = http_handler
        # Initialize ScreenHandler
        self.screen_handler = screen_handler

        # Username and password input texts
        self.username = ""
        self.password = ""

        # Flag for correct login
        self.correct_login = False

    # Main method to run the login page
    def run(self):
        # Fill the screen with white color
        self.screen_handler.screen.fill(self.screen_handler.WHITE)

        # Draw title
        title_font = pygame.font.Font(None, self.screen_handler.FONT_SIZE * 2)
        self.screen_handler.draw_text("Login", title_font, self.screen_handler.BLACK,
                                      self.screen_handler.SCREEN_WIDTH // 2, self.screen_handler.SCREEN_HEIGHT // 8)

        # Draw username field
        username_label_x = self.screen_handler.SCREEN_WIDTH // 4
        username_label_y = self.screen_handler.SCREEN_HEIGHT // 3
        self.screen_handler.draw_text("Username:", pygame.font.Font(None, self.screen_handler.FONT_SIZE),
                                      self.screen_handler.BLACK, username_label_x, username_label_y)
        username_input_rect = self.screen_handler.draw_text_input(self.screen_handler.SCREEN_WIDTH // 2,
                                                                  self.screen_handler.SCREEN_HEIGHT // 3, 400, 50,
                                                                  self.username)

        # Draw password field
        password_label_y = self.screen_handler.SCREEN_HEIGHT // 2
        self.screen_handler.draw_text("Password:", pygame.font.Font(None, self.screen_handler.FONT_SIZE),
                                      self.screen_handler.BLACK, username_label_x, password_label_y)
        password_input_rect = self.screen_handler.draw_text_input(self.screen_handler.SCREEN_WIDTH // 2,
                                                                  password_label_y, 400, 50, self.password,
                                                                  is_password=True)

        # Draw login button
        login_button_rect = self.screen_handler.draw_button("Login",
                                                            pygame.font.Font(None, self.screen_handler.FONT_SIZE),
                                                            self.screen_handler.BLACK,
                                                            self.screen_handler.SCREEN_WIDTH * 3 // 4,
                                                            self.screen_handler.SCREEN_HEIGHT * 7 // 8, 300, 100)

        # Draw back button
        back_button_rect = self.screen_handler.draw_button("Back",
                                                           pygame.font.Font(None, self.screen_handler.FONT_SIZE),
                                                           self.screen_handler.BLACK,
                                                           self.screen_handler.SCREEN_WIDTH // 4,
                                                           self.screen_handler.SCREEN_HEIGHT * 7 // 8, 300, 100)

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
                        # Handle back button click
                        if back_button_rect.collidepoint(mouse_pos):
                            print("Back button clicked")
                            return None
                        # Handle login button click
                        if login_button_rect.collidepoint(mouse_pos):
                            response = (self.http_handler.auth(self.username, self.password))
                            if response is None:
                                self.screen_handler.draw_text("Incorrect username or password",
                                                              pygame.font.Font(None, self.screen_handler.FONT_SIZE),
                                                              self.screen_handler.BLACK,
                                                              self.screen_handler.SCREEN_WIDTH // 2,
                                                              self.screen_handler.SCREEN_HEIGHT * 3 // 4)
                                pygame.display.flip()
                            else:
                                return tuple((self.username, response["PlayerId"]))

                        elif username_input_rect.collidepoint(mouse_pos):
                            print("Username input clicked")
                            # Handle username input field interaction here
                        elif password_input_rect.collidepoint(mouse_pos):
                            print("Password input clicked")
                            # Handle password input field interaction here
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        # Handle backspace key press for input fields
                        if username_input_rect.collidepoint(pygame.mouse.get_pos()):
                            self.username = self.username[:-1]
                        elif password_input_rect.collidepoint(pygame.mouse.get_pos()):
                            self.password = self.password[:-1]
                    else:
                        # Handle other key presses for input fields
                        if username_input_rect.collidepoint(pygame.mouse.get_pos()):
                            self.username += event.unicode
                        elif password_input_rect.collidepoint(pygame.mouse.get_pos()):
                            self.password += event.unicode

                    # Update the screen
                    self.screen_handler.screen.fill(self.screen_handler.WHITE)
                    self.screen_handler.draw_text("Login", title_font, self.screen_handler.BLACK,
                                                  self.screen_handler.SCREEN_WIDTH // 2,
                                                  self.screen_handler.SCREEN_HEIGHT // 8)
                    self.screen_handler.draw_text("Username:", pygame.font.Font(None, self.screen_handler.FONT_SIZE),
                                                  self.screen_handler.BLACK, username_label_x, username_label_y)
                    self.screen_handler.draw_text("Password:", pygame.font.Font(None, self.screen_handler.FONT_SIZE),
                                                  self.screen_handler.BLACK, username_label_x, password_label_y)
                    username_input_rect = self.screen_handler.draw_text_input(self.screen_handler.SCREEN_WIDTH // 2,
                                                                              self.screen_handler.SCREEN_HEIGHT // 3,
                                                                              400, 50, self.username)
                    password_input_rect = self.screen_handler.draw_text_input(self.screen_handler.SCREEN_WIDTH // 2,
                                                                              password_label_y, 400, 50, self.password,
                                                                              is_password=True)
                    self.screen_handler.draw_button("Login", pygame.font.Font(None, self.screen_handler.FONT_SIZE),
                                                    self.screen_handler.BLACK,
                                                    self.screen_handler.SCREEN_WIDTH * 3 // 4,
                                                    self.screen_handler.SCREEN_HEIGHT * 7 // 8, 300, 100)
                    self.screen_handler.draw_button("Back",
                                                    pygame.font.Font(None, self.screen_handler.FONT_SIZE),
                                                    self.screen_handler.BLACK,
                                                    self.screen_handler.SCREEN_WIDTH // 4,
                                                    self.screen_handler.SCREEN_HEIGHT * 7 // 8, 300, 100)
                    pygame.display.flip()


if __name__ == "__main__":
    # Initialize user HTTP handler with server URL
    user_http_handler = UserHTTPHandler("http://127.0.0.1:5000")
    # Initialize screen handler
    screenHandler = ScreenHandler()
    # Set up the app infrastructure (e.g., screen settings)
    screenHandler.setup_app_infrastructure()
    # Create and run the login page
    loginPage = LoginPage(screenHandler, user_http_handler)
    loginPage.run()
