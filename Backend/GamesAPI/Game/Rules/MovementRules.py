from Backend.GamesAPI.Game.Rules.RunnerRules import RunnerRules


class MovementRules:
    IllegalPositions = [(6, 3), (6, 4), (5, 3), (5, 3), (6, 7), (6, 8), (5, 7), (5, 8)]

    # Takes as input the piece being checked and the game board and returns a list of
    # possible positions to which the piece can move.
    @classmethod
    def calculate_possible_moves(cls, piece, game_board):
        # Runner can move differently than regular pieces.
        if piece.strength == 2:
            RunnerRules.calculate_runner_possible_moves(piece, game_board)

        # The flag and bombs cannot move.
        if piece.strength == 'B' or piece.strength == "F":
            return []

        return MovementRules.reg_piece_possible_moves(piece, game_board)

    # Finds possible moves for a regular piece
    @classmethod
    def reg_piece_possible_moves(cls, piece, game_board):
        surrounding_positions = MovementRules.find_surrounding_options(piece.position)
        for pos in surrounding_positions:
            if pos in MovementRules.IllegalPositions:
                surrounding_positions.remove(pos)
            elif game_board[pos[0], pos[1]].color == piece.color:
                surrounding_positions.remove(pos)

        return surrounding_positions

    # Takes a list as an input and returns a list of the surrounding positions on the board.
    # Take note, positions that are diagonally placed from the inputted positions are not included.
    @classmethod
    def find_surrounding_options(cls, position):
        surrounding_positions = [(position[0] - 1, position[1]), (position[0] + 1, position[1]),
                                 (position[0], position[1] - 1),
                                 (position[0], position[1] + 1)]

        # Checks if the position is on the board
        for pos in surrounding_positions:
            if pos[0] > 9 or pos[1] > 9:
                surrounding_positions.remove(pos)

        return surrounding_positions


