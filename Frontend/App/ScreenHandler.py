import sys

import pygame


class ScreenHandler:
    def __init__(self):
        # Initialize screen properties and color definitions
        self.screen = None  # This will hold the main display surface
        self.WHITE = (255, 255, 255)  # RGB color for white
        self.BLACK = (0, 0, 0)  # RGB color for black
        self.FONT_SIZE = 32  # Default font size
        self.SCREEN_WIDTH = 1920  # Default screen width
        self.SCREEN_HEIGHT = 1080  # Default screen height

    def draw_text(self, text, font, color, x, y):
        """
        Draw text on the screen at a specified location.
        :param text: String to display
        :param font: pygame Font object
        :param color: Tuple (R, G, B)
        :param x: X coordinate of the text center
        :param y: Y coordinate of the text center
        """
        text_obj = font.render(text, True, color)  # Render the text
        text_rect = text_obj.get_rect()
        text_rect.center = (x, y)  # Position the text
        self.screen.blit(text_obj, text_rect)  # Blit the text onto the screen

    def draw_button(self, text, font, color, x, y, width, height):
        """
        Draw a button with text centered on the screen.
        :param text: String on the button
        :param font: pygame Font object for the text
        :param color: Tuple (R, G, B) for text color
        :param x: X coordinate of the button center
        :param y: Y coordinate of the button center
        :param width: Width of the button
        :param height: Height of the button
        :return: Rect object for the button
        """
        button_rect = pygame.Rect(x - width // 2, y - height // 2, width, height)
        pygame.draw.rect(self.screen, color, button_rect, 2)  # Draw button outline
        self.draw_text(text, font, color, x, y)  # Draw text on button
        return button_rect

    @classmethod
    def wrap_text(cls, font, content, max_width):
        """
        Wrap text to fit within a specified width when rendering.
        :param font: pygame Font object
        :param content: Text string to wrap
        :param max_width: Maximum width in pixels for the text line
        :return: List of strings where each string is a line of text
        """
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

    def draw_text_input(self, x, y, width, height, text, is_password=False):
        """
        Draw a text input field on the screen.
        :param x: X coordinate of the center of the input field
        :param y: Y coordinate of the center of the input field
        :param width: Width of the input field
        :param height: Height of the input field
        :param text: Text to display in the field
        :param is_password: Boolean to determine if text should be obscured
        :return: Rect object for the input field
        """
        input_rect = pygame.Rect(x - width // 2, y - height // 2, width, height)
        pygame.draw.rect(self.screen, self.BLACK, input_rect, 2)  # Draw input box
        font = pygame.font.Font(None, self.FONT_SIZE)
        displayed_text = "*" * len(text) if is_password else text  # Obscure text if password
        text_surface = font.render(displayed_text, True, self.BLACK)
        text_x = x - text_surface.get_width() // 2  # Center text horizontally
        text_y = y - text_surface.get_height() // 2  # Center text vertically
        self.screen.blit(text_surface, (text_x, text_y))
        return input_rect

    def setup_app_infrastructure(self):
        """
        Initialize Pygame and set up the display.
        """
        pygame.init()
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        pygame.display.set_caption("Stratego")

    @classmethod
    def event_handling_when_waiting(cls):
        """
        Handle events while waiting for the player's turn.
        Processes events like quitting or mouse button down.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                continue  # Placeholder to handle mouse button events


if __name__ == "__main__":
    # If run directly, initialize and set up the screen handler.
    screenHandler = ScreenHandler()
    screenHandler.setup_app_infrastructure()
