class GameBoard:
    def __init__(self):
        self._board_matrix = []

    # Creates a 2d matrix that represents the board.
    def set_up_board(self):
        for i in range(10):
            self._board_matrix.append([])
            for j in range(10):
                self._board_matrix[i][j] = 0

    def get_board_matrix(self):
        return self._board_matrix

    # Moves a piece to a new position in the board matrix.
    def set_board_piece(self, piece, new_position):
        # Finds piece position and changes it, only if game has already started.
        if piece.position:
            piece_pos = piece.position
            self._board_matrix[piece_pos[0]][piece_pos[1]] = 0

        # Sets piece position to new position and changes board matrix accordingly.
        piece.position = new_position
        self._board_matrix[new_position[0]][new_position[1]] = piece
        return True


