from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt


db = SQLAlchemy()

bcrypt = Bcrypt()


# (app) from app.py
def connect_db(app):
    db.app = app
    db.init_app(app)


class League(db.Model):
    __tablename__ = "leagues"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text, nullable=False, unique=True)
    start_date = db.Column(db.Text, nullable=False)
    end_date = db.Column(db.Text, nullable=False)
    location = db.Column(db.Text)

    @classmethod
    def register(cls, name, start_date, end_date, location):
        """Register a league."""

        league = League(
            name=name,
            start_date=start_date,
            end_date=end_date,
            location=location,
        )

        db.session.add(league)
        return league


class TeamLeague(db.Model):
    """Which teams are a part of which leagues."""

    __tablename__ = "teams_leagues"

    team_id = db.Column(db.Integer, db.ForeignKey("teams.id"), primary_key=True)
    league_id = db.Column(db.Integer, db.ForeignKey("leagues.id"), primary_key=True)


class Bowler(db.Model):
    __tablename__ = "bowlers"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.Text, nullable=False)
    last_name = db.Column(db.Text, nullable=False)
    username = db.Column(db.Text, nullable=False, unique=True)
    password = db.Column(db.Text, nullable=False)
    email = db.Column(db.Text, nullable=False, unique=True)
    city = db.Column(db.Text, nullable=False)
    state = db.Column(db.Text, nullable=False)
    image_url = db.Column(
        db.Text,
        default="/static/images/default-pic.jpg",
    )

    scorecards = db.relationship(
        "Scorecard", backref="bowlers", cascade="all, delete-orphan"
    )

    # start_register
    @classmethod
    def register(
        cls, first_name, last_name, username, password, email, city, state, image_url
    ):
        """Register bowler w/hashed password & return bowler."""

        hashed_utf8 = bcrypt.generate_password_hash(password).decode("utf8")

        bowler = Bowler(
            first_name=first_name,
            last_name=last_name,
            username=username,
            password=hashed_utf8,
            email=email,
            city=city,
            state=state,
            image_url=image_url,
        )

        db.session.add(bowler)
        return bowler

    # start_authenticate
    @classmethod
    def authenticate(cls, username, password):
        """Validate that bowler exists & password is correct.

        Return bowler if valid; else return False.
        """

        # searches for the bowler
        bowler = cls.query.filter_by(username=username).first()

        if bowler and bcrypt.check_password_hash(bowler.password, password):
            return bowler
        else:
            return False

    def __repr__(self):
        u = self
        return f"<Bowler id = {u.id}, first_name = {u.first_name}, last_name = {u.last_name}>"


class BowlerTeam(db.Model):
    __tablename__ = "bowlers_teams"

    bowler_id = db.Column(db.Integer, db.ForeignKey("bowlers.id"), primary_key=True)
    team_id = db.Column(db.Integer, db.ForeignKey("teams.id"))


class Team(db.Model):
    __tablename__ = "teams"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text, nullable=False, unique=True)

    leagues = db.relationship("League", secondary="teams_leagues", backref="teams")
    bowlers = db.relationship("Bowler", secondary="bowlers_teams", backref="teams")

    @classmethod
    def register(cls, name):
        """Register a league."""

        team = Team(name=name)

        db.session.add(team)
        return team


class Match(db.Model):
    __tablename__ = "matches"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    league_id = db.Column(db.Integer, db.ForeignKey("leagues.id"))
    date = db.Column(db.Text, nullable=False)
    team_1_id = db.Column(db.Integer, db.ForeignKey("teams.id"))
    team_2_id = db.Column(db.Integer, db.ForeignKey("teams.id"))

    team_1 = db.relationship("Team", foreign_keys=[team_1_id])
    team_2 = db.relationship("Team", foreign_keys=[team_2_id])
    leagues = db.relationship("League", backref="matches")


class Scorecard(db.Model):
    __tablename__ = "scorecards"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date = db.Column(db.Text, nullable=False)
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
    bowler_id = db.Column(db.Integer, db.ForeignKey("bowlers.id"))

    bowler = db.relationship("Bowler", foreign_keys=[bowler_id])
