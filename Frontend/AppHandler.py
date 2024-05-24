# Importing necessary modules from the application's structure
from Frontend.App.InstructionsPage import InstructionsPage
from Frontend.App.LoginPage import LoginPage
from Frontend.App.OptionsPage import OptionsPage
from Frontend.App.ScreenHandler import ScreenHandler
from Frontend.App.SignUpPage import SignUpPage
from Frontend.App.StatsPage import StatsPage
from Frontend.App.WelcomePage import WelcomePage
from Frontend.Game.GameHandler import GameHandler
from Frontend.ServerCommunications.UserHTTPHandler import UserHTTPHandler


class AppHandler:
    def __init__(self, http_address):
        # Initialize the application with the server address.
        self.server_address = http_address
        # Set up communication handler for user-related HTTP requests.
        self.user_http_handler = UserHTTPHandler(http_address)
        # Manage screens and transitions within the app.
        self.screen_handler = ScreenHandler()
        # Prepare the graphical user interface infrastructure.
        self.screen_handler.setup_app_infrastructure()
        # Create and display the welcome page.
        welcome_page = WelcomePage(self.screen_handler)
        signed_in = False
        # Continue prompting for login/sign up until successful.
        while not signed_in:
            user_option = welcome_page.create_page()
            signed_in = self.login_or_sign_up(user_option)
        # After sign-in, proceed to the options page.
        options_page = OptionsPage(self.screen_handler)
        # Main loop to handle user options until the application is exited.
        while True:
            option = options_page.run()
            self.user_option(option)

    def login_or_sign_up(self, user_option):
        # Handle user decisions to either log in or sign up.
        if user_option == "Sign Up":
            sign_up_page = SignUpPage(self.screen_handler, self.user_http_handler)
            response = sign_up_page.run()
            # If sign-up successful, store username and player ID.
            if response:
                self.username, self.player_id = response[0], response[1]
                return True
            else:
                return False
        else:
            login_page = LoginPage(self.screen_handler, self.user_http_handler)
            response = login_page.run()
            # If login successful, store username and player ID.
            if response:
                self.username, self.player_id = response[0], response[1]
                return True
            else:
                return False

    def get_stats(self):
        # Fetch and display the user's game statistics.
        stats = self.user_http_handler.get_stats(self.username)
        stats_page = StatsPage(self.screen_handler)
        stats_page.create_stats_page(self.username, stats["wins"], stats["losses"], stats["ties"])

    def instructions(self):
        # Display game instructions to the user.
        instructions_page = InstructionsPage(self.screen_handler)
        instructions_page.run()

    def user_option(self, option):
        # Handle options selected by the user from the options page.
        if option == "Join Game":
            self.join_game()
            return False
        elif option == "Get Stats":
            self.get_stats()
            return False
        elif option == "Instructions":
            self.instructions()
            return False

    def join_game(self):
        # Initialize and manage the game session.
        game_handler = GameHandler(self.player_id, self.screen_handler, self.server_address)
        game_handler.await_opponent_player_connect()
        game_handler.game_loop()
        return


if __name__ == "__main__":
    # Start the application with the specified server address.
    appHandler = AppHandler("http://127.0.0.1:5000")
