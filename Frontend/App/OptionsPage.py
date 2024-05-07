import sys

import pygame

from Frontend.App.ScreenHandler import ScreenHandler
from Frontend.ServerCommunications.UserHTTPHandler import UserHTTPHandler


class OptionsPage:
    def __init__(self, screen_handler):

        # Initialize ScreenHandler
        self.screen_handler = screen_handler

    # Main method to run the options page
    def run(self):
        self.screen_handler.screen.fill(self.screen_handler.WHITE)

        # Draw title
        title_font = pygame.font.Font(None, self.screen_handler.FONT_SIZE * 2)
        self.screen_handler.draw_text("Options", title_font, self.screen_handler.BLACK,
                                      self.screen_handler.SCREEN_WIDTH // 2, self.screen_handler.SCREEN_HEIGHT // 8)

        # Draw join game button
        join_game_button_rect = self.screen_handler.draw_button("Join Game",
                                                                pygame.font.Font(None, self.screen_handler.FONT_SIZE),
                                                                self.screen_handler.BLACK,
                                                                self.screen_handler.SCREEN_WIDTH // 2,
                                                                self.screen_handler.SCREEN_HEIGHT // 3, 400, 100)

        # Draw get player stats button
        get_stats_button_rect = self.screen_handler.draw_button("Get Player Stats",
                                                                pygame.font.Font(None,
                                                                                 self.screen_handler.FONT_SIZE),
                                                                self.screen_handler.BLACK,
                                                                self.screen_handler.SCREEN_WIDTH // 2,
                                                                self.screen_handler.SCREEN_HEIGHT // 2, 400, 100)

        # Draw Instructions button
        instructions_button_rect = self.screen_handler.draw_button("Game Rules",
                                                                   pygame.font.Font(None,
                                                                                    self.screen_handler.FONT_SIZE),
                                                                   self.screen_handler.BLACK,
                                                                   self.screen_handler.SCREEN_WIDTH // 2,
                                                                   self.screen_handler.SCREEN_HEIGHT // 3 * 2, 400, 100)

        # Draw quit game button
        quit_game_button_rect = self.screen_handler.draw_button("Quit Game",
                                                                pygame.font.Font(None, self.screen_handler.FONT_SIZE),
                                                                self.screen_handler.BLACK,
                                                                self.screen_handler.SCREEN_WIDTH // 2,
                                                                self.screen_handler.SCREEN_HEIGHT // 6 * 5, 400, 100)

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
                        # Handle join game functionality here
                        if join_game_button_rect.collidepoint(mouse_pos):
                            self.screen_handler.draw_text("Joining Game...", title_font,
                                                          self.screen_handler.BLACK,
                                                          self.screen_handler.SCREEN_WIDTH // 2,
                                                          self.screen_handler.SCREEN_HEIGHT // 8 * 6)
                            pygame.display.flip()
                            return "Join Game"
                        # Handle get player stats functionality here
                        elif get_stats_button_rect.collidepoint(mouse_pos):
                            return "Get Stats"
                        # Handle instructions functionality here
                        elif instructions_button_rect.collidepoint(mouse_pos):
                            return "Instructions"
                        elif quit_game_button_rect.collidepoint(mouse_pos):
                            pygame.quit()
                            sys.exit()


if __name__ == "__main__":
    user_http_handler = UserHTTPHandler("http://127.0.0.1:5000")
    screenHandler = ScreenHandler()
    screenHandler.setup_app_infrastructure()
    options_page = OptionsPage(screenHandler)
    options_page.run()
