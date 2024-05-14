import sys

import pygame


class GameResultPage:
    def __init__(self, screen_handler):

        # Initialize ScreenHandler
        self.screen_handler = screen_handler

    # Main method to run the options page
    def run(self, is_winner):

        # Draw title
        title_font = pygame.font.Font(None, self.screen_handler.FONT_SIZE * 2)
        info_font = pygame.font.Font(None, self.screen_handler.FONT_SIZE)

        return_to_options_button_rect = self.screen_handler.draw_button("Quit Game",
                                                                        pygame.font.Font(None,
                                                                                         self.screen_handler.FONT_SIZE),
                                                                        self.screen_handler.BLACK,
                                                                        self.screen_handler.SCREEN_WIDTH // 2,
                                                                        self.screen_handler.SCREEN_HEIGHT // 3 * 2, 400,
                                                                        100)


        # Main loop
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left mouse button
                        mouse_pos = pygame.mouse.get_pos()
                        if return_to_options_button_rect.collidepoint(mouse_pos):
                            return
                            # Handle join game functionality here

            self.screen_handler.screen.fill(self.screen_handler.WHITE)

            self.screen_handler.draw_text("Game Results", title_font, self.screen_handler.BLACK,
                                          self.screen_handler.SCREEN_WIDTH // 2, self.screen_handler.SCREEN_HEIGHT // 8)

            if is_winner:
                self.screen_handler.draw_text("You Won!", info_font, self.screen_handler.BLACK,
                                              self.screen_handler.SCREEN_WIDTH // 2,
                                              self.screen_handler.SCREEN_HEIGHT // 8 * 2)

                self.screen_handler.draw_text("Added to user stats", info_font, self.screen_handler.BLACK,
                                              self.screen_handler.SCREEN_WIDTH // 2,
                                              self.screen_handler.SCREEN_HEIGHT // 8 * 3)

            else:
                self.screen_handler.draw_text("You Lost!", info_font, self.screen_handler.BLACK,
                                              self.screen_handler.SCREEN_WIDTH // 2,
                                              self.screen_handler.SCREEN_HEIGHT // 8 * 2)
                self.screen_handler.draw_text("Added to user stats", info_font, self.screen_handler.BLACK,
                                              self.screen_handler.SCREEN_WIDTH // 2,
                                              self.screen_handler.SCREEN_HEIGHT // 8 * 3)

            return_to_options_button_rect = self.screen_handler.draw_button("Options Menu",
                                                                            pygame.font.Font(None,
                                                                                             self.screen_handler.FONT_SIZE),
                                                                            self.screen_handler.BLACK,
                                                                            self.screen_handler.SCREEN_WIDTH // 2,
                                                                            self.screen_handler.SCREEN_HEIGHT // 3 * 2,
                                                                            400,
                                                                            100)

            pygame.display.flip()
