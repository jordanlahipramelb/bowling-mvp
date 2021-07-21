from flask import Flask, render_template, redirect, session, flash, g, request
from flask_debugtoolbar import DebugToolbarExtension
from models import (
    connect_db,
    db,
    Bowler,
    Team,
    BowlerTeam,
    League,
    TeamLeague,
    Match,
    Scorecard,
)

from forms import BowlerAddForm, LoginForm, BowlerEditForm
from sqlalchemy.exc import IntegrityError
import os

CURR_BOWLER_KEY = "curr_bowler"

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
    "DATABASE_URL", "postgresql:///bowling_db"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "bowlingrocks")
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = True


connect_db(app)
db.create_all()

# toolbar = DebugToolbarExtension(app)


# ***************************************************
# *********** User Signup/Login/Logout **************
# ***************************************************


@app.before_request
def add_bowler_to_g():
    """If we're logged in, add curr bowler to Flask global."""

    if CURR_BOWLER_KEY in session:
        g.bowler = Bowler.query.get(session[CURR_BOWLER_KEY])

    else:
        g.bowler = None


def do_login(bowler):
    """Log in user."""

    # inserts the CURR_BOWLER_KEY into the session, names it bowler.id
    session[CURR_BOWLER_KEY] = bowler.id
    # import pdb

    # pdb.set_trace()


def do_logout():
    """Logout user."""

    if CURR_BOWLER_KEY in session:
        del session[CURR_BOWLER_KEY]


# *******************************************


@app.route("/register", methods=["GET", "POST"])
def register():
    """Handles bowler registration.

    If the there already is a bowler with that username: flash message
    and re-present form."""

    form = BowlerAddForm()

    if form.validate_on_submit():
        try:
            bowler = Bowler.register(
                username=form.username.data,
                password=form.password.data,
                first_name=form.first_name.data,
                last_name=form.last_name.data,
                email=form.email.data,
                image_url=form.image_url.data or Bowler.image_url.default.arg,
            )
            db.session.commit()

        except IntegrityError:
            flash("Username already taken", "danger")
            return render_template("register.html", form=form)

        do_login(bowler)

        return redirect("/")

    else:
        return render_template("register.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Handles bowler login."""

    form = LoginForm()

    if form.validate_on_submit():
        bowler = Bowler.authenticate(form.username.data, form.password.data)

        if bowler:
            do_login(bowler)
            flash(f"Welcome back, {bowler.first_name}!", "success")

            return redirect("/")

        flash("Invalid username/password.", "danger")

    return render_template("login.html", form=form)


@app.route("/logout", methods=["POST"])
def logout():
    """Handles bowler logout."""

    do_logout()
    flash("Goodbye!", "success")

    return redirect("/login")


# *************************************************************
# *************************************************************
# *************************************************************
@app.route("/scorecard", methods=["GET"])
def display_scorecard():
    """Displays scorecard."""

    return render_template("scorecard.html")


@app.route("/scorecard", methods=["POST"])
def submit_scorecard():
    """Submits scorecard."""

    f1b1 = request.form.get("f1b1", 0)
    f1b2 = request.form.get("f1b2", 0)
    f2b1 = request.form.get("f2b1", 0)
    f2b2 = request.form.get("f2b2", 0)
    f3b1 = request.form.get("f3b1", 0)
    f3b2 = request.form.get("f3b2", 0)
    f4b1 = request.form.get("f4b1", 0)
    f4b2 = request.form.get("f4b2", 0)
    f5b1 = request.form.get("f5b1", 0)
    f5b2 = request.form.get("f5b2", 0)
    f6b1 = request.form.get("f6b1", 0)
    f6b2 = request.form.get("f6b2", 0)
    f7b1 = request.form.get("f7b1", 0)
    f7b2 = request.form.get("f7b2", 0)
    f8b1 = request.form.get("f8b1", 0)
    f8b2 = request.form.get("f8b2", 0)
    f9b1 = request.form.get("f9b1", 0)
    f9b2 = request.form.get("f9b2", 0)
    f10b1 = request.form.get("f10b1", 0)
    f10b2 = request.form.get("f10b2", 0)
    f10b3 = request.form.get("f10b3", 0)

    f1_score = request.form.get("f1-score", 0)
    f2_score = request.form.get("f2-score", 0)
    f3_score = request.form.get("f3-score", 0)
    f4_score = request.form.get("f4-score", 0)
    f5_score = request.form.get("f5-score", 0)
    f6_score = request.form.get("f6-score", 0)
    f7_score = request.form.get("f7-score", 0)
    f8_score = request.form.get("f8-score", 0)
    f9_score = request.form.get("f9-score", 0)
    f10_score = request.form.get("f10-score", 0)

    total_score = request.form.get("total-score", 0)

    new_scorecard = Scorecard(
        frame1_1_pins=f1b1,
        frame1_2_pins=f1b2,
        frame1_score=f1_score,
        frame2_1_pins=f2b1,
        frame2_2_pins=f2b2,
        frame2_score=f2_score,
        frame3_1_pins=f3b1,
        frame3_2_pins=f3b2,
        frame3_score=f3_score,
        frame4_1_pins=f4b1,
        frame4_2_pins=f4b2,
        frame4_score=f4_score,
        frame5_1_pins=f5b1,
        frame5_2_pins=f5b2,
        frame5_score=f5_score,
        frame6_1_pins=f6b1,
        frame6_2_pins=f6b2,
        frame6_score=f6_score,
        frame7_1_pins=f7b1,
        frame7_2_pins=f7b2,
        frame7_score=f7_score,
        frame8_1_pins=f8b1,
        frame8_2_pins=f8b2,
        frame8_score=f8_score,
        frame9_1_pins=f9b1,
        frame9_2_pins=f9b2,
        frame9_score=f9_score,
        frame10_1_pins=f10b1,
        frame10_2_pins=f10b2,
        frame10_3_pins=f10b3,
        frame10_score=f1_score,
        total_score=total_score,
    )

    db.session.add(new_scorecard)
    db.session.commit()

    return redirect("/scorecards")
