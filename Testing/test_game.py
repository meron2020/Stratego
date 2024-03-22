import unittest
import json
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
        print(httpHandler.send_starting_positions(game_id, {}, 1))


if __name__ == '__main__':
    unittest.main()
