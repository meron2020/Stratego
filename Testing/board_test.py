import pygame

from Testing.sprite_testing import PieceSprite


class Board:
    def __init__(self, screen, board_size=10, margin_percentage=0.1):
        self.start_y = None
        self.start_x = None
        self.margin = None
        self.square_size = None
        self.screen = screen
        self.board_size = board_size
        self.margin_percentage = margin_percentage
        self.calculate_dimensions()
        board_width = self.board_size * self.square_size
        board_height = self.board_size * self.square_size
        self.start_x = (self.screen.get_width() - board_width) // 2
        self.start_y = (self.screen.get_height() - board_height) // 2
        self.dark_green = (0, 100, 0)
        self.black = (0, 0, 0)
        self.blue = (0, 0, 255)
        self.pieces = []  # List to store PieceSprite instances
        self.board_matrix = [[[] for i in range(10)] for j in range(10)]

    def is_bottom_rows_filled(self):
        bottom_rows = self.board_matrix[-1:]  # Select the bottom four rows
        for row in bottom_rows:
            for cell in row:
                if not cell:
                    return False
        return True

    def add_piece(self, row, col, piece):
        self.pieces.append(piece)
        self.board_matrix[row - 1][col - 5] =[piece.piece_id]

    def calculate_dimensions(self):
        min_dimension = min(self.screen.get_width(), self.screen.get_height())
        self.square_size = min_dimension // self.board_size - 15
        self.margin = int(self.margin_percentage * self.square_size)

    def draw_board(self):
        self.calculate_dimensions()
        board_width = self.board_size * self.square_size
        board_height = self.board_size * self.square_size
        self.start_x = (self.screen.get_width() - board_width) // 2
        self.start_y = (self.screen.get_height() - board_height) // 2

        # Draw background
        background = pygame.image.load(
            "C:\\Users\\yoavm\\PycharmProjects\\Stratego\\Frontend\\GUI\\Sprite_Images\\soldier.png")  # Replace with your actual file path
        background = pygame.transform.scale(background, (self.screen.get_width(), self.screen.get_height()))
        self.screen.blit(background, (0, 0))

        for row in range(self.board_size):
            for col in range(self.board_size):
                rect = pygame.Rect(
                    self.start_x + col * self.square_size + self.margin,
                    self.start_y + row * self.square_size + self.margin,
                    self.square_size - 2 * self.margin,
                    self.square_size - 2 * self.margin
                )
                if (row, col) in [(4, 2), (4, 3), (5, 2), (5, 3), (4, 6), (4, 7), (5, 6), (5, 7)]:
                    # Draw lake (4 squares)
                    pygame.draw.rect(self.screen, self.blue, rect)
                else:
                    # Draw land
                    pygame.draw.rect(self.screen, self.dark_green, rect)
        for i in range(1, self.board_size):
            # Vertical lines
            pygame.draw.line(self.screen, self.black, (self.start_x + i * self.square_size, self.start_y),
                             (self.start_x + i * self.square_size, self.start_y + board_height), 2 * self.margin)
            # Horizontal lines
            pygame.draw.line(self.screen, self.black, (self.start_x, self.start_y + i * self.square_size),
                             (self.start_x + board_width, self.start_y + i * self.square_size), 2 * self.margin)

        for piece in self.pieces:
            self.screen.blit(piece.image, piece.rect.topleft)

    def check_square_filled(self, row, col):
        return self.board_matrix[row - 1][col - 5] != []

    def create_piece_to_pos_dict(self):
        piece_to_pos_dict = {}
        print(self.board_matrix)
        for row in self.board_matrix:
            for col in row:
                if len(col) != 0:
                    piece_id = col[0]
                    piece_to_pos_dict[piece_id] = (row, col)

        return piece_to_pos_dict

    def color_square(self, position, color):
        row, col = position[0], position[1]
        rect = pygame.Rect(
            self.start_x + col * self.square_size + self.margin,
            self.start_y + row * self.square_size + self.margin,
            self.square_size - 2 * self.margin,
            self.square_size - 2 * self.margin
        )
        pygame.draw.rect(self.screen, color, rect)
        pygame.display.flip()

