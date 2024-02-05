import unittest

from Backend.GamesAPI.Game.Game import Game
from Backend.GamesAPI.GameHandler.GamesHandler import GamesHandler


class MyTestCase(unittest.TestCase):
    def test_something(self):
        self.assertEqual(True, False)  # add assertion here

    def test_game(self):
        game = Game(1, [1, 2])
        GamesHandler.turn_to_json(game)
        returned_game = GamesHandler.get_from_json(1)
        self.assertEqual(game.__dict__ == returned_game.__dict__, True)


if __name__ == '__main__':
    unittest.main()
