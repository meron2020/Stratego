import sys
from Frontend.App.ScreenHandler import ScreenHandler
import pygame


class StatsPage:
    def __init__(self, screen_handler):

        # Initialize ScreenHandler
        self.screen_handler = screen_handler

    # Method to create and display the stats page
    def create_stats_page(self, user, wins, losses, ties):
        self.screen_handler.screen.fill(self.screen_handler.WHITE)

        # Draw title
        title_font = pygame.font.Font(None, self.screen_handler.FONT_SIZE * 2)
        self.screen_handler.draw_text("User Stats", title_font, self.screen_handler.BLACK,
                                      self.screen_handler.SCREEN_WIDTH // 2, self.screen_handler.SCREEN_HEIGHT // 8)

        # Draw user name
        center_x = self.screen_handler.SCREEN_WIDTH // 2
        start_y = self.screen_handler.SCREEN_HEIGHT // 3
        gap_y = self.screen_handler.SCREEN_HEIGHT // 12
        title_x_offset = 300  # Offset for the category titles

        # Draw user name
        self.screen_handler.draw_text("User:", pygame.font.Font(None, self.screen_handler.FONT_SIZE),
                                      self.screen_handler.BLACK, center_x - title_x_offset, start_y)
        self.screen_handler.draw_text(user, pygame.font.Font(None, self.screen_handler.FONT_SIZE),
                                      self.screen_handler.BLACK, center_x + title_x_offset, start_y)

        # Draw wins
        self.screen_handler.draw_text("Wins:", pygame.font.Font(None, self.screen_handler.FONT_SIZE),
                                      self.screen_handler.BLACK, center_x - title_x_offset, start_y + gap_y)
        self.screen_handler.draw_text(str(wins), pygame.font.Font(None, self.screen_handler.FONT_SIZE),
                                      self.screen_handler.BLACK, center_x + title_x_offset, start_y + gap_y)

        # Draw losses
        self.screen_handler.draw_text("Losses:", pygame.font.Font(None, self.screen_handler.FONT_SIZE),
                                      self.screen_handler.BLACK, center_x - title_x_offset, start_y + 2 * gap_y)
        self.screen_handler.draw_text(str(losses), pygame.font.Font(None, self.screen_handler.FONT_SIZE),
                                      self.screen_handler.BLACK, center_x + title_x_offset, start_y + 2 * gap_y)

        # Draw ties
        self.screen_handler.draw_text("Ties:", pygame.font.Font(None, self.screen_handler.FONT_SIZE),
                                      self.screen_handler.BLACK, center_x - title_x_offset, start_y + 3 * gap_y)
        self.screen_handler.draw_text(str(ties), pygame.font.Font(None, self.screen_handler.FONT_SIZE),
                                      self.screen_handler.BLACK, center_x + title_x_offset, start_y + 3 * gap_y)

        pygame.display.flip()

        # Main loop
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()


if __name__ == "__main__":
    screenHandler = ScreenHandler()
    screenHandler.setup_app_infrastructure()
    stats_page = StatsPage(screenHandler)
    stats_page.create_stats_page("Player1", 10, 5, 3)
