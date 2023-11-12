class GameBoard:
    def __init__(self):
        self._board_matrix = []

    def set_up_board(self):
        for i in range(10):
            for j in range(10):
                self.board_matrix[i][j] = 0

    def get_board_matrix(self):
        return self._board_matrix

