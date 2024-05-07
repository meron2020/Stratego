import sys

import pygame


class ScreenHandler:
    def __init__(self):
        self.screen = None
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.FONT_SIZE = 32
        self.SCREEN_WIDTH = 1920
        self.SCREEN_HEIGHT = 1080

        # Function to draw text on the screen

    def draw_text(self, text, font, color, x, y):
        text_obj = font.render(text, True, color)
        text_rect = text_obj.get_rect()
        text_rect.center = (x, y)
        self.screen.blit(text_obj, text_rect)

    # Function to draw buttons on the screen
    def draw_button(self, text, font, color, x, y, width, height):
        button_rect = pygame.Rect(x - width // 2, y - height // 2, width, height)
        pygame.draw.rect(self.screen, self.BLACK, button_rect, 2)
        self.draw_text(text, font, color, x, y)
        return button_rect

    @classmethod
    # Function to wrap text content
    def wrap_text(cls, font, content, max_width):
        """Wraps a text content into multiple lines based on the font width."""
        words = content.split()
        lines = []
        current_line = words[0]

        for word in words[1:]:
            test_line = f"{current_line} {word}"
            if font.size(test_line)[0] > max_width:
                lines.append(current_line)
                current_line = word
            else:
                current_line = test_line

        lines.append(current_line)  # Append the last line
        return lines

    # Function to draw text input field
    # Function to draw text input field
    def draw_text_input(self, x, y, width, height, text, is_password=False):
        input_rect = pygame.Rect(x - width // 2, y - height // 2, width, height)
        pygame.draw.rect(self.screen, self.BLACK, input_rect, 2)
        font = pygame.font.Font(None, self.FONT_SIZE)
        if is_password:
            displayed_text = "*" * len(text)  # Show asterisks instead of characters
        else:
            displayed_text = text
        text_surface = font.render(displayed_text, True, self.BLACK)
        text_width, text_height = text_surface.get_size()
        text_x = x - text_width // 2  # Center the text horizontally
        text_y = y - text_height // 2  # Center the text vertically
        self.screen.blit(text_surface, (text_x, text_y))
        return input_rect

    def setup_app_infrastructure(self):
        pygame.init()

        # Initialize the screen in full-screen mode
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        pygame.display.set_caption("Stratego")

    # Function to handle pygame events while awaiting players turn. Freezes the game.
    @classmethod
    def event_handling_when_waiting(cls):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                continue
