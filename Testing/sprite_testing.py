import pygame


class PieceSprite(pygame.sprite.Sprite):
    def __init__(self, image, row, column, board, screen, piece_id):
        super().__init__()
        self.setup_mode = True
        self.board = board
        self.image = pygame.transform.scale(pygame.image.load(image),
                                            (int(self.board.square_size), int(self.board.square_size)))
        self.rect = self.image.get_rect()
        self.rect.topleft = self.calculate_exact_position(row, column)
        self.is_dragging = False
        self.offset = (0, 0)
        self.screen = screen
        self.piece_id = piece_id

        self.cur_row = None
        self.cur_col = None

    def set_setup_mode(self, setup_mode):
        self.setup_mode = setup_mode

    def calculate_exact_position(self, row, column):
        start_x = (self.board.screen.get_width() - self.board.board_size * (
                self.board.square_size + self.board.margin)) // 2
        start_y = (self.board.screen.get_height() - self.board.board_size * (
                self.board.square_size + self.board.margin)) // 2
        x_pos = start_x + column * (self.board.square_size + self.board.margin) + self.board.margin
        y_pos = start_y + row * (self.board.square_size + self.board.margin) + self.board.margin
        return x_pos, y_pos

    def start_drag(self, mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            self.is_dragging = True
            self.offset = (self.rect.x - mouse_pos[0], self.rect.y - mouse_pos[1])
            self.cur_row, self.cur_col = self.find_current_square()

    def drag(self, mouse_rel):
        if self.is_dragging:
            self.rect.x = mouse_rel[0] + self.offset[0]
            self.rect.y = mouse_rel[1] + self.offset[1]

    def find_current_square(self):
        # Calculate the center coordinates of the current position
        center_x = self.rect.x + self.rect.width / 2
        center_y = self.rect.y + self.rect.height / 2

        # Find the current square based on the center coordinates
        row = int((center_y - self.board.margin) / self.board.square_size)
        col = int((center_x - self.board.margin) / self.board.square_size)

        # Ensure the row and col are within the board bounds
        row = max(0, min(row, self.board.board_size - 1))
        col = max(0, min(col, self.board.board_size - 1))

        return row, col

    def stop_drag(self, options=None):
        self.is_dragging = False
        # Snap to the closest square
        row, col = self.find_closest_square(options)
        self.rect.topleft = self.calculate_square_position(row, col)
        self.board.add_piece(row, col, self)

    def find_closest_square(self, options=None):
        # Calculate the center coordinates of the current position
        center_x = self.rect.x + self.rect.width / 2
        center_y = self.rect.y + self.rect.height / 2

        # Find the closest square based on the center coordinates
        row = int((center_y - self.board.margin) / self.board.square_size)
        col = int((center_x - self.board.margin) / self.board.square_size)

        # If the function is called for checkin piece options.
        if options is not None:
            if (row, col) in options:
                return row, col
            else:
                return self.cur_row, self.cur_col
        # If function is called for setting up.
        else:
            if PieceSprite.is_over_lake(row, col):
                row, col = self.cur_row, self.cur_col

            elif self.setup_mode and not PieceSprite.check_setup_viable(row):
                row, col = self.cur_row, self.cur_col

            elif self.board.check_square_filled(row, col):
                row, col = self.cur_row, self.cur_col

            # Ensure the row and col are within the board bounds
            row = max(1, min(row, self.board.board_size))
            col = max(0, min(col, self.board.board_size + 4))

        return row, col

    def update(self):
        if self.is_dragging:
            mouse_pos = pygame.mouse.get_pos()
            self.drag(mouse_pos)

    def calculate_square_position(self, row, col):
        x = col * self.board.square_size + self.board.margin * 8
        y = row * self.board.square_size - 4 * self.board.margin
        return x, y

    @classmethod
    def check_setup_viable(cls, row):
        if row in range(7, 11):
            return True
        return False

    @classmethod
    def is_over_lake(cls, row, col):
        # Check if the square is over a lake
        if row == 5 or row == 6:
            if col in [12, 11, 7, 8]:
                return True

        return False

    @classmethod
    def adjust_for_lake(cls, row, col):
        # Adjust row and col if the square is over a lake
        if row == 4 and col == 2:
            row += 1
        elif row == 4 and col == 7:
            row += 1
        return row, col


class PieceGroup(pygame.sprite.Group):
    def __init__(self, board):
        super().__init__()
        self.board = board

    def update(self, *args, **kwargs):
        super().update(*args, **kwargs)
        self.check_snap()

    def check_snap(self):
        for piece in self.sprites():
            row = round((piece.rect.y - self.board.margin) / (self.board.square_size - 2 * self.board.margin))
            col = round((piece.rect.x - self.board.margin) / (self.board.square_size - 2 * self.board.margin))
            piece.rect.topleft = (col * (self.board.square_size - 2 * self.board.margin) + self.board.margin,
                                  row * (self.board.square_size - 2 * self.board.margin) + self.board.margin)


class DraggableSquare(pygame.sprite.Sprite):
    def __init__(self, image, color, board, start_x, start_y):
        super().__init__()
        self.start_x = start_x
        self.start_y = start_y
        self.board = board
        self.image = pygame.transform.scale(pygame.image.load(image),
                                            (int(self.board.square_size), int(self.board.square_size)))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.is_dragging = False
        self.offset = (0, 0)

    def start_drag(self, mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            self.is_dragging = True
            self.offset = (self.rect.x - mouse_pos[0], self.rect.y - mouse_pos[1])

    def drag(self, mouse_pos):
        if self.is_dragging:
            self.rect.x = mouse_pos[0] + self.offset[0]
            self.rect.y = mouse_pos[1] + self.offset[1]

    def stop_drag(self):
        self.is_dragging = False
        # Snap to the closest square
        row, col = self.find_closest_square()
        self.rect.topleft = self.calculate_square_position(row, col)

    def find_closest_square(self):
        # Calculate the center coordinates of the current position
        center_x = self.rect.x + self.rect.width / 2
        center_y = self.rect.y + self.rect.height / 2

        # Find the closest square based on the center coordinates
        row = int((center_y - self.board.margin) / self.board.square_size)
        col = int((center_x - self.board.margin) / self.board.square_size)

        # Ensure the row and col are within the board bounds
        row = max(0, min(row, self.board.board_size - 1))
        col = max(5, min(col, self.board.board_size + 4))

        return row, col

    def calculate_square_position(self, row, col):
        x = col * self.board.square_size + self.board.margin * 8
        y = row * self.board.square_size - 4 * self.board.margin
        return x, y
