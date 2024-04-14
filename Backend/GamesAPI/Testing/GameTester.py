from Backend.GamesAPI.Game.Game import Game
from Backend.GamesAPI.Game.GameBoard import GameBoard
from Backend.GamesAPI.Game.Piece import Piece
from Backend.GamesAPI.GameHandler.GamesHandler import GamesHandler


class GameTester:
    @classmethod
    def create_test_game(cls):
        test_game = Game(1)
        test_game.two_players_connected = True
        test_game.game_state = "Running"
        test_game.turn_id = 1
        test_game.pieces_dict = GameTester.create_piece_dict()
        test_game.board = GameTester.create_board(test_game.pieces_dict)
        test_game.turn_color = "red"
        test_game.turn = 1
        test_game.player_to_color_dict = {"1": "red", "2": "blue"}

        GamesHandler.turn_to_json(test_game)

    @classmethod
    def create_board(cls, piece_dict):
        board_matrix = [[[] for j in range(10)] for i in range(10)]
        for piece_id, piece in piece_dict.items():
            board_matrix[piece.position[0]][piece.position[1]] = piece_id
        board = GameBoard(board_matrix)
        return board

    @classmethod
    def create_piece_dict(cls):
        piece = Piece(2, "red", "Scout", 105, [5, 9])
        piece1 = Piece(2, "blue", "Scout", 204, [5, 8])
        piece2 = Piece(3, "blue", "Miner", 203, [2, 1])
        piece3 = Piece(2, "red", "Scout", 103, [3, 8])
        flag1 = Piece('F', "red", "Flag", 101, [4, 2])
        flag2 = Piece('F', "blue", "Flag", 201, [3, 2])

        piece_dict = {105: piece, 204: piece1, 203: piece2, 101: flag1, 201: flag2, 103: piece3}
        return piece_dict


GameTester.create_test_game()
