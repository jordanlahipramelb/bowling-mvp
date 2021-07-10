from flask import Flask, render_template, redirect, session, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import connect_db, db
from sqlalchemy.exc import IntegrityError
import os

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "postgresql:///bowling_scorecard_db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "bowlingrocks")
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False


connect_db(app)
db.drop_all()
db.create_all()

toolbar = DebugToolbarExtension(app)


@app.route("/scorecard")
def show_scorecard():
    """Displays scorecard."""

    return render_template("scorecard.html")