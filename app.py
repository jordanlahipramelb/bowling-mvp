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

from forms import (
    BowlerAddForm,
    LoginForm,
    BowlerEditForm,
    TeamAddEditForm,
    LeagueAddEditForm,
    NewTeamForLeagueForm,
    NewBowlerForTeamForm,
    NewMatchForLeague,
)
from sqlalchemy.exc import IntegrityError
import os
import re

CURR_BOWLER_KEY = "curr_bowler"

app = Flask(__name__)


uri = os.environ.get("DATABASE_URL", "postgresql:///bowling_db")
if uri.startswith("postgres://"):
    uri = uri.replace("postgres://", "postgresql://", 1)
    # rest of connection code using the connection string `uri`

app.config["SQLALCHEMY_DATABASE_URI"] = uri
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "bowlingrocks")
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False


connect_db(app)


toolbar = DebugToolbarExtension(app)


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


@app.route("/")
def homepage():
    """Welcome Page."""

    return render_template("welcome.html")


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
                city=form.city.data,
                state=form.state.data,
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


@app.route("/logout")
def logout():
    """Handles bowler logout."""

    do_logout()
    flash("Goodbye!", "success")

    return redirect("/login")


# *******************************************
# ***** Bowler/User related routes **********
# *******************************************


@app.route("/bowlers")
def list_bowlers():
    """Show list of all bowlers."""

    bowlers = Bowler.query.all()

    return render_template("all_bowlers.html", bowlers=bowlers)


@app.route("/bowlers/<int:bowler_id>")
def show_bowler_profile(bowler_id):
    """Show bowler profile."""

    bowler = Bowler.query.get_or_404(bowler_id)

    scorecards = Scorecard.query.all()

    bowler_team = BowlerTeam.query.filter(BowlerTeam.bowler_id == bowler_id).first()

    if bowler_team is None:
        team_id = 0

    else:
        team_id = bowler_team.team_id

    team = Team.query.get(team_id)

    return render_template(
        "profile.html", bowler=bowler, scorecards=scorecards, team=team
    )


@app.route("/bowlers/<int:bowler_id>/edit", methods=["GET", "POST"])
def update_bowler_profile(bowler_id):
    """Update current bowler profile."""

    if not g.bowler:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    bowler = g.bowler
    form = BowlerEditForm(obj=bowler)

    if form.validate_on_submit():
        if Bowler.authenticate(bowler.username, form.password.data):
            bowler.username = form.username.data
            bowler.first_name = form.first_name.data
            bowler.last_name = form.last_name.data
            bowler.email = form.email.data
            bowler.city = form.city.data
            bowler.state = form.state.data
            bowler.image_url = form.image_url.data or "/static/images/default-pic.jpg"

            db.session.commit()

            return redirect(f"/bowlers/{bowler.id}")

        flash("Invalid password! Try again.", "danger")

    return render_template("profile_edit.html", form=form)


@app.route("/bowlers/delete", methods=["POST"])
def delete_bowler():
    """Delete bowler."""

    if not g.bowler:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    do_logout()
    flash("Bowler Deleted", "danger")
    db.session.delete(g.bowler)
    db.session.commit()

    return redirect("/")


# ****************************************************
# ************** Scorecard Related *******************
# ****************************************************


@app.route("/scorecards")
def show_all_scorecards():
    """Display all scorecards."""

    scorecards = Scorecard.query.all()

    return render_template("scorecards.html", scorecards=scorecards)


@app.route("/scorecards/<int:bowler_id>/new", methods=["GET"])
def display_new_scorecard(bowler_id):
    """Displays scorecard."""

    if not g.bowler:
        flash(
            "Access unauthorized. Please login/register to track your game.", "danger"
        )
        return redirect("/")

    scorecards = Scorecard.query.all()

    return render_template("scorecard_new.html")


@app.route("/scorecards/<int:bowler_id>/new", methods=["POST"])
def submit_scorecard(bowler_id):
    """Submits scorecard."""

    if not g.bowler:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    date = request.form["date"]
    location = request.form["location"]
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
        date=date,
        location=location,
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
        frame10_score=f10_score,
        total_score=total_score,
        bowler_id=g.bowler.id,
    )

    db.session.add(new_scorecard)
    db.session.commit()

    return redirect(f"/bowlers/{g.bowler.id}")


@app.route("/scorecards/<int:scorecard_id>")
def show_scorecard(scorecard_id):
    """Displays a scorecard."""
    scorecard = Scorecard.query.get_or_404(scorecard_id)

    return render_template("scorecard_details.html", scorecard=scorecard)


@app.route("/scorecards/<int:scorecard_id>/delete", methods=["POST"])
def delete_scorecard(scorecard_id):
    """Delete a scorecard."""

    if not g.bowler:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    scorecard = Scorecard.query.get(scorecard_id)

    db.session.delete(scorecard)
    db.session.commit()
    flash("Scorecard deleted.", "danger")
    return redirect(f"/bowlers/{g.bowler.id}")


# ****************************************************
# ************** Team Related *******************
# ****************************************************


@app.route("/teams")
def list_teams():
    """Display all teams."""

    teams = Team.query.all()

    return render_template("teams.html", teams=teams)


@app.route("/teams/add", methods=["GET", "POST"])
def create_team():
    """Create a new team."""

    if not g.bowler:
        flash("Access unauthorized. Please login to add a new team.", "danger")
        return redirect("/teams")

    form = TeamAddEditForm()

    if form.validate_on_submit():
        try:
            team = Team.register(
                name=form.name.data,
            )

            db.session.commit()

        except IntegrityError:
            flash("Name already taken", "danger")
            return render_template("teams_register.html", form=form)

        flash("Team Created!", "success")
        return redirect("/teams")

    return render_template("teams_register.html", form=form)


@app.route("/teams/<int:team_id>")
def show_teammates(team_id):
    """Show names of bowlers on a team."""

    team = Team.query.get_or_404(team_id)
    bowlers = Bowler.query.all()

    return render_template("team_teammates.html", team=team, bowlers=bowlers)


@app.route("/teams/<int:team_id>/add-bowler", methods=["GET", "POST"])
def add_bowler_to_team(team_id):
    """Add bowler to a team."""

    if not g.bowler:
        flash("Access unauthorized. Please login to add a new bowler.", "danger")
        return redirect("/")

    team = Team.query.get_or_404(team_id)
    form = NewBowlerForTeamForm()

    curr_on_team = [bowler.id for bowler in team.bowlers]
    form.bowler.choices = (
        db.session.query(Bowler.id, Bowler.first_name + " " + Bowler.last_name)
        .filter(Bowler.id.notin_(curr_on_team))
        .all()
    )

    if form.validate_on_submit():

        bowler_team = BowlerTeam(bowler_id=form.bowler.data, team_id=team_id)
        db.session.add(bowler_team)
        db.session.commit()

        return redirect(f"/teams/{team_id}")

    return render_template("add_bowler_to_team.html", team=team, form=form)


# ****************************************************
# ************** League Related *******************
# ****************************************************


@app.route("/leagues")
def list_leagues():
    """Display all leagues."""

    leagues = League.query.all()

    return render_template("leagues.html", leagues=leagues)


@app.route("/leagues/<int:league_id>")
def show_teams_in_league(league_id):
    """Show names of teams in a league."""

    league = League.query.get_or_404(league_id)

    return render_template("league_teams.html", league=league)


@app.route("/leagues/add", methods=["GET", "POST"])
def create_league():
    """Create a new league."""

    if not g.bowler:
        flash("Access unauthorized. Please login to create a new league.", "danger")
        return redirect("/leagues")

    form = LeagueAddEditForm()

    if form.validate_on_submit():
        try:
            league = League.register(
                name=form.name.data,
                start_date=form.start_date.data,
                end_date=form.end_date.data,
                location=form.location.data,
            )

            db.session.commit()

        except IntegrityError:
            flash("Name already taken", "danger")
            return render_template("leagues_register.html", form=form)

        flash("League Created!", "success")
        return redirect("/leagues")

    return render_template("league_register.html", form=form)


@app.route("/leagues/<int:league_id>/add-team", methods=["GET", "POST"])
def add_team_to_league(league_id):
    """Add team to a league."""

    if not g.bowler:
        flash("Access unauthorized. Please login to create a new league.", "danger")
        return redirect("/")

    league = League.query.get_or_404(league_id)
    form = NewTeamForLeagueForm()

    curr_on_league = [team.id for team in league.teams]
    form.team.choices = (
        db.session.query(Team.id, Team.name)
        .filter(Team.id.notin_(curr_on_league))
        .all()
    )

    if form.validate_on_submit():

        team_league = TeamLeague(team_id=form.team.data, league_id=league_id)
        db.session.add(team_league)
        db.session.commit()

        return redirect(f"/leagues/{league_id}")

    return render_template("add_team_to_league.html", league=league, form=form)


@app.route("/leagues/<int:league_id>/add-match", methods=["GET", "POST"])
def add_match(league_id):

    league = League.query.get_or_404(league_id)
    form = NewMatchForLeague()

    curr_on_league = [team.id for team in league.teams]
    form.team_1.choices = (
        db.session.query(Team.id, Team.name)
        .filter(Team.id.notin_(curr_on_league))
        .all()
    )
    form.team_2.choices = (
        db.session.query(Team.id, Team.name)
        .filter(Team.id.notin_(curr_on_league))
        .all()
    )

    if form.validate_on_submit():

        match = Match(
            date=form.date.data,
            team_1_id=form.team_1.data,
            team_2_id=form.team_2.data,
            league_id=league_id,
        )

        db.session.add(match)
        db.session.commit()

        return redirect(f"/leagues/{league_id}")

    return render_template("match_add.html", league=league, form=form)


# ****************************************************
# ************** Location Related *******************
# ****************************************************


@app.route("/locate")
def show_location_page():
    """Displays location page."""

    return render_template("locate.html")
