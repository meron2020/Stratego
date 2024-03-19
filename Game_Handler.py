import time

import pygame
from bidict import bidict
from Frontend.ServerCommunications.GameHTTPHandler import GameHTTPHandler
from Testing.board_test import Board


class GameHandler:
    def __init__(self, server_address, game_id, player_id):
        self.game_id = game_id
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.player_id = player_id
        self.server_address = server_address
        self.board = Board(self.screen, margin_percentage=0.05)
        self.http_handler = GameHTTPHandler(self.server_address)

    def send_setup(self, player_id):
        piece_to_pos_dict = self.board.create_piece_to_pos_dict()
        response = self.http_handler.send_starting_positions(self.game_id, piece_to_pos_dict, player_id)
        print(response)

    def await_other_player_finish_setup(self):
        while True:
            response = self.http_handler.get_game_state(self.game_id)
            if response["game_state"] == "Running":
                break
            time.sleep(1)
        return True

    def check_if_my_turn(self):
        while True:
            response = self.http_handler.check_if_my_turn(self.game_id, self.player_id)
            if response["request_owner_turn"]:
                return True
            time.sleep(1)

    def display_piece_options(self, piece):
        response = self.http_handler.check_piece_options(self.game_id, piece.piece_id)
        options = response["piece_options"]
        for option in options:
            self.board.color_square(option, (0, 255, 0))

        return options

    def send_new_piece_pos(self, piece, pos):
        response = self.http_handler.piece_act(self.game_id, piece.piece_id, pos)

    def get_state(self):
        return self.http_handler.get_game_state(self.game_id)

    def get_game_board(self):
        return self.http_handler.get_board(self.game_id)


