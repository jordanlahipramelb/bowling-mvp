from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
import datetime

db = SQLAlchemy()

bcrypt = Bcrypt()


# (app) from app.py
def connect_db(app):
    db.app = app
    db.init_app(app)


class Bowler(db.Model):
    __tablename__ = "bowlers"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.Text, nullable=False)
    last_name = db.Column(db.Text, nullable=False)
    username = db.Column(db.Text, nullable=False, unique=True)

    password = db.Column(db.Text, nullable=False)

    # start_register
    @classmethod
    def register(cls, username, pwd):
        """Register user w/hashed password & return user."""

        hashed = bcrypt.generate_password_hash(pwd)

        hashed_utf8 = hashed.decode("utf8")

        return cls(username=username, password=hashed_utf8)

    # start_authenticate
    @classmethod
    def authenticate(cls, username, pwd):
        """Validate that user exists & password is correct.

        Return user if valid; else return False.
        """

        # searches for the user
        user = Bowler.query.filter_by(username=username).first()

        if user and bcrypt.check_password_hash(user.password, pwd):
            return user
        else:
            return False

    def __repr__(self):
        u = self
        return f"<User id = {u.id}, first_name = {u.first_name}, last_name = {u.last_name}>"


class Scorecard(db.Model):
    __tablename__ = "scorecards"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    bowler_id = db.Column(db.Integer, db.ForeignKey("bowlers.id"))
    frame_0 = db.Column(db.Text, nullable=False, default=0)
    frame1_ball1 = db.Column(db.Integer, default=0)
    frame1_ball2 = db.Column(db.Integer, default=0)
    frame2_ball1 = db.Column(db.Integer, default=0)
    frame2_ball2 = db.Column(db.Integer, default=0)
    frame3_ball1 = db.Column(db.Integer, default=0)
    frame3_ball2 = db.Column(db.Integer, default=0)
    frame4_ball1 = db.Column(db.Integer, default=0)
    frame4_ball2 = db.Column(db.Integer, default=0)
    frame5_ball1 = db.Column(db.Integer, default=0)
    frame5_ball2 = db.Column(db.Integer, default=0)
    frame6_ball1 = db.Column(db.Integer, default=0)
    frame6_ball2 = db.Column(db.Integer, default=0)
    frame7_ball1 = db.Column(db.Integer, default=0)
    frame7_ball2 = db.Column(db.Integer, default=0)
    frame8_ball1 = db.Column(db.Integer, default=0)
    frame8_ball2 = db.Column(db.Integer, default=0)
    frame9_ball1 = db.Column(db.Integer, default=0)
    frame9_ball2 = db.Column(db.Integer, default=0)
    frame10_ball1 = db.Column(db.Integer, default=0)
    frame10_ball2 = db.Column(db.Integer, default=0)
    frame10_ball3 = db.Column(db.Integer, default=0)
    total = db.Column(db.Integer, nullable=False)


class DateLocation(db.Model):

    __tablename__ = "dates_locations"

    id = db.Column(db.Integer, db.ForeignKey("scorecards.id"), primary_key=True)
    bowler_id = db.Column(db.Integer, db.ForeignKey("bowlers.id"))
    date = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now)
    location = db.Column(db.Text, nullable=False)


class BowlerScore(db.Model):

    __tablename__ = "bowlers_scores"

    bowler_id = db.Column(db.Integer, db.ForeignKey("bowlers.id"), primary_key=True)
    scorecard_id = db.Column(db.Integer, db.ForeignKey("scorecards.id"), primary_key=True)
