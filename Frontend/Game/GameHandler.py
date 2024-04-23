import threading
import time

from Frontend.App.ScreenHandler import ScreenHandler
from Frontend.Game.Board import Board
from Frontend.Game.PlayThroughHandler import PlayThroughHandler
from Frontend.Game.PlayerHandler import PlayerHandler
from Frontend.Game.SetupHandler import SetupHandler
from Frontend.ServerCommunications.GameHTTPHandler import GameHTTPHandler


class GameHandler:
    def __init__(self, player_id, screen_handler):
        self.screen_handler = screen_handler
        self.player_id = player_id
        self.set_up_game_handler()
        self.opponent_player_connected = False

    def set_up_game_handler(self):
        self.httpHandler = GameHTTPHandler("http://127.0.0.1:5000")
        #self.game_id = self.httpHandler.join_game(self.player_id)["game_id"]
        self.game_id = 1
        self.board = Board(self.screen_handler.screen, margin_percentage=0.05)
        self.player_handler = PlayerHandler(self.player_id, self.board, self.screen_handler.screen, self.httpHandler,
                                            self.game_id)
        self.setup_handler = SetupHandler(self.player_id, self.screen_handler, self.board, self.game_id,
                                          self.player_handler, self.httpHandler)
        self.play_through_handler = PlayThroughHandler(self.httpHandler, self.board, self.game_id, self.player_handler,
                                                       self.player_id, self.screen_handler.screen)

    def game_loop(self):
        # self.setup_handler.run_setup_loop()
        # self.setup_handler.await_opponent_player_setup()
        self.play_through_handler.run_play_through_loop()

    def check_opponent_connect(self):
        while True:
            response = self.httpHandler.get_game_state(self.game_id)
            if response["game_state"] == "Awaiting Opponent Player Connect":
                time.sleep(2)
                continue
            else:
                break
        self.opponent_player_connected = True
        return

    def await_opponent_player_connect(self):
        check_thread = threading.Thread(target=self.check_opponent_connect)
        check_thread.daemon = True  # Daemonize the thread so it terminates when the main program exits
        check_thread.start()

        # Function for handling the pygame while awaiting the server response.
        while not self.opponent_player_connected:
            ScreenHandler.event_handling_when_waiting()
