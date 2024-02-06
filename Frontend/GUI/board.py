import pygame


class Board:
    def __init__(self, screen):
        self.cell_size = pygame.display.get_window_size()[0] / 25
        self.margin = 10
        self.screen = screen
        self.board_matrix = []

    def create_board(self, color):
        start_x = (pygame.display.get_window_size()[0] - 10 * (self.cell_size + self.margin)) // 2
        start_y = (pygame.display.get_window_size()[1] - 10 * (self.cell_size + self.margin)) // 2
        for column in range(10):
            self.board_matrix.append([])
            for row in range(10):
                cell = pygame.Rect(column * (self.cell_size + self.margin) + self.margin + start_x,
                                   start_y + row * (self.cell_size + self.margin) +
                                   self.margin, self.cell_size, self.cell_size)
                self.board_matrix[column].append(cell)
                pygame.draw.rect(self.screen, color,
                                 cell)

    def color_movement_options(self, move_options, attack_options):
        for option in move_options:
            cell = self.board_matrix[option[0]][option[1]]
            pygame.draw.rect(self.screen, (0, 255, 0), cell)

        for option in attack_options:
            cell = self.board_matrix[option[0]][option[1]]
            pygame.draw.rect(self.screen, (255, 0, 0), cell)
