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

    # start_register
    @classmethod
    def register(cls, first_name, last_name, username, pwd, email, image_url):
        """Register user w/hashed password & return user."""

        hashed_utf8 = bcrypt.generate_password_hash(pwd).decode("utf8")

        bowler = Bowler(
            first_name=first_name,
            last_name=last_name,
            username=username,
            pwd=hashed_utf8,
            email=email,
            image_url=image_url
        )

        db.session.add(bowler)
        return bowler

    # start_authenticate
    @classmethod
    def authenticate(cls, username, pwd):
        """Validate that user exists & password is correct.

        Return user if valid; else return False.
        """

        # searches for the user
        bowler = cls.query.filter_by(username=username).first()

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
    date = db.Column(db.DateTime, nullable=False,
                     default=datetime.datetime.now)
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
