from GameBoard import GameBoard
from Piece import Piece
from Rules.AttackingRules import AttackingRules
from Rules.MovementRules import MovementRules
from universals import strength_to_name_and_number_dict as s_to_n_and_n


# Game class is responsible for running the game.
class Game:
    def __init__(self):
        self.board = GameBoard()
        self.pieces_dict = Game.create_pieces_dict()
        self.turn = "red"
        self.board_set = False

    # Function takes a color as a parameter and returns the initial list of pieces set with that color.
    @staticmethod
    def create_pieces_dict():
        colors = ["red", "blue"]
        pieces_dict = {}
        for n in range(len(colors)):
            player_id = 100 + n * 100
            color = colors[n]
            pieces_dict[player_id + 1] = Piece('F', color, "Flag", player_id + 1)
            for i in range(1, 11):
                for j in range(s_to_n_and_n[i][1]):
                    pieces_dict[player_id + i + j + 1] = Piece(i, color, s_to_n_and_n[i][0], player_id + i + j + 1)
            for i in range(1, 4):
                pieces_dict[player_id + 37 + i] = Piece('B', color, "Bomb", player_id + 37 + i)

        return pieces_dict

    # Takes id as a parameter and returns the piece object
    def get_piece_by_id(self, piece_id):
        return self.pieces_dict[piece_id]

    # Takes a dictionary of piece objects to their positions and sets the board object accordingly.
    def set_board(self, piece_to_position_dict):
        for piece, position in piece_to_position_dict.items():
            self.board.set_new_piece_position(piece, position)

        self.board_set = True

    # Function takes piece object and position as parameters. If position is free, the piece will move.
    # If not, the piece will attack the defending piece. The function returns a boolean that represents whether the
    # action was successful.
    def piece_act(self, piece, new_position):
        piece_in_new_position = self.board.get_piece_in_position(new_position)
        if not piece_in_new_position:
            self.board.set_new_piece_position(piece, new_position)
            return True

        else:
            self.piece_attack(piece, piece_in_new_position, new_position)

    # Checks which piece is stronger and returns True if the attacker won, False otherwise.
    def piece_attack(self, piece, piece_to_attack, new_position):
        winner = AttackingRules.check_battle_winner(piece, piece_to_attack)
        if winner == piece:
            self.board.set_new_piece_position(piece, new_position)
            return True
        return False

    # Takes a piece id as a parameter and returns a list of the possible positions that the piece can move to.
    def return_piece_options(self, piece_id):
        piece = self.get_piece_by_id(piece_id)
        return MovementRules.calculate_possible_moves(piece, self.board)

    # Takes the set and
    def set_color_pieces(self, id_to_pos_dict):
        for piece_id, position in id_to_pos_dict.items():
            piece = self.get_piece_by_id(piece_id)
            self.board.set_new_piece_position(piece, position)
        if self.board.get_piece_count() == 40:
            self.board_set = True
