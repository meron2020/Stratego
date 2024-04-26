class User:
    def __init__(self, player_id, username, password, wins=0, losses=0, ties=0):
        # Initialize a User object with the provided attributes.
        # Parameters:
        # - player_id (int): The unique identifier for the user.
        # - username (str): The username of the user.
        # - password (str): The password of the user.
        # - wins (int): The number of wins the user has (default is 0).
        # - losses (int): The number of losses the user has (default is 0).
        # - ties (int): The number of ties the user has (default is 0).
        self.player_id = player_id
        self.username = username
        self.password = password
        self.wins = wins
        self.losses = losses
        self.ties = ties

    def add_win(self):
        # Increment the wins count for the user by 1.
        self.wins += 1

    def add_loss(self):
        # Increment the losses count for the user by 1.
        self.losses += 1

    def add_tie(self):
        # Increment the ties count for the user by 1.
        self.ties += 1
