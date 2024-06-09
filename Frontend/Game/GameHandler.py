import threading
import time

from Frontend.App.GameResultPage import GameResultPage
from Frontend.Game.Board import Board
from Frontend.Game.PlayThroughHandler import PlayThroughHandler
from Frontend.Game.PlayerHandler import PlayerHandler
from Frontend.Game.SetupHandler import SetupHandler
from Frontend.ServerCommunications.GameHTTPHandler import GameHTTPHandler


class GameHandler:
    # Initializer for the GameHandler class
    def __init__(self, player_id, screen_handler, server_address, test=False):
        self.screen_handler = screen_handler  # Handles screen related tasks
        self.server_address = server_address  # Address of the server for HTTP communication
        self.player_id = player_id  # Unique identifier for the player
        if test:
            self.test_setup_handler()  # Setup for testing environment
        else:
            self.set_up_game_handler()  # Setup for production environment
        self.opponent_player_connected = False  # Flag to track the connection status of the opponent

    # Method to setup the game handler for actual game play
    def set_up_game_handler(self):
        self.httpHandler = GameHTTPHandler(self.server_address)  # Handles HTTP communication with the game server

        self.game_id = self.httpHandler.join_game(self.player_id)["game_id"]  # Joins a game and retrieves the game ID
        self.board = Board(self.screen_handler.screen, margin_percentage=0.05)  # Sets up the game board
        self.player_handler = PlayerHandler(self.player_id, self.board, self.screen_handler, self.httpHandler,
                                            self.game_id)  # Handles player interactions
        self.setup_handler = SetupHandler(self.player_id, self.screen_handler, self.board, self.game_id,
                                          self.player_handler, self.httpHandler)  # Handles game setup
        self.play_through_handler = PlayThroughHandler(self.httpHandler, self.board, self.game_id, self.player_handler,
                                                       self.player_id,
                                                       self.screen_handler)  # Handles gameplay logic

    # Setup handler for testing environment, similar to the production but uses a fixed server address and game ID
    def test_setup_handler(self):
        self.httpHandler = GameHTTPHandler("http://127.0.0.1:5000")
        self.game_id = 1
        self.board = Board(self.screen_handler.screen, margin_percentage=0.05)
        self.player_handler = PlayerHandler(self.player_id, self.board, self.screen_handler,
                                            self.httpHandler, self.game_id)
        self.setup_handler = SetupHandler(self.player_id, self.screen_handler, self.board, self.game_id,
                                          self.player_handler, self.httpHandler)
        self.play_through_handler = PlayThroughHandler(self.httpHandler, self.board, self.game_id,
                                                       self.player_handler, self.player_id, self.screen_handler)

    # Main game loop for handling the complete game process
    def game_loop(self):
        finished = self.setup_handler.run_setup_loop()  # Run the setup loop
        if finished == "Opponent Quit":
            result = True
        elif finished:
            self.setup_handler.await_opponent_player_setup()  # Wait for the opponent's setup to complete
            result = self.play_through_handler.run_play_through_loop()  # Execute the main game play loop
        else:
            result = False
            forfeited = True
        result_page = GameResultPage(self.screen_handler)
        result_page.run(result)  # Display the game result page
        return

    # Game loop used for testing, similar to the main loop but might include specific conditions or configurations
    def test_game_loop(self):
        result = self.play_through_handler.run_play_through_loop()
        if result == "Opponent Quit":
            result = True
        if not result:
            result = False

        result_page = GameResultPage(self.screen_handler)
        result_page.run(result)

    # Checks the opponent's connection status in a loop
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

    # Spawns a thread to asynchronously check for opponent player connection
    def await_opponent_player_connect(self):
        check_thread = threading.Thread(target=self.check_opponent_connect)
        check_thread.daemon = True  # Daemonize the thread so it terminates when the main program exits
        check_thread.start()

        # Handles the pygame events while awaiting server response
        while not self.opponent_player_connected:
            self.screen_handler.event_handling_when_waiting()
