import json
import unittest

from Backend.GamesAPI.Game.Game import Game
from Backend.GamesAPI.GameHandler.GamesHandler import GamesHandler
from Frontend.GUI.GUIHandler import GUIHandler
from Frontend.ServerCommunications.GameHTTPHandler import GameHTTPHandler


class MyTestCase(unittest.TestCase):

    def test_create_game(self):
        game = Game(1, [1, 2])
        GamesHandler.turn_to_json(game)
        returned_game = GamesHandler.get_from_json(1)
        self.assertEqual(
            json.dumps(Game.object_to_dict(game), sort_keys=True) == json.dumps(Game.object_to_dict(returned_game),
                                                                                sort_keys=True), True)

    def test_delete_game(self):
        self.assertEqual(GamesHandler.delete_game(1), True)

    def test_post(self):
        GamesHandler.delete_game(1)
        GamesHandler.post(1)
        self.assertEqual(GamesHandler.post(2), {"status": "game ready to play"})

    def test_put(self):
        httpHandler = GameHTTPHandler("http://127.0.0.1:5000")
        game_id = httpHandler.join_game(1)["game_id"]
        httpHandler.join_game(2)
        print(httpHandler.send_starting_positions(game_id,
                                                  {138: (6, 0), 137: (6, 1), 128: (6, 2), 126: (6, 3), 123: (6, 4),
                                                   111: (6, 5), 115: (6, 6), 101: (6, 7), 102: (6, 8), 103: (6, 9),
                                                   139: (7, 0), 136: (7, 1), 127: (7, 2), 125: (7, 3), 122: (7, 4),
                                                   112: (7, 5), 116: (7, 6), 104: (7, 7), 105: (7, 8), 106: (7, 9),
                                                   135: (8, 0), 140: (8, 1), 129: (8, 2), 124: (8, 3), 121: (8, 4),
                                                   113: (8, 5), 117: (8, 6), 107: (8, 7), 118: (8, 8), 119: (8, 9),
                                                   131: (9, 0), 132: (9, 1), 133: (9, 2), 134: (9, 3), 114: (9, 4),
                                                   130: (9, 5), 120: (9, 6), 108: (9, 7), 110: (9, 8), 109: (9, 9)}, 1))

    def test_put_action(self):
        httpHandler = GameHTTPHandler("http://127.0.0.1:5000")
        game_id = httpHandler.join_game(1)["game_id"]
        httpHandler.join_game(2)
        httpHandler.send_starting_positions(game_id,
                                            {138: (6, 0), 137: (6, 1), 128: (6, 2), 126: (6, 3), 123: (6, 4),
                                             111: (6, 5), 115: (6, 6), 101: (6, 7), 102: (6, 8), 103: (6, 9),
                                             139: (7, 0), 136: (7, 1), 127: (7, 2), 125: (7, 3), 122: (7, 4),
                                             112: (7, 5), 116: (7, 6), 104: (7, 7), 105: (7, 8), 106: (7, 9),
                                             135: (8, 0), 140: (8, 1), 129: (8, 2), 124: (8, 3), 121: (8, 4),
                                             113: (8, 5), 117: (8, 6), 107: (8, 7), 118: (8, 8), 119: (8, 9),
                                             131: (9, 0), 132: (9, 1), 133: (9, 2), 134: (9, 3), 114: (9, 4),
                                             130: (9, 5), 120: (9, 6), 108: (9, 7), 110: (9, 8), 109: (9, 9)}, 1)
        httpHandler.send_starting_positions(game_id,
                                            {238: (0, 0), 237: (0, 1), 228: (0, 2), 226: (0, 3), 223: (0, 4),
                                             211: (0, 5), 215: (0, 6), 201: (0, 7), 202: (0, 8), 203: (0, 9),
                                             239: (1, 0), 236: (1, 1), 227: (1, 2), 225: (1, 3), 222: (1, 4),
                                             212: (1, 5), 216: (1, 6), 204: (1, 7), 205: (1, 8), 206: (1, 9),
                                             235: (2, 0), 240: (2, 1), 229: (2, 2), 224: (2, 3), 221: (2, 4),
                                             213: (2, 5), 217: (2, 6), 207: (2, 7), 218: (2, 8), 219: (2, 9),
                                             231: (3, 0), 232: (3, 1), 233: (3, 2), 234: (3, 3), 214: (3, 4),
                                             230: (3, 5), 220: (3, 6), 208: (3, 7), 210: (3, 8), 209: (3, 9)}, 2)

    def test_get_board(self):
        httpHandler = GameHTTPHandler("http://127.0.0.1:5000")
        response_dict = httpHandler.get_board(1)
        guiHandler = GUIHandler(1)
        guiHandler.game_id = 1
        sprite_group = guiHandler.create_pieces_sprites_from_get_request(response_dict["pieces_dict"])
        guiHandler.sprite_group = sprite_group
        guiHandler.run_game_loop()


if __name__ == '__main__':
    unittest.main()


def test_get_board():
    httpHandler = GameHTTPHandler("http://127.0.0.1:5000")
    response_dict = httpHandler.get_board(1)
    guiHandler = GUIHandler(1)
    guiHandler.game_id = 1
    sprite_group = guiHandler.create_pieces_sprites_from_get_request(response_dict["pieces_dict"])
    guiHandler.run_game_loop(sprite_group)

