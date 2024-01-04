from GameBoard import GameBoard
from Piece import Piece
from Rules.AttackingRules import AttackingRules
from Rules.MovementRules import MovementRules
from universals import strength_to_name_and_number_dict as s_to_n_and_n


# Game class is responsible for running the game.
class Game:
    def __init__(self, game_id):
        self.game_id = game_id
        self.board = GameBoard()
        self.pieces_dict = Game.create_pieces_dict()
        self.turn = 0
        self.player_to_color_dict = {}
        self.turn_id = "red"
        self.board_set = False
        self.two_players_connected = False

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

    def get_pieces_dict(self):
        return self.pieces_dict

    def get_opposite_player(self, player_id):
        for player in self.player_to_color_dict.keys():
            if player != player_id:
                return player

    def set_piece_new_pos_by_id(self, piece_id, new_pos):
        piece = self.get_piece_by_id(piece_id)
        piece.set_new_piece_position(new_pos)

    # Function takes piece object and position as parameters. If position is free, the piece will move.
    # If not, the piece will attack the defending piece. The function returns a boolean that represents whether the
    # action was successful.
    def piece_act(self, piece_id, new_position):
        piece_id_in_new_position = self.board.get_piece_id_in_position(new_position)

        if not piece_id_in_new_position:
            self.board.set_new_piece_id_position(piece_id, new_position)
            self.set_piece_new_pos_by_id(piece_id, new_position)

        else:
            piece_in_new_position = self.get_piece_by_id(piece_id_in_new_position)
            self.piece_attack(piece_id, piece_in_new_position, new_position)

        if self.turn_color == "red":
            self.turn_color = "blue"
        else:
            self.turn_color = "red"
            self.turn += 1

    # Deletes piece if lost a battle.
    def delete_piece(self, piece_id):
        self.board.delete_piece(self.pieces_dict[piece_id].position)
        self.pieces_dict.pop(piece_id)

    # Checks which piece is stronger and returns True if the attacker won, False otherwise.
    def piece_attack(self, piece_id, piece_to_attack, new_position):
        piece = self.get_piece_by_id(piece_id)
        winner = AttackingRules.check_battle_winner(piece, piece_to_attack)
        if winner == piece:
            self.board.set_new_piece_id_position(piece_id, new_position)
        else:
            self.delete_piece(piece_id)

    # Takes a piece id as a parameter and returns a list of the possible positions that the piece can move to.
    def return_piece_options(self, piece_id):
        return MovementRules.calculate_possible_moves(piece_id, self.board)

    # Takes dictionary of piece id to position and sets it to the board. If the piece amount on the board is 40, set
    # the board as ready to play.
    def set_color_pieces(self, id_to_pos_dict):
        for piece_id, position in id_to_pos_dict.items():
            piece = self.get_piece_by_id(piece_id)
            piece.set_new_piece_position(position)
            self.board.set_new_piece_id_position(piece_id, position)
        if self.board.get_piece_count() == 40:
            self.board_set = True

    # Getter method that returns the board object.
    def get_board(self):
        return self.board.get_board_matrix()

    def connect_to_game(self, player_id):
        if len(self.player_to_color_dict.keys()) == 0:
            self.player_to_color_dict[player_id] = "red"
        elif len(self.player_to_color_dict.keys()) == 1:
            self.player_to_color_dict[player_id] = "blue"
            self.two_players_connected = True
        else:
            return False

    # Getter method that returns True if board is ready to play and False otherwise based on the board_set variable.
    def board_ready_to_play(self):
        return self.board_set

    # Takes id as a parameter and returns the piece object
    def get_piece_by_id(self, piece_id):
        return self.pieces_dict[piece_id]

    def get_player_id_by_turn(self):
        return self.player_to_color_dict[self.turn_color]

    def end_game(self, player_id):
        return {"winner": self.get_opposite_player(player_id),
                "loser": player_id}


