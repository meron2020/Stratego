import sys

import pygame

from Frontend.App.ScreenHandler import ScreenHandler
from Frontend.ServerCommunications.UserHTTPHandler import UserHTTPHandler


class SignUpPage:
    def __init__(self, screen_handler, user_http_handler):
        self.screen_handler = screen_handler
        self.user_http_handler = user_http_handler

    def run(self):
        username = ""
        password = ""
        password_confirm = ""
        self.screen_handler.screen.fill(self.screen_handler.WHITE)

        # Draw title
        title_font = pygame.font.Font(None, self.screen_handler.FONT_SIZE * 2)
        self.screen_handler.draw_text("Sign Up", title_font, self.screen_handler.BLACK,
                                      self.screen_handler.SCREEN_WIDTH // 2, self.screen_handler.SCREEN_HEIGHT // 8)

        # Draw username field
        username_label_x = self.screen_handler.SCREEN_WIDTH // 4
        username_label_y = self.screen_handler.SCREEN_HEIGHT // 3
        self.screen_handler.draw_text("Username:", pygame.font.Font(None, self.screen_handler.FONT_SIZE),
                                      self.screen_handler.BLACK, username_label_x, username_label_y)

        username_input_rect = self.screen_handler.draw_text_input(self.screen_handler.SCREEN_WIDTH // 2,
                                                                  self.screen_handler.SCREEN_HEIGHT // 3,
                                                                  400, 50,
                                                                  username)

        # Draw password field
        password_label_y = self.screen_handler.SCREEN_HEIGHT // 2
        self.screen_handler.draw_text("Password:", pygame.font.Font(None, self.screen_handler.FONT_SIZE),
                                      self.screen_handler.BLACK, username_label_x, password_label_y)
        password_input_rect = self.screen_handler.draw_text_input(self.screen_handler.SCREEN_WIDTH // 2,
                                                                  password_label_y, 400, 50, password,
                                                                  is_password=True)

        # Draw password confirmation field
        password_confirm_label_y = self.screen_handler.SCREEN_HEIGHT * 2 // 3
        self.screen_handler.draw_text("Confirm Password:", pygame.font.Font(None, self.screen_handler.FONT_SIZE),
                                      self.screen_handler.BLACK, username_label_x, password_confirm_label_y)
        password_confirm_input_rect = self.screen_handler.draw_text_input(self.screen_handler.SCREEN_WIDTH // 2,
                                                                          password_confirm_label_y, 400, 50,
                                                                          password_confirm, is_password=True)

        # Draw buttons
        back_button_rect = self.screen_handler.draw_button("Back",
                                                           pygame.font.Font(None, self.screen_handler.FONT_SIZE),
                                                           self.screen_handler.BLACK,
                                                           self.screen_handler.SCREEN_WIDTH // 4,
                                                           self.screen_handler.SCREEN_HEIGHT * 7 // 8, 300, 100)
        signup_button_rect = self.screen_handler.draw_button("Sign Up",
                                                             pygame.font.Font(None, self.screen_handler.FONT_SIZE),
                                                             self.screen_handler.BLACK,
                                                             self.screen_handler.SCREEN_WIDTH * 3 // 4,
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
                        if back_button_rect.collidepoint(mouse_pos):
                            print("Back button clicked")
                            return None
                            # Handle going back to the welcome page
                        elif signup_button_rect.collidepoint(mouse_pos):
                            print("Sign Up button clicked")
                            if password == password_confirm:
                                response = self.user_http_handler.create_user(username, password)
                                if response["message"] == "User created":
                                    return tuple((username, response["PlayerId"]))
                                else:
                                    self.screen_handler.draw_text("Username already exists",
                                                                  pygame.font.Font(None, self.screen_handler.FONT_SIZE),
                                                                  self.screen_handler.BLACK,
                                                                  self.screen_handler.SCREEN_WIDTH // 2,
                                                                  self.screen_handler.SCREEN_HEIGHT * 3 // 4)
                                    pygame.display.flip()
                            # Handle sign up functionality here
                        elif username_input_rect.collidepoint(mouse_pos):
                            print("Username input clicked")
                            # Handle input field interaction here
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        if username_input_rect.collidepoint(pygame.mouse.get_pos()):
                            username = username[:-1]
                        elif password_input_rect.collidepoint(pygame.mouse.get_pos()):
                            password = password[:-1]
                        elif password_confirm_input_rect.collidepoint(pygame.mouse.get_pos()):
                            password_confirm = password_confirm[:-1]
                    else:
                        if username_input_rect.collidepoint(pygame.mouse.get_pos()):
                            username += event.unicode
                        elif password_input_rect.collidepoint(pygame.mouse.get_pos()):
                            password += event.unicode
                        elif password_confirm_input_rect.collidepoint(pygame.mouse.get_pos()):
                            password_confirm += event.unicode

                    # Update the screen
                    self.screen_handler.screen.fill(self.screen_handler.WHITE)
                    self.screen_handler.draw_text("Sign Up", title_font, self.screen_handler.BLACK,
                                                  self.screen_handler.SCREEN_WIDTH // 2,
                                                  self.screen_handler.SCREEN_HEIGHT // 8)
                    self.screen_handler.draw_text("Username:",
                                                  pygame.font.Font(None, self.screen_handler.FONT_SIZE),
                                                  self.screen_handler.BLACK, username_label_x, username_label_y)
                    self.screen_handler.draw_text("Password:",
                                                  pygame.font.Font(None, self.screen_handler.FONT_SIZE),
                                                  self.screen_handler.BLACK, username_label_x, password_label_y)
                    self.screen_handler.draw_text("Confirm Password:",
                                                  pygame.font.Font(None, self.screen_handler.FONT_SIZE),
                                                  self.screen_handler.BLACK, username_label_x,
                                                  password_confirm_label_y)
                    username_input_rect = self.screen_handler.draw_text_input(
                        self.screen_handler.SCREEN_WIDTH // 2, self.screen_handler.SCREEN_HEIGHT // 3, 400, 50,
                        username)
                    password_input_rect = self.screen_handler.draw_text_input(
                        self.screen_handler.SCREEN_WIDTH // 2, password_label_y, 400, 50, password,
                        is_password=True)
                    password_confirm_input_rect = self.screen_handler.draw_text_input(
                        self.screen_handler.SCREEN_WIDTH // 2, password_confirm_label_y, 400, 50,
                        password_confirm, is_password=True)
                    self.screen_handler.draw_button("Back",
                                                    pygame.font.Font(None, self.screen_handler.FONT_SIZE),
                                                    self.screen_handler.BLACK,
                                                    self.screen_handler.SCREEN_WIDTH // 4,
                                                    self.screen_handler.SCREEN_HEIGHT * 7 // 8, 300, 100)
                    self.screen_handler.draw_button("Sign Up",
                                                    pygame.font.Font(None, self.screen_handler.FONT_SIZE),
                                                    self.screen_handler.BLACK,
                                                    self.screen_handler.SCREEN_WIDTH * 3 // 4,
                                                    self.screen_handler.SCREEN_HEIGHT * 7 // 8, 300, 100)
                    pygame.display.flip()


if __name__ == "__main__":
    httpHandler = UserHTTPHandler("http://127.0.0.1:5000")
    screenHandler = ScreenHandler()
    screenHandler.setup_app_infrastructure()
    signUpPage = SignUpPage(screenHandler, httpHandler)
    signUpPage.run()
