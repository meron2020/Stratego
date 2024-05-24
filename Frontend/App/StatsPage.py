import sys
import pygame
from Frontend.App.ScreenHandler import ScreenHandler


class StatsPage:
    def __init__(self, screen_handler):
        # Initialize the StatsPage with a reference to the screen handler object
        self.screen_handler = screen_handler

    def create_stats_page(self, user, wins, losses, ties):
        # Fill the screen with white color using the predefined WHITE attribute from screen handler
        self.screen_handler.screen.fill(self.screen_handler.WHITE)

        # Draw the title of the stats page at the top
        title_font = pygame.font.Font(None, self.screen_handler.FONT_SIZE * 2)
        self.screen_handler.draw_text("User Stats", title_font, self.screen_handler.BLACK,
                                      self.screen_handler.SCREEN_WIDTH // 2, self.screen_handler.SCREEN_HEIGHT // 8)

        # Prepare to draw user statistics
        center_x = self.screen_handler.SCREEN_WIDTH // 2
        start_y = self.screen_handler.SCREEN_HEIGHT // 3
        gap_y = self.screen_handler.SCREEN_HEIGHT // 12
        title_x_offset = 300  # Offset for aligning the category titles to the left

        # Draw a back button and store its rectangle for click detection
        back_button_rect = self.screen_handler.draw_button("Back",
                                                           pygame.font.Font(None, self.screen_handler.FONT_SIZE),
                                                           self.screen_handler.BLACK,
                                                           self.screen_handler.SCREEN_WIDTH // 2,
                                                           self.screen_handler.SCREEN_HEIGHT * 7 // 8, 300, 100)

        # Display the user's name
        self.screen_handler.draw_text("User:", pygame.font.Font(None, self.screen_handler.FONT_SIZE),
                                      self.screen_handler.BLACK, center_x - title_x_offset, start_y)
        self.screen_handler.draw_text(user, pygame.font.Font(None, self.screen_handler.FONT_SIZE),
                                      self.screen_handler.BLACK, center_x + title_x_offset, start_y)

        # Display the number of wins
        self.screen_handler.draw_text("Wins:", pygame.font.Font(None, self.screen_handler.FONT_SIZE),
                                      self.screen_handler.BLACK, center_x - title_x_offset, start_y + gap_y)
        self.screen_handler.draw_text(str(wins), pygame.font.Font(None, self.screen_handler.FONT_SIZE),
                                      self.screen_handler.BLACK, center_x + title_x_offset, start_y + gap_y)

        # Display the number of losses
        self.screen_handler.draw_text("Losses:", pygame.font.Font(None, self.screen_handler.FONT_SIZE),
                                      self.screen_handler.BLACK, center_x - title_x_offset, start_y + 2 * gap_y)
        self.screen_handler.draw_text(str(losses), pygame.font.Font(None, self.screen_handler.FONT_SIZE),
                                      self.screen_handler.BLACK, center_x + title_x_offset, start_y + 2 * gap_y)

        # Display the number of ties
        self.screen_handler.draw_text("Ties:", pygame.font.Font(None, self.screen_handler.FONT_SIZE),
                                      self.screen_handler.BLACK, center_x - title_x_offset, start_y + 3 * gap_y)
        self.screen_handler.draw_text(str(ties), pygame.font.Font(None, self.screen_handler.FONT_SIZE),
                                      self.screen_handler.BLACK, center_x + title_x_offset, start_y + 3 * gap_y)

        # Update the display to show all changes
        pygame.display.flip()

        # Main event loop to handle user interaction
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    # Exit the game if the window is closed
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Check if the left mouse button was pressed
                        mouse_pos = pygame.mouse.get_pos()
                        if back_button_rect.collidepoint(mouse_pos):
                            # If the back button is clicked, print to the console and exit the loop
                            print("Back button clicked")
                            return False


if __name__ == "__main__":
    # If the script is run directly, initialize the screen handler and display the stats page
    screenHandler = ScreenHandler()
    screenHandler.setup_app_infrastructure()
    stats_page = StatsPage(screenHandler)
    stats_page.create_stats_page("Player1", 10, 5, 3)
