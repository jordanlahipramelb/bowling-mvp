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
    email = db.Column(db.Text, nullable=False, unique=True)
    image_url = db.Column(
        db.Text,
        default="/static/images/default-pic.jpg",
    )

    teams = db.relationship("Team", secondary="bowlers_teams", backref="bowlers")

    # start_register
    @classmethod
    def register(cls, first_name, last_name, username, password, email, image_url):
        """Register bowler w/hashed password & return bowler."""

        hashed_utf8 = bcrypt.generate_password_hash(password).decode("utf8")

        bowler = Bowler(
            first_name=first_name,
            last_name=last_name,
            username=username,
            password=hashed_utf8,
            email=email,
            image_url=image_url,
        )

        db.session.add(bowler)
        return bowler

    # start_authenticate
    @classmethod
    def authenticate(cls, username, pwd):
        """Validate that bowler exists & password is correct.

        Return bowler if valid; else return False.
        """

        # searches for the bowler
        bowler = cls.query.filter_by(username=username).first()

        if bowler and bcrypt.check_password_hash(bowler.password, pwd):
            return bowler
        else:
            return False

    def __repr__(self):
        u = self
        return f"<Bowler id = {u.id}, first_name = {u.first_name}, last_name = {u.last_name}>"


class Team(db.Model):
    __tablename__ = "teams"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    team_name = db.Column(db.Text, nullable=False, unique=True)


class BowlerTeam(db.Model):
    __tablename__ = "bowlers_teams"

    bowler_id = db.Column(db.Integer, db.ForeignKey("bowlers.id"), primary_key=True)
    team_id = db.Column(db.Integer, db.ForeignKey("teams.id"), primary_key=True)


class League(db.Model):
    __tablename__ = "leagues"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text, nullable=False)
    date = db.Column(db.Text)
    location = db.Column(db.Text)


class TeamLeague(db.Model):
    """Which teams are a part of which leagues."""

    __tablename__ = "teams_leagues"

    team_id = db.Column(db.Integer, db.ForeignKey("teams.id"), primary_key=True)
    league_id = db.Column(db.Integer, db.ForeignKey("leagues.id"), primary_key=True)


class Match(db.Model):
    __tablename__ = "matches"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    league_id = db.Column(db.Integer, db.ForeignKey("leagues.id"))
    date = db.Column(db.Text, nullable=False)
    team_1_id = db.Column(db.Integer, db.ForeignKey("teams.id"))
    team_2_id = db.Column(db.Integer, db.ForeignKey("teams.id"))


class Scorecard(db.Model):
    __tablename__ = "scorecards"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    bowler_id = db.Column(db.Integer, db.ForeignKey("bowlers.id"))
    date = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now)
    location = db.Column(db.Text, nullable=False)

    frame1_1_pins = db.Column(db.Text)
    frame1_2_pins = db.Column(db.Text)
    frame1_score = db.Column(db.Text)
    frame2_1_pins = db.Column(db.Text)
    frame2_2_pins = db.Column(db.Text)
    frame2_score = db.Column(db.Text)
    frame3_1_pins = db.Column(db.Text)
    frame3_2_pins = db.Column(db.Text)
    frame3_score = db.Column(db.Text)
    frame4_1_pins = db.Column(db.Text)
    frame4_2_pins = db.Column(db.Text)
    frame4_score = db.Column(db.Text)
    frame5_1_pins = db.Column(db.Text)
    frame5_2_pins = db.Column(db.Text)
    frame5_score = db.Column(db.Text)
    frame6_1_pins = db.Column(db.Text)
    frame6_2_pins = db.Column(db.Text)
    frame6_score = db.Column(db.Text)
    frame7_1_pins = db.Column(db.Text)
    frame7_2_pins = db.Column(db.Text)
    frame7_score = db.Column(db.Text)
    frame8_1_pins = db.Column(db.Text)
    frame8_2_pins = db.Column(db.Text)
    frame8_score = db.Column(db.Text)
    frame9_1_pins = db.Column(db.Text)
    frame9_2_pins = db.Column(db.Text)
    frame9_score = db.Column(db.Text)
    frame10_1_pins = db.Column(db.Text)
    frame10_2_pins = db.Column(db.Text)
    frame10_3_pins = db.Column(db.Text)
    frame10_score = db.Column(db.Text)
    total_score = db.Column(db.Text, nullable=False)

    # frame_number = db.Column(db.Text)
    # ball_number = db.Column(db.Text)
    # frame_score = db.Column(db.Text)
    # total_score = db.Column(db.Text, nullable=False)
