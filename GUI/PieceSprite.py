import pygame


class PieceSprite(pygame.sprite.Sprite):
    def __init__(self, image, row, column, board):
        super().__init__()
        self.board = board
        self.image = pygame.transform.scale(pygame.image.load(image),
                                            (int(self.board.cell_size), int(self.board.cell_size)))
        self.rect = self.image.get_rect()
        self.rect.topleft = self.calculate_exact_position(row, column)

    def calculate_exact_position(self, row, column):
        start_x = (pygame.display.get_window_size()[0] - 10 * (self.board.cell_size + self.board.margin)) // 2
        start_y = (pygame.display.get_window_size()[1] - 10 * (self.board.cell_size + self.board.margin)) // 2
        x_pos = start_x + row * (self.board.cell_size + self.board.margin) + self.board.margin
        y_pos = start_y + column * (self.board.cell_size + self.board.margin) + self.board.margin
        return tuple((x_pos, y_pos))

    def set_new_pos(self, row, column):
        self.rect.topleft = self.calculate_exact_position(row, column)
