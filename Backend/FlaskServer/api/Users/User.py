from Backend.FlaskServer.db import db


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    password = db.Column(db.String(80))
    wins = db.Column(db.Integer)
    losses = db.Column(db.Integer)
    ties = db.Column(db.Integer)

    def __init__(self, username, password, wins=0, losses=0, ties=0):
        # Initialize a User object with the provided attributes.
        # Parameters:
        # - player_id (int): The unique identifier for the user.
        # - username (str): The username of the user.
        # - password (str): The password of the user.
        # - wins (int): The number of wins the user has (default is 0).
        # - losses (int): The number of losses the user has (default is 0).
        # - ties (int): The number of ties the user has (default is 0).
        self.username = username
        self.password = password
        self.wins = wins
        self.losses = losses
        self.ties = ties

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def add_win_to_user(cls, user_id):
        user = User.find_by_id(user_id)
        user.add_win()
        user.save_to_db()

    @classmethod
    def add_loss_to_user(cls, user_id):
        user = User.find_by_id(user_id)
        user.add_loss()
        user.save_to_db()

    @classmethod
    def add_tie_to_user(cls, user_id):
        user = User.find_by_id(user_id)
        user.add_tie()
        user.save_to_db()

    def add_win(self):
        # Increment the wins count for the user by 1.
        self.wins += 1

    def add_loss(self):
        # Increment the losses count for the user by 1.
        self.losses += 1

    def add_tie(self):
        # Increment the ties count for the user by 1.
        self.ties += 1
