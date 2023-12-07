class GameBoard:
    def __init__(self):
        self._board_matrix = []

    # Creates a 2d matrix that represents the board.
    def set_up_board(self):
        for i in range(10):
            self._board_matrix.append([])
            for j in range(10):
                self._board_matrix[i][j] = None

    def get_piece_in_position(self, position):
        return self._board_matrix[position[0]][position[1]]

    def get_board_matrix(self):
        return self._board_matrix

    # Moves a piece to a new position in the board matrix.
    def set_new_piece_position(self, piece, new_position):
        # Finds piece position and changes it, only if game has already started.
        if piece.position:
            piece_pos = piece.position
            self._board_matrix[piece_pos[0]][piece_pos[1]] = None

        # Sets piece position to new position and changes board matrix accordingly.
        piece.position = new_position
        self._board_matrix[new_position[0]][new_position[1]] = piece
        return True

    def get_piece_count(self):
        piece_count = 0
        for i in range(10):
            for j in range(10):
                if self._board_matrix[i][j]:
                    piece_count += 1

        return piece_count
