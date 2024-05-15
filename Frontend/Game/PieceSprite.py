import json

import pygame

from universals import id_to_image_dict


class PieceSprite(pygame.sprite.Sprite):
    def __init__(self, image, row, column, board, screen, piece_id, in_set_up_mode):
        super().__init__()
        self.setup_mode = in_set_up_mode
        self.board = board
        self.image = pygame.transform.scale(pygame.image.load(image),
                                            (int(self.board.square_size) - 10, int(self.board.square_size) - 10))
        self.rect = self.image.get_rect()
        self.rect.topleft = self.calculate_exact_position(row, column)
        self.is_dragging = False
        self.offset = (0, 0)
        self.screen = screen
        self.piece_id = piece_id
        self.player_id = int(piece_id / 100)
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

    def stop_drag(self, player_id, options=None):
        self.is_dragging = False
        # Snap to the closest square
        row, col = self.find_closest_square(player_id, options)
        self.rect.topleft = self.calculate_square_position(row, col)
        self.board.add_piece(row, col, self)

    def find_closest_square(self, player_id, options=None):
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

            elif self.setup_mode and not PieceSprite.check_setup_viable(row, player_id):
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
        return x + 5, y + 5

    @classmethod
    def check_setup_viable(cls, row, player_id):
        if player_id == 1:
            if row in range(7, 11):
                return True
            return False
        else:
            if row in range(1, 5):
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


class SpriteCreator:
    # Function creates the list of PieceSprites from the dictionary provided by the server
    @classmethod
    def create_pieces_sprites_from_get_request(cls, pieces_dict, board, screen, player_id):
        folder_path = "Frontend/Game/Sprite_Images/"
        sprite_group = pygame.sprite.Group()
        for piece_id, piece_object in pieces_dict.items():
            piece_object = json.loads(piece_object)
            if int(int(piece_id) / 100) == player_id:
                file_name = piece_object["_name"] + ".png"
                image_path = folder_path + file_name
            else:
                image_path = folder_path + "soldier.png"
            sprite_group.add(
                PieceSprite(image_path, int(piece_object["_position"][0]), int(piece_object["_position"][1]),
                            board, screen, int(piece_id), False))
        return sprite_group

    # Function creates the list of PieceSprites for the setup.
    @classmethod
    def create_player_sprites(cls, player_id, board, screen, pos):
        folder_path = "Frontend/Game/Sprite_Images/"
        sprite_group = pygame.sprite.Group()
        for i in range(10):
            for j in range(4):
                piece_id = player_id * 100 + 1 + j * 10 + i
                if pos == "bottom":
                    # Sprites for player with playerId = 1
                    image_path = folder_path + id_to_image_dict[piece_id % 100] + ".png"
                    sprite_group.add(
                        PieceSprite(image_path, i, j - 4, board, screen, piece_id,
                                    True))
                else:
                    # Sprites for player with playerId = 2
                    image_path = folder_path + id_to_image_dict[piece_id % 100] + ".png"
                    sprite_group.add(
                        PieceSprite(image_path, i, j + 10, board, screen, piece_id,
                                    True))
        return sprite_group
