import pygame


class Board:
    def __init__(self, screen):
        self.cell_size = pygame.display.get_window_size()[0] / 25
        self.margin = 10
        self.screen = screen

    def create_board(self, color):
        start_x = (pygame.display.get_window_size()[0] - 10 * (self.cell_size + self.margin)) // 2
        start_y = (pygame.display.get_window_size()[1] - 10 * (self.cell_size + self.margin)) // 2
        for column in range(10):
            for row in range(10):
                pygame.draw.rect(self.screen, color,
                                 pygame.Rect(column * (self.cell_size + self.margin) + self.margin + start_x,
                                             start_y+row * (self.cell_size + self.margin) +
                                             self.margin, self.cell_size, self.cell_size))

