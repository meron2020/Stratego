from Frontend.App.LoginPage import LoginPage
from Frontend.App.OptionsPage import OptionsPage
from Frontend.App.ScreenHandler import ScreenHandler
from Frontend.App.SignUpPage import SignUpPage
from Frontend.App.StatsPage import StatsPage
from Frontend.App.WelcomePage import WelcomePage
from Frontend.Game.GameHandler import GameHandler
from Frontend.ServerCommunications.UserHTTPHandlers import UserHTTPHandler


class AppHandler:
    def __init__(self):
        self.user_http_handler = UserHTTPHandler("http://127.0.0.1:5000")
        self.screen_handler = ScreenHandler()
        self.screen_handler.setup_app_infrastructure()
        welcome_page = WelcomePage(self.screen_handler)
        user_option = welcome_page.create_page()
        self.login_or_sign_up(user_option)
        options_page = OptionsPage(self.screen_handler)
        option = options_page.run()
        self.user_option(option)

    def login_or_sign_up(self, user_option):
        if user_option == "Sign Up":
            sign_up_page = SignUpPage(self.screen_handler, self.user_http_handler)
            self.username, self.player_id = sign_up_page.run()
        else:
            login_page = LoginPage(self.screen_handler, self.user_http_handler)
            self.username, self.player_id = login_page.run()

    def get_stats(self):
        stats = self.user_http_handler.get_stats(self.username)
        stats_page = StatsPage(self.screen_handler)
        stats_page.create_stats_page(self.username, stats["wins"], stats["losses"], stats["ties"])

    def user_option(self, option):
        if option == "Join Game":
            self.join_game()
        elif option == "Get Stats":
            self.get_stats()

    def join_game(self):
        game_handler = GameHandler(self.player_id, self.screen_handler)
        game_handler.await_opponent_player_connect()
        game_handler.game_loop()


if __name__ == "__main__":
    appHandler = AppHandler()
