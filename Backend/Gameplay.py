from Rules.RunnerRules import RunnerRules
from Rules.AttackingRules import AttackingRules
from Rules.MovementRules import MovementRules
from universals import strength_to_name_and_number_dict as s_to_n_and_n
from GameBoard import GameBoard
from Piece import Piece


# Game class is responsible for running the game.
class Game:
    def __init__(self):
        self.board = GameBoard()
        self.red_piece_list = Game.create_pieces_lists("red")
        self.blue_piece_list = Game.create_pieces_lists("blue")
        self.turn = "red"

    # Function takes a color as a parameter and returns the initial list of pieces set with that color.
    @staticmethod
    def create_pieces_lists(color):
        piece_list = [Piece('F', color, "Flag")]
        for i in range(1, 11):
            for j in range(s_to_n_and_n[i][1]):
                piece_list.append(Piece(i, color, s_to_n_and_n[i][0]))

        for i in range(3):
            piece_list.append(Piece('B', color, "Bomb"))

        return piece_list
