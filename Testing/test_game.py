import json
import unittest

from Backend.GamesAPI.Game.Game import Game
from Backend.GamesAPI.GameHandler.GamesHandler import GamesHandler
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


if __name__ == '__main__':
    unittest.main()
