from Backend.GamesAPI.Game.GameBoard import GameBoard
from Backend.GamesAPI.Game.Piece import Piece
from Backend.GamesAPI.Game.Rules.AttackingRules import AttackingRules
from Backend.GamesAPI.Game.Rules.MovementRules import MovementRules
from Backend.GamesAPI.Game.Rules.VictoryRules import VictoryRules
from universals import strength_to_name_and_number_dict as s_to_n_and_n


# Game class is responsible for running the game.
class Game:
    # Game object constructor
    def __init__(self, game_id=1, players=[], board=GameBoard(), pieces_dict=None, turn=0,
                 player_to_color_dict={},
                 turn_id=None, turn_color="red", game_state="Awaiting Opponent Player Connect",
                 player_to_setup_pos_dict={}, two_players_connected=False, test=False):

        if test:
            print("test")

        self.player_to_setup_pos_dict = player_to_setup_pos_dict
        self.game_id = game_id
        self.board = board
        self.turn = turn
        self.player_to_color_dict = player_to_color_dict
        self.players = players
        if pieces_dict:
            self.pieces_dict = pieces_dict
        self.turn_id = turn_id
        self.turn_color = turn_color
        self.game_state = game_state
        self.one_player_connected = False
        self.two_players_connected = two_players_connected

    # Function takes a color as a parameter and returns the initial list of pieces set with that color.
    def create_pieces_dict(self):
        colors = ["red", "blue"]
        pieces_dict = {}
        for n in range(len(colors)):
            player_id = self.players[n] * 100
            color = colors[n]
            pieces_dict[player_id + 1] = Piece('F', color, "Flag", player_id + 1)
            counter = 102 + n * 100
            for i in range(1, 11):
                for j in range(s_to_n_and_n[i][1]):
                    pieces_dict[counter] = Piece(i, color, s_to_n_and_n[i][0], counter)
                    counter += 1
            for i in range(6):
                pieces_dict[counter] = Piece('B', color, "Bomb", counter)
                counter += 1

        return pieces_dict

    def get_opposite_player(self, player_id):
        for player in self.player_to_color_dict.keys():
            if player != str(player_id):
                return player

    def set_piece_new_pos_by_id(self, piece_id, new_pos):
        piece = self.get_piece_by_id(piece_id)
        piece.set_new_piece_position(new_pos)

    # Function takes piece object and position as parameters. If position is free, the piece will move.
    # If not, the piece will attack the defending piece. The function returns a boolean that represents whether the
    # action was successful.
    def piece_act(self, piece_id, new_position):
        winner = VictoryRules.check_player_is_winner(self.get_opposite_player(self.turn_id), self.pieces_dict)
        if not winner:
            piece_id_in_new_position = self.board.get_piece_id_in_position(new_position)
            if piece_id_in_new_position == []:
                self.board.set_new_piece_id_position(self.pieces_dict[str(piece_id)], new_position)
                self.set_piece_new_pos_by_id(piece_id, new_position)
            else:
                piece_in_new_position = self.get_piece_by_id(piece_id_in_new_position)
                self.piece_attack(piece_id, piece_in_new_position, new_position)
            winner = VictoryRules.check_player_is_winner(self.get_opposite_player(self.turn_id), self.pieces_dict)
            if winner:
                return self.end_game(self.turn_id, self.get_opposite_player(self.turn_id))
            if VictoryRules.check_tie(self.turn_id, self.get_opposite_player(self.turn_id), self.pieces_dict):
                return {"return_type": 2, "player_ids": self.players}
            if VictoryRules.check_player_is_winner(self.turn_id, self.pieces_dict):
                return self.end_game(self.get_opposite_player(self.turn_id), self.turn_id)
            if not winner:
                if self.turn_color == "red":
                    self.turn_color = "blue"
                else:
                    self.turn_color = "red"
                    self.turn += 1
                self.turn_id = self.get_opposite_player(self.turn_id)
                return None
        return self.end_game(self.get_opposite_player(self.turn_id), self.turn_id)

    # Deletes piece if lost a battle.
    def delete_piece(self, piece_id):
        self.board.delete_piece(self.pieces_dict[str(piece_id)].position)
        self.pieces_dict.pop(str(piece_id))

    # Checks which piece is stronger and returns True if the attacker won, False otherwise.
    def piece_attack(self, piece_id, piece_to_attack, new_position):
        piece = self.get_piece_by_id(piece_id)
        winner = AttackingRules.check_battle_winner(piece, piece_to_attack)
        if winner == piece:
            self.board.set_new_piece_id_position(piece, new_position)
            self.pieces_dict.pop(str(piece_to_attack.piece_id))
        if not winner:
            self.delete_piece(piece_id)
            self.delete_piece(piece_to_attack.piece_id)
        else:
            self.delete_piece(piece_id)

    # Takes a piece id as a parameter and returns a list of the possible positions that the piece can move to.
    def return_piece_options(self, piece_id):
        piece = self.pieces_dict[str(piece_id)]
        return MovementRules.calculate_possible_moves(piece, self.board.get_board_matrix(), self.pieces_dict)

    # Takes dictionary of piece id to position and sets it to the board. If the piece amount on the board is 40, set
    # the board as ready to play.
    def set_color_pieces(self, id_to_pos_dict):
        for piece_id, position in id_to_pos_dict.items():
            piece = self.get_piece_by_id(piece_id)
            piece.set_new_piece_position(position)
            self.board.set_new_piece_id_position(piece, position)
            self.game_state = "Awaiting Opponent Player Setup"
        if self.board.get_piece_count() == 80:
            self.game_state = "Running"
            self.turn_id = 1

        return True

    # Getter method that returns the board object.
    def get_board(self):
        return self.board.get_board_matrix()

    # Function adds player to game, and assigns them their relevant values depending on whether they are the first or
    # the second player to connect. Returns true if connection successful, false otherwise.
    def connect_to_game(self, player_id):
        if len(self.player_to_color_dict.keys()) == 0:
            self.player_to_color_dict[player_id] = "red"
            self.players.append(player_id)
            self.game_state = "Awaiting Opponent Player Connect"
            self.player_to_setup_pos_dict[player_id] = "bottom"
            self.one_player_connected = True
            return True
        elif len(self.player_to_color_dict.keys()) == 1:
            self.player_to_color_dict[player_id] = "blue"
            self.two_players_connected = True
            self.players.append(player_id)
            self.pieces_dict = self.create_pieces_dict()
            self.game_state = "Awaiting setups"
            self.player_to_setup_pos_dict[player_id] = "top"
            return True
        else:
            return False

    # Getter method that returns True if board is ready to play and False otherwise based on the board_set variable.
    def get_state(self):
        return self.game_state

    # Takes id as a parameter and returns the piece object
    def get_piece_by_id(self, piece_id):
        return self.pieces_dict[str(piece_id)]

    # Function returns true if game is running and false otherwise.
    def check_game_still_running(self):
        return (self.game_state == "Awaiting setups" or self.game_state == "Running" or
                self.game_state == "Awaiting Opponent Player Setup")

    # Function ends the game. Removes the player that ended the game from the player list.
    # Updates the game state, and returns to the player that ended the game the result.
    def end_game(self, winner, loser):
        self.players.remove(winner)
        self.game_state = "Awaiting opponent disconnect"
        self.winner = winner
        self.loser = loser
        return {"winner": winner,
                "loser": loser, "game_state": self.game_state}

    # Function takes an object as a parameter and returns a
    # dictionary with instance variable names as keys and the values themselves as values
    @staticmethod
    def object_to_dict(obj):
        if isinstance(obj, list):
            return [Game.object_to_dict(item) for item in obj]
        elif isinstance(obj, dict):
            return {key: Game.object_to_dict(value) for key, value in obj.items()}
        elif hasattr(obj, '__dict__'):
            return {key: Game.object_to_dict(value) for key, value in obj.__dict__.items() if not callable(value)}
        else:
            return obj
