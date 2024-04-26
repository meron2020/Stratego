class RunnerRules:
    # Define illegal positions where the runner cannot move
    IllegalPositions = [(4, 2), (4, 3), (5, 2), (5, 3), (4, 6), (4, 7), (5, 6), (5, 7)]

    @classmethod
    def check_runner_above(cls, pos, color, board, pieces_dict):
        try:
            # Check if the runner is at the top edge of the board
            if pos[0] < 0:
                return []
            # Check if the position is in the list of illegal positions
            elif pos in RunnerRules.IllegalPositions:
                return []
            else:
                hit_piece = pieces_dict[str(board[pos[0]][pos[1]])]
                # Check if there is a piece of the opposite color above the runner
                if hit_piece.color != color:
                    return [pos]
                else:
                    return []
        except KeyError:
            # Recursively check positions above the runner
            pos_list = (RunnerRules.check_runner_above((pos[0] - 1, pos[1]), color, board, pieces_dict))
            pos_list.append(pos)
            return pos_list

    @classmethod
    def check_runner_below(cls, pos, color, board, pieces_dict):
        try:
            # Check if the runner is at the bottom edge of the board
            if pos[0] > 9:
                return []
            # Check if the position is in the list of illegal positions
            elif pos in RunnerRules.IllegalPositions:
                return []
            else:
                hit_piece = pieces_dict[str(board[pos[0]][pos[1]])]
                # Check if there is a piece of the opposite color below the runner
                if hit_piece.color != color:
                    return [pos]
                else:
                    return []
        except KeyError:
            # Recursively check positions below the runner
            pos_list = (RunnerRules.check_runner_below((pos[0] + 1, pos[1]), color, board, pieces_dict))
            pos_list.append(pos)
            return pos_list

    @classmethod
    def check_runner_left(cls, pos, color, board, pieces_dict):
        try:
            # Check if the runner is at the left edge of the board
            if pos[1] < 0:
                return []
            # Check if the position is in the list of illegal positions
            elif pos in RunnerRules.IllegalPositions:
                return []
            else:
                hit_piece = pieces_dict[str(board[pos[0]][pos[1]])]
                # Check if there is a piece of the opposite color to the left of the runner
                if hit_piece.color != color:
                    return [pos]
                else:
                    return []
        except KeyError:
            # Recursively check positions to the left of the runner
            pos_list = (RunnerRules.check_runner_left((pos[0], pos[1] - 1), color, board, pieces_dict))
            pos_list.append(pos)
            return pos_list

    @classmethod
    def check_runner_right(cls, pos, color, board, pieces_dict):
        try:
            # Check if the runner is at the right edge of the board
            if pos[1] > 9:
                return []
            # Check if the position is in the list of illegal positions
            elif pos in RunnerRules.IllegalPositions:
                return []
            else:
                hit_piece = pieces_dict[str(board[pos[0]][pos[1]])]
                # Check if there is a piece of the opposite color to the right of the runner
                if hit_piece.color != color:
                    return [pos]
                else:
                    return []
        except KeyError:
            # Recursively check positions to the right of the runner
            pos_list = (RunnerRules.check_runner_right((pos[0], pos[1] + 1), color, board, pieces_dict))
            pos_list.append(pos)
            return pos_list

    @classmethod
    def calculate_runner_possible_moves(cls, piece, game_board, pieces_dict):
        possible_moves = []
        # Check available moves in all four directions relative to the runner's position
        possible_moves += RunnerRules.check_runner_above((piece.position[0] - 1, piece.position[1]), piece.color,
                                                         game_board, pieces_dict)
        possible_moves += RunnerRules.check_runner_below((piece.position[0] + 1, piece.position[1]), piece.color,
                                                         game_board, pieces_dict)
        possible_moves += RunnerRules.check_runner_right((piece.position[0], piece.position[1] + 1), piece.color,
                                                         game_board, pieces_dict)
        possible_moves += RunnerRules.check_runner_left((piece.position[0], piece.position[1] - 1), piece.color,
                                                        game_board, pieces_dict)

        return possible_moves
