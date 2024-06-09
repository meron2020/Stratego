import sys

import pygame

from Frontend.App.ScreenHandler import ScreenHandler
from Frontend.ServerCommunications.UserHTTPHandler import UserHTTPHandler


class OptionsPage:
    def __init__(self, screen_handler):
        # Initialize the screen handler
        self.screen_handler = screen_handler

    # Main method to run the options page
    def run(self):
        # Fill the screen with white color
        self.screen_handler.screen.fill(self.screen_handler.WHITE)

        # Draw title
        title_font = pygame.font.Font(None, self.screen_handler.FONT_SIZE * 2)
        self.screen_handler.draw_text("Options", title_font, self.screen_handler.BLACK,
                                      self.screen_handler.SCREEN_WIDTH // 2, self.screen_handler.SCREEN_HEIGHT // 8)

        # Draw "Join Game" button
        join_game_button_rect = self.screen_handler.draw_button("Join Game",
                                                                pygame.font.Font(None, self.screen_handler.FONT_SIZE),
                                                                self.screen_handler.BLACK,
                                                                self.screen_handler.SCREEN_WIDTH // 2,
                                                                self.screen_handler.SCREEN_HEIGHT // 3, 400, 100)

        # Draw "Get Player Stats" button
        get_stats_button_rect = self.screen_handler.draw_button("Get Player Stats",
                                                                pygame.font.Font(None, self.screen_handler.FONT_SIZE),
                                                                self.screen_handler.BLACK,
                                                                self.screen_handler.SCREEN_WIDTH // 2,
                                                                self.screen_handler.SCREEN_HEIGHT // 2, 400, 100)

        # Draw "Game Rules" button
        instructions_button_rect = self.screen_handler.draw_button("Game Rules",
                                                                   pygame.font.Font(None,
                                                                                    self.screen_handler.FONT_SIZE),
                                                                   self.screen_handler.BLACK,
                                                                   self.screen_handler.SCREEN_WIDTH // 2,
                                                                   self.screen_handler.SCREEN_HEIGHT // 3 * 2, 400, 100)

        # Draw "Quit Game" button
        quit_game_button_rect = self.screen_handler.draw_button("Quit Game",
                                                                pygame.font.Font(None, self.screen_handler.FONT_SIZE),
                                                                self.screen_handler.BLACK,
                                                                self.screen_handler.SCREEN_WIDTH // 2,
                                                                self.screen_handler.SCREEN_HEIGHT // 6 * 5, 400, 100)

        # Update the display with drawn elements
        pygame.display.flip()

        # Main loop to handle events
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left mouse button
                        mouse_pos = pygame.mouse.get_pos()
                        # Handle "Join Game" button click
                        if join_game_button_rect.collidepoint(mouse_pos):
                            self.screen_handler.draw_text("Joining Game...", title_font,
                                                          self.screen_handler.BLACK,
                                                          self.screen_handler.SCREEN_WIDTH // 2,
                                                          self.screen_handler.SCREEN_HEIGHT // 8 * 6)
                            pygame.display.flip()
                            return "Join Game"
                        # Handle "Get Player Stats" button click
                        elif get_stats_button_rect.collidepoint(mouse_pos):
                            return "Get Stats"
                        # Handle "Game Rules" button click
                        elif instructions_button_rect.collidepoint(mouse_pos):
                            return "Instructions"
                        # Handle "Quit Game" button click
                        elif quit_game_button_rect.collidepoint(mouse_pos):
                            pygame.quit()
                            sys.exit()


if __name__ == "__main__":
    # Initialize user HTTP handler with server URL
    user_http_handler = UserHTTPHandler("http://127.0.0.1:5000")
    # Initialize screen handler
    screenHandler = ScreenHandler()
    # Set up the app infrastructure (e.g., screen settings)
    screenHandler.setup_app_infrastructure()
    # Create and run the options page
    options_page = OptionsPage(screenHandler)
    options_page.run()
