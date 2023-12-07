class RunnerRules:
    IllegalPositions = [(6, 3), (6, 4), (5, 3), (5, 3), (6, 7), (6, 8), (5, 7), (5, 8)]

    # Checks available moves above the runner.
    @classmethod
    def check_runner_above(cls, pos, color, board):
        if pos in RunnerRules.IllegalPositions or board[pos[0], pos[1]].color == color or pos[0] < 0:
            return []
        if board[pos[0], pos[1]].color != color:
            return [pos]

        return RunnerRules.check_runner_above((pos[0] - 1, pos[1]), color, board).append(pos)

    # Checks available moves below the runner.
    @classmethod
    def check_runner_below(cls, pos, color, board):
        if pos in RunnerRules.IllegalPositions or board[pos[0], pos[1]].color == color or pos[0] > 9:
            return []
        if board[pos[0], pos[1]].color != color:
            return [pos]

        return RunnerRules.check_runner_below((pos[0] + 1, pos[1]), color, board).append(pos)

    # Checks available moves on the left side of the runner.
    @classmethod
    def check_runner_left(cls, pos, color, board):
        if pos in RunnerRules.IllegalPositions or board[pos[0], pos[1]].color == color or pos[1] < 0:
            return []
        if board[pos[0], pos[1]].color != color:
            return [pos]

        return RunnerRules.check_runner_left((pos[0], pos[1] - 1), color, board).append(pos)

    # Checks available moves on the right side of the runner.
    @classmethod
    def check_runner_right(cls, pos, color, board):
        if pos in RunnerRules.IllegalPositions or board[pos[0], pos[1]].color == color or pos[1] > 9:
            return []
        if board[pos[0], pos[1]].color != color:
            return [pos]

        return RunnerRules.check_runner_right((pos[0], pos[1] + 1), color, board).append(pos)

    # Checks all available moves for the runner.
    @classmethod
    def calculate_runner_possible_moves(cls, piece, game_board):
        possible_moves = []
        possible_moves += RunnerRules.check_runner_above((piece.position[0] - 1, piece.position[1]), piece.color,
                                                         game_board)
        possible_moves += RunnerRules.check_runner_below((piece.position[0] + 1, piece.position[1]), piece.color,
                                                         game_board)
        possible_moves += RunnerRules.check_runner_right((piece.position[0], piece.position[1] + 1), piece.color,
                                                         game_board)
        possible_moves += RunnerRules.check_runner_left((piece.position[0], piece.position[1] - 1), piece.color,
                                                        game_board)

        return possible_moves
