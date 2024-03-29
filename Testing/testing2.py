import unittest

from Frontend.GUI.GUIHandler import GUIHandler
from Frontend.ServerCommunications.GameHTTPHandler import GameHTTPHandler


class MyTestCase(unittest.TestCase):
    def test_something(self):
        self.assertEqual(True, False)  # add assertion here

    def test_get_board(self):
        httpHandler = GameHTTPHandler("http://127.0.0.1:5000")
        response_dict = httpHandler.get_board(1)
        guiHandler = GUIHandler(1)
        guiHandler.game_id = 1
        sprite_group = guiHandler.create_pieces_sprites_from_get_request(response_dict["pieces_dict"])
        guiHandler.run_game_loop(sprite_group)


if __name__ == '__main__':
    unittest.main()
