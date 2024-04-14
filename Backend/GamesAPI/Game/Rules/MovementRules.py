from Backend.GamesAPI.Game.Rules.RunnerRules import RunnerRules


class MovementRules:
    IllegalPositions = [(4, 2), (4, 3), (5, 2), (5, 3), (4, 7), (4, 6), (5, 7), (5, 6)]

    # Takes as input the piece being checked and the game board and returns a list of
    # possible positions to which the piece can move.
    @classmethod
    def calculate_possible_moves(cls, piece, game_board, pieces_dict):
        # Runner can move differently than regular pieces.
        if piece.strength == 2:
            return RunnerRules.calculate_runner_possible_moves(piece, game_board, pieces_dict)

        # The flag and bombs cannot move.
        if piece.strength == 'B' or piece.strength == "F":
            return []

        return MovementRules.reg_piece_possible_moves(piece, game_board)

    # Finds possible moves for a regular piece
    @classmethod
    def reg_piece_possible_moves(cls, piece, game_board):
        surrounding_positions = MovementRules.find_surrounding_options(piece.position)
        possible_options = []
        for pos in surrounding_positions:
            if not (pos in MovementRules.IllegalPositions or str(game_board[pos[0]][pos[1]])[0] == str(piece.piece_id)[0]):
                possible_options.append(pos)

        return possible_options

    # Takes a list as an input and returns a list of the surrounding positions on the board.
    # Take note, positions that are diagonally placed from the inputted positions are not included.
    @classmethod
    def find_surrounding_options(cls, position):
        positions_to_return = []
        surrounding_positions = [(position[0] - 1, position[1]), (position[0] + 1, position[1]),
                                 (position[0], position[1] - 1),
                                 (position[0], position[1] + 1)]

        # Checks if the position is on the board
        for pos in surrounding_positions:
            if (9 >= pos[0] >= 0) and (9 >= pos[1] >= 0):
                positions_to_return.append(pos)

        return positions_to_return


