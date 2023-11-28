import pygame


class PieceSprite(pygame.sprite.Sprite):
    def __init__(self, image, row, column, board):
        super().__init__()
        self.board = board
        self.image = pygame.transform.scale(pygame.image.load(image), (20, 20))
        self.rect = self.image.get_rect()
        self.rect.topleft = self.calculate_exact_position(row, column)

    def calculate_exact_position(self, row, column):
        x_pos = row * (self.board.height + self.board.margin)
        y_pos = column * (self.board.height + self.board.margin)
        return tuple((x_pos, y_pos))

    def set_new_pos(self, row, column):
        self.rect.topleft = self.calculate_exact_position(row, column)

