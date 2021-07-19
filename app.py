from flask import Flask, render_template, redirect, session, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import connect_db, db, Scorecard
from sqlalchemy.exc import IntegrityError
import os

CURR_BOWLER_KEY = "curr_bowler"

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
    "DATABASE_URL", "postgresql:///bowling_db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "bowlingrocks")
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False


connect_db(app)
db.create_all()

toolbar = DebugToolbarExtension(app)


# ***************************************************
# *********** User Signup/Login/Logout **************
# ***************************************************

@app.before_request
def add_user_to_g():
    """If we're logged in, add curr bowler to Flask global."""

    if CURR_BOWLER_KEY in session:
        g.user = Bowler.query.get(session[CURR_BOWLER_KEY])

    else:
        g.user = None


def do_login(user):
    """Log in user."""

    # inserts the CURR_BOWLER_KEY into the session, names it user.id
    session[CURR_BOWLER_KEY] = user.id
    # import pdb

    # pdb.set_trace()


def do_logout():
    """Logout user."""

    if CURR_BOWLER_KEY in session:
        del session[CURR_BOWLER_KEY]


@app.route("/scorecard")
def show_scorecard():
    """Displays scorecard."""

    f1b1 = request.form["f1b1"]
    f1b2 = request.form["f1b2"]
    f2b1 = request.form["f2b1"]
    f2b2 = request.form["f2b2"]
    f3b1 = request.form["f3b1"]
    f3b2 = request.form["f3b2"]
    f4b1 = request.form["f4b1"]
    f4b2 = request.form["f4b2"]
    f5b1 = request.form["f5b1"]
    f5b2 = request.form["f5b2"]
    f6b1 = request.form["f6b1"]
    f6b2 = request.form["f6b2"]
    f7b1 = request.form["f7b1"]
    f7b2 = request.form["f7b2"]
    f8b1 = request.form["f8b1"]
    f8b2 = request.form["f8b2"]
    f9b1 = request.form["f9b1"]
    f9b2 = request.form["f9b2"]
    f10b1 = request.form["f10b1"]
    f10b2 = request.form["f10b2"]
    f10b3 = request.form["f10b3"]

    f1_score = request.form["f1-score"]
    f2_score = request.form["f2-score"]
    f3_score = request.form["f3-score"]
    f4_score = request.form["f4-score"]
    f5_score = request.form["f5-score"]
    f6_score = request.form["f6-score"]
    f7_score = request.form["f7-score"]
    f8_score = request.form["f8-score"]
    f9_score = request.form["f9-score"]
    f10_score = request.form["f10-score"]

    total_score = request.form["total-score"]

    new_scorecard = Scorecard(
        frame1_1_pins=f1b1, frame1_2_pins=f1b2, frame1_score=f1_score, frame2_1_pins=f2b1, frame2_2_pins=f2b2, frame2_score=f2_score, frame3_1_pins=f3b1, frame3_2_pins=f3b2, frame3_score=f3_score, frame4_1_pins=f4b1, frame4_2_pins=f4b2, frame4_score=f4_score, frame5_1_pins=f5b1, frame5_2_pins=f5b2, frame5_score=f5_score, frame6_1_pins=f6b1, frame6_2_pins=f6b2, frame6_score=f6_score, frame7_1_pins=f7b1, frame7_2_pins=f7b2, frame7_score=f7_score, frame8_1_pins=f8b1, frame8_2_pins=f8b2, frame8_score=f8_score, frame9_1_pins=f9b1, frame9_2_pins=f9b2, frame9_score=f9_score, frame10_1_pins=f10b1, frame10_2_pins=f10b2, frame10_3_pins=f10b3, frame10_score=f1_score, total_score=total_score)

    return render_template("scorecard.html")
