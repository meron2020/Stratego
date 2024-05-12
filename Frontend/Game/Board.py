import pygame


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
        self.piece_id_matrix = [[[] for i in range(10)] for j in range(10)]
        self.rect_matrix = [[] for i in range(10)]

    def setup_rows_filled(self, player_id):
        if player_id == 1:
            bottom_rows = self.piece_id_matrix[-4:]  # Select the bottom four rows
            for row in bottom_rows:
                for cell in row:
                    if not cell:
                        return False
            return True
        else:
            top_rows = self.piece_id_matrix[:4]  # Select the top four rows
            for row in top_rows:
                for cell in row:
                    if not cell:
                        return False
            return True

    def add_piece(self, row, col, piece):
        self.pieces.append(piece)
        self.piece_id_matrix[row - 1][col - 5] = [piece.piece_id]

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
           "App/Background_Images/Game_Background.png")  # Replace with your actual file path
        background = pygame.transform.scale(background, (self.screen.get_width(), self.screen.get_height()))
        self.screen.blit(background, (0, 0))

        for row in range(self.board_size):
            for col in range(self.board_size):
                rect = self.create_square_by_row_and_column(row, col)
                self.rect_matrix[row].append(rect)
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
        return self.piece_id_matrix[row - 1][col - 5] != []

    def create_square_by_row_and_column(self, row, col):
        rect = pygame.Rect(
            self.start_x + col * self.square_size + self.margin,
            self.start_y + row * self.square_size + self.margin,
            self.square_size - 2 * self.margin,
            self.square_size - 2 * self.margin
        )
        return rect

    def create_piece_to_pos_dict(self):
        piece_to_pos_dict = {}
        for row in self.piece_id_matrix:
            for col in row:
                if len(col) != 0:
                    piece_id = col[0]
                    piece_to_pos_dict[piece_id] = (self.piece_id_matrix.index(row), row.index(col))

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


    @classmethod
    def get_clicked_sprite_and_position(cls, sprite_group, mouse_pos):
        for sprite in sprite_group:
            if sprite.rect.collidepoint(mouse_pos):
                return sprite
        return None

    def get_clicked_square(self, mouse_pos):
        for row in self.rect_matrix:
            for rect in row:
                if rect.collidepoint(mouse_pos):
                    return [self.rect_matrix.index(row), row.index(rect)]
