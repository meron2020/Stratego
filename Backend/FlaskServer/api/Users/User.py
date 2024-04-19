class User:
    def __init__(self, player_id, username, password, wins=0, losses=0, ties=0):
        self.player_id = player_id
        self.username = username
        self.password = password
        self.wins = wins
        self.losses = losses
        self.ties = ties

    def add_win(self):
        self.wins += 1

    def add_loss(self):
        self.losses += 1

    def add_tie(self):
        self.ties += 1
