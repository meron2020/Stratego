import unittest

from Frontend.Game.GameHandler import GameHandler
from Frontend.ServerCommunications.GameHTTPHandler import GameHTTPHandler
from Frontend.App.ScreenHandler import ScreenHandler


class MyTestCase(unittest.TestCase):

    #     def test_create_game(self):
    #         game = Game(1, [1, 2])
    #         GamesHandler.turn_to_json(game)
    #         returned_game = GamesHandler.get_from_json(1)
    #         self.assertEqual(
    #             json.dumps(Game.object_to_dict(game), sort_keys=True) == json.dumps(Game.object_to_dict(returned_game),
    # #                                                                                 sort_keys=True), True)
    #
    #     def test_delete_game(self):
    #         self.assertEqual(GamesHandler.delete_game(1), True)
    #
    #     def test_post(self):
    #         GamesHandler.delete_game(1)
    #         GamesHandler.post(1)
    #         self.assertEqual(GamesHandler.post(2), {"status": "game ready to play"})
    #
    #     def test_put(self):
    #         httpHandler = GameHTTPHandler("http://127.0.0.1:5000")
    #         game_id = httpHandler.join_game(1)["game_id"]
    #         httpHandler.join_game(2)
    #         handler = GameHandler()
    #         handler.game_id = game_id
    #         handler.run_setup_loop()
    #
    def test_put_action(self):
        httpHandler = GameHTTPHandler("http://127.0.0.1:5000")
        game_id = httpHandler.join_game(1)["game_id"]
        httpHandler.join_game(2)
        httpHandler.send_starting_positions(game_id,
                                            {138: (6, 0), 137: (6, 1), 128: (6, 2), 126: (6, 3), 123: (6, 9),
                                             111: (7, 7), 115: (6, 6), 101: (6, 7), 102: (6, 8), 103: (6, 4),
                                             139: (7, 0), 136: (7, 1), 127: (7, 2), 125: (7, 3), 122: (7, 4),
                                             112: (7, 5), 116: (7, 6), 104: (6, 5), 105: (7, 8), 106: (7, 9),
                                             135: (8, 0), 140: (8, 1), 129: (8, 2), 124: (8, 3), 121: (8, 4),
                                             113: (8, 5), 117: (8, 6), 107: (8, 7), 118: (8, 8), 119: (8, 9),
                                             131: (9, 0), 132: (9, 1), 133: (9, 2), 134: (9, 3), 114: (9, 4),
                                             130: (9, 5), 120: (9, 6), 108: (9, 7), 110: (9, 8), 109: (9, 9)}, 1)
        httpHandler.send_starting_positions(game_id,
                                            {238: (0, 0), 237: (0, 1), 228: (0, 2), 226: (0, 3), 223: (0, 4),
                                             211: (0, 5), 215: (0, 6), 201: (3, 5), 202: (3, 4), 203: (0, 8),
                                             239: (1, 0), 236: (1, 1), 227: (1, 2), 225: (1, 3), 222: (1, 4),
                                             212: (1, 5), 216: (1, 6), 204: (1, 7), 205: (1, 8), 206: (1, 9),
                                             235: (2, 0), 240: (2, 1), 229: (2, 2), 224: (2, 3), 221: (2, 4),
                                             213: (2, 5), 217: (2, 6), 207: (2, 7), 218: (2, 8), 219: (2, 9),
                                             231: (3, 0), 232: (3, 1), 233: (3, 2), 234: (3, 3), 214: (0, 9),
                                             230: (0, 7), 220: (3, 6), 208: (3, 7), 210: (3, 8), 209: (3, 9)}, 2)

    def test_get_board(self):
        screenHandler = ScreenHandler()
        screenHandler.setup_app_infrastructure()
        guiHandler = GameHandler(1, screenHandler, "http://127.0.0.1:5000", True)
        guiHandler.test_game_loop()

    def test_end_player_two(self):
        screenHandler = ScreenHandler()
        screenHandler.setup_app_infrastructure()
        guiHandler = GameHandler(2, screenHandler, "http://127.0.0.1:5000", True)
        guiHandler.test_game_loop()

    def test_send_setup(self):
        httpHandler = GameHTTPHandler("http://127.0.0.1:5000")
        httpHandler.send_starting_positions(1,
                                            {238: (0, 0), 237: (0, 1), 228: (0, 2), 226: (0, 3), 223: (0, 4),
                                             211: (0, 5), 215: (0, 6), 201: (0, 7), 202: (0, 8), 203: (0, 9),
                                             239: (1, 0), 236: (1, 1), 227: (1, 2), 225: (1, 3), 222: (1, 4),
                                             212: (1, 5), 216: (1, 6), 204: (1, 7), 205: (1, 8), 206: (1, 9),
                                             235: (2, 0), 240: (2, 1), 229: (2, 2), 224: (2, 3), 221: (2, 4),
                                             213: (2, 5), 217: (2, 6), 207: (2, 7), 218: (2, 8), 219: (2, 9),
                                             231: (3, 0), 232: (3, 1), 233: (3, 2), 234: (3, 3), 214: (3, 4),
                                             230: (3, 5), 220: (3, 6), 208: (3, 7), 210: (3, 8), 209: (3, 9)}, 2)
#
# async def test_get_board():
#     guiHandler = GameHandler()
#     guiHandler.game_id = 1
#     await guiHandler.game_loop()
#
#
# if __name__ == '__main__':
#     asyncio.run(test_get_board())