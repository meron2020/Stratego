import sys

import pygame


class GameResultPage:
    def __init__(self, screen_handler):
        # Initialize the screen handler
        self.screen_handler = screen_handler

    # Main method to run the game result page
    def run(self, is_winner):
        self.screen_handler.quit_button_presented = False
        # Set the fonts for the title and info text
        title_font = pygame.font.Font(None, self.screen_handler.FONT_SIZE * 2)
        info_font = pygame.font.Font(None, self.screen_handler.FONT_SIZE)

        # Draw the "Quit Game" button
        return_to_options_button_rect = self.screen_handler.draw_button("Quit Game",
                                                                        pygame.font.Font(None,
                                                                                         self.screen_handler.FONT_SIZE),
                                                                        self.screen_handler.BLACK,
                                                                        self.screen_handler.SCREEN_WIDTH // 2,
                                                                        self.screen_handler.SCREEN_HEIGHT // 3 * 2, 400,
                                                                        100)

        # Main loop to handle events and update the screen
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left mouse button
                        mouse_pos = pygame.mouse.get_pos()
                        # If the "Quit Game" button is clicked, return to the options menu
                        if return_to_options_button_rect.collidepoint(mouse_pos):
                            return

            # Fill the screen with white color
            self.screen_handler.screen.fill(self.screen_handler.WHITE)

            # Draw the "Game Results" title
            self.screen_handler.draw_text("Game Results", title_font, self.screen_handler.BLACK,
                                          self.screen_handler.SCREEN_WIDTH // 2, self.screen_handler.SCREEN_HEIGHT // 8)

            # Display the result message based on whether the player won or lost
            if is_winner:
                result = "You Won!"
                self.screen_handler.draw_text(result, info_font, self.screen_handler.BLACK,
                                              self.screen_handler.SCREEN_WIDTH // 2,
                                              self.screen_handler.SCREEN_HEIGHT // 8 * 2)
                self.screen_handler.draw_text("Added to user stats", info_font, self.screen_handler.BLACK,
                                              self.screen_handler.SCREEN_WIDTH // 2,
                                              self.screen_handler.SCREEN_HEIGHT // 8 * 3)
            else:
                result = "You Lost!"
                self.screen_handler.draw_text(result, info_font, self.screen_handler.BLACK,
                                              self.screen_handler.SCREEN_WIDTH // 2,
                                              self.screen_handler.SCREEN_HEIGHT // 8 * 2)
                self.screen_handler.draw_text("Added to user stats", info_font, self.screen_handler.BLACK,
                                              self.screen_handler.SCREEN_WIDTH // 2,
                                              self.screen_handler.SCREEN_HEIGHT // 8 * 3)

            # Draw the "Options Menu" button
            return_to_options_button_rect = self.screen_handler.draw_button("Options Menu",
                                                                            pygame.font.Font(None,
                                                                                             self.screen_handler.FONT_SIZE),
                                                                            self.screen_handler.BLACK,
                                                                            self.screen_handler.SCREEN_WIDTH // 2,
                                                                            self.screen_handler.SCREEN_HEIGHT // 3 * 2,
                                                                            400,
                                                                            100)

            # Update the display
            pygame.display.flip()
