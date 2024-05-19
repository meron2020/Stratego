# Importing the database module from the FlaskServer configuration
from Backend.FlaskServer.db import db


# Defining the User model class inheriting from db.Model
class User(db.Model):
    # Specify the name of the table in the database
    __tablename__ = 'users'

    # Define columns for the user table
    id = db.Column(db.Integer, primary_key=True)  # Unique identifier for each user
    username = db.Column(db.String(80))  # Username field limited to 80 characters
    password = db.Column(db.String(80))  # Password field limited to 80 characters
    wins = db.Column(db.Integer)  # Integer to count the number of wins
    losses = db.Column(db.Integer)  # Integer to count the number of losses
    ties = db.Column(db.Integer)  # Integer to count the number of ties

    def __init__(self, username, password, wins=0, losses=0, ties=0):
        # Initialize a new user instance.
        # param username: String, the username of the user.
        # param password: String, the password of the user.
        # param wins: Integer, default is 0, represents the number of wins.
        # param losses: Integer, default is 0, represents the number of losses.
        # param ties: Integer, default is 0, represents the number of ties.

        self.username = username
        self.password = password
        self.wins = wins
        self.losses = losses
        self.ties = ties

    def save_to_db(self):
        # Adds the current user instance to the database and commits the transaction.

        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        # Deletes the current user instance from the database and commits the transaction.

        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_id(cls, _id):
        # Class method to find a user by their ID.
        # param _id: Integer, the user ID.
        # return: User instance or None if not found.

        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_by_username(cls, username):
        # Class method to find a user by their username.
        # param username: String, the username.
        # return: User instance or None if not found.

        return cls.query.filter_by(username=username).first()

    @classmethod
    def add_win_to_user(cls, user_id):
        # Class method to increment the win count of a user by ID.
        # param user_id: Integer, the user ID.

        user = cls.find_by_id(user_id)
        user.add_win()
        user.save_to_db()

    @classmethod
    def add_loss_to_user(cls, user_id):
        # Class method to increment the loss count of a user by ID.
        # param user_id: Integer, the user ID.

        user = cls.find_by_id(user_id)
        user.add_loss()
        user.save_to_db()

    @classmethod
    def add_tie_to_user(cls, user_id):
        # Class method to increment the tie count of a user by ID.
        # param user_id: Integer, the user ID.

        user = cls.find_by_id(user_id)
        user.add_tie()
        user.save_to_db()

    def add_win(self):
        # Increments the user's win count by one.
        self.wins += 1

    def add_loss(self):
        # Increments the user's loss count by one.

        self.losses += 1

    def add_tie(self):
        # Increments the user's tie count by one.

        self.ties += 1
