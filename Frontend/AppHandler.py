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
        self.server_address = http_address
        self.user_http_handler = UserHTTPHandler(http_address)
        self.screen_handler = ScreenHandler()
        self.screen_handler.setup_app_infrastructure()
        welcome_page = WelcomePage(self.screen_handler)
        signed_in = False
        while not signed_in:
            user_option = welcome_page.create_page()
            signed_in = self.login_or_sign_up(user_option)
        options_page = OptionsPage(self.screen_handler)
        while True:
            option = options_page.run()
            self.user_option(option)

    def login_or_sign_up(self, user_option):
        if user_option == "Sign Up":
            sign_up_page = SignUpPage(self.screen_handler, self.user_http_handler)
            response = sign_up_page.run()
            if response:
                self.username, self.player_id = response[0], response[1]
                return True
            else:
                return False
        else:
            login_page = LoginPage(self.screen_handler, self.user_http_handler)
            response = login_page.run()
            if response:
                self.username, self.player_id = response[0], response[1]
                return True
            else:
                return False

    def get_stats(self):
        stats = self.user_http_handler.get_stats(self.username)
        stats_page = StatsPage(self.screen_handler)
        stats_page.create_stats_page(self.username, stats["wins"], stats["losses"], stats["ties"])

    def instructions(self):
        instructions_page = InstructionsPage(self.screen_handler)
        instructions_page.run()

    def user_option(self, option):
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
        game_handler = GameHandler(self.player_id, self.screen_handler, self.server_address)
        game_handler.await_opponent_player_connect()
        game_handler.game_loop()
        return


if __name__ == "__main__":
    appHandler = AppHandler("http://10.116.3.101:5000")
