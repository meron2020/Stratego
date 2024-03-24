class GameBoard:
    # GameBoard constructor.
    def __init__(self, board_matrix=None):
        if board_matrix is None:
            self._board_matrix = [[[] for i in range(10)] for j in range(10)]
        else:
            self._board_matrix = board_matrix

    # Creates a 2d matrix that represents the board.
    def set_up_board(self):
        for i in range(10):
            self._board_matrix.append([])
            for j in range(10):
                self._board_matrix[i][j] = None

    # Takes position as parameter and returns the id of the piece in that position.
    def get_piece_id_in_position(self, position):
        return self._board_matrix[position[0]][position[1]]

    # Returns the board matrix
    def get_board_matrix(self):
        return self._board_matrix

    # Moves a piece to a new position in the board matrix.
    def set_new_piece_id_position(self, piece, new_position):
        # Finds piece position and changes it, only if game has already started.
        if piece.position:
            piece_pos = piece.position
            self._board_matrix[piece_pos[0]][piece_pos[1]] = []

        # Sets piece position to new position and changes board matrix accordingly.
        piece.position = new_position
        self._board_matrix[new_position[0]][new_position[1]] = [piece.piece_id]
        return True

    # Takes a position and deletes the piece in that position.
    def delete_piece(self, position):
        self._board_matrix[position[0]][position[1]] = None

    # Returns the amount of pieces on the board.
    def get_piece_count(self):
        piece_count = 0
        for i in range(10):
            for j in range(10):
                if self._board_matrix[i][j]:
                    piece_count += 1

        return piece_count
