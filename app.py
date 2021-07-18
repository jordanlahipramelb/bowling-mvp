from flask import Flask, render_template, redirect, session, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import connect_db, db
from sqlalchemy.exc import IntegrityError
import os

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "postgresql:///bowling_db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "bowlingrocks")
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False


connect_db(app)
db.create_all()

toolbar = DebugToolbarExtension(app)


@app.route("/scorecard")
def show_scorecard():
    """Displays scorecard."""

    frame_1 = request.form["f1"]
    frame_2 = request.form["f2"]
    frame_3 = request.form["f3"]
    frame_4 = request.form["f4"]
    frame_5 = request.form["f5"]
    frame_6 = request.form["f6"]
    frame_7 = request.form["f7"]
    frame_8 = request.form["f8"]
    frame_9 = request.form["f9"]
    frame_10 = request.form["f10"]

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

    return render_template("scorecard.html")
