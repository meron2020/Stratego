from Backend.FlaskServer.db import db


class UserModel(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    password_hash = db.Column(db.String(50))
    wins = db.Column(db.Integer)
    losses = db.Column(db.Integer)
    ties = db.Column(db.Integer)

    def __init__(self, name, password_hash):
        self.name = name
        self.password_hash = password_hash
        self.wins = 0
        self.losses = 0
        self.ties = 0

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_by_id(cls, player_id):
        return cls.query.filter_by(id=player_id).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        try:
            db.session.delete(self)
            db.session.commit()
            return True
        except Exception:
            return False

    def add_win(self):
        self.wins += 1
        db.session.commit()

    def add_loss(self):
        self.losses += 1
        db.session.commit()

    def add_tie(self):
        self.losses += 1
        db.session.commit()

    @classmethod
    def get_stats(cls, username):
        user = cls.find_by_name(username)
        return {"user": user.name, "wins": user.wins, "losses": user.losses, "ties": user.ties}

    @classmethod
    def create_new_user(cls, name, password_hash):
        try:
            user = UserModel(name, password_hash)
            user.save_to_db()
            return {"user_created": True}
        except Exception:
            return {"user_created": False}

    @classmethod
    def delete_user(cls, username):
        user = cls.find_by_name(username)
        deleted = user.delete_from_db()
        return {"deleted": deleted}