import pygame


class ScreenHandler:
    def __init__(self):
        self.screen = None
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.FONT_SIZE = 32
        self.SCREEN_WIDTH = 1920
        self.SCREEN_HEIGHT = 1080

    @classmethod
    def draw_text(cls, text, font, color, surface, x, y):
        text_obj = font.render(text, True, color)
        text_rect = text_obj.get_rect()
        text_rect.center = (x, y)
        surface.blit(text_obj, text_rect)

    def setup_app_infrastructure(self):
        pygame.init()

        # Initialize the screen in full-screen mode
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        pygame.display.set_caption("Stratego")
