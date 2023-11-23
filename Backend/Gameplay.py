from Rules.RunnerRules import RunnerRules
from Rules.AttackingRules import AttackingRules
from Rules.MovementRules import MovementRules
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
        piece_list = [Piece('F', color, "Flag"), Piece(1, color, "Spy"), Piece(10, color, "Marshall"),
                      Piece(9, color, "General")]

        for i in range(2):
            piece_list.append(Piece(8, color, "Colonel"))

        for i in range(3):
            piece_list.append(Piece(7, color, "Major"))

        for i in range(4):
            piece_list.append(Piece(6, color, "Captain"))

        for i in range(4):
            piece_list.append(Piece(5, color, "Lieutenant"))

        for i in range(4):
            piece_list.append(Piece(4, color, "Sergeant"))

        for i in range(5):
            piece_list.append(Piece(3, color, "Miner"))

        for i in range(8):
            piece_list.append(Piece(2, color, "Scout"))

        return piece_list
