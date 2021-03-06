from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    PasswordField,
    TextAreaField,
    SelectField,
    DateField,
)
from wtforms.validators import DataRequired, Email, Length
from datetime import date

states = [
    "AL",
    "AK",
    "AZ",
    "AR",
    "CA",
    "CO",
    "CT",
    "DC",
    "DE",
    "FL",
    "GA",
    "HI",
    "ID",
    "IL",
    "IN",
    "IA",
    "KS",
    "KY",
    "LA",
    "ME",
    "MD",
    "MA",
    "MI",
    "MN",
    "MS",
    "MO",
    "MT",
    "NE",
    "NV",
    "NH",
    "NJ",
    "NM",
    "NY",
    "NC",
    "ND",
    "OH",
    "OK",
    "OR",
    "PA",
    "RI",
    "SC",
    "SD",
    "TN",
    "TX",
    "UT",
    "VT",
    "VA",
    "WA",
    "WV",
    "WI",
    "WY",
]


class LoginForm(FlaskForm):
    """Login form."""

    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[Length(min=6)])


class BowlerAddForm(FlaskForm):
    """Form for adding users."""

    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[Length(min=6)])
    first_name = StringField("First Name", validators=[DataRequired()])
    last_name = StringField("Last Name", validators=[DataRequired()])
    email = StringField("E-mail", validators=[DataRequired(), Email()])
    city = StringField("City", validators=[DataRequired()])
    state = SelectField(
        "State", choices=[(st, st) for st in states], validators=[DataRequired()]
    )
    image_url = StringField("(Optional) Image URL")


class BowlerEditForm(FlaskForm):
    """User Edit Form"""

    username = StringField("Username", validators=[DataRequired()])
    first_name = StringField("First Name", validators=[DataRequired()])
    last_name = StringField("Last Name", validators=[DataRequired()])
    email = StringField("E-mail", validators=[DataRequired(), Email()])
    city = StringField("City", validators=[DataRequired()])
    state = SelectField(
        "State", choices=[(st, st) for st in states], validators=[DataRequired()]
    )
    image_url = StringField("(Optional) Image URL")
    bio = TextAreaField("(Optional) Tell us more about yourself")
    password = PasswordField("Password", validators=[Length(min=6)])


class TeamAddEditForm(FlaskForm):
    """Team Add Form"""

    name = StringField(
        "Team Name",
        validators=[DataRequired(message="Please enter the name of your team.")],
    )


class LeagueAddEditForm(FlaskForm):
    """League Add Form"""

    name = StringField(
        "Name",
        validators=[DataRequired(message="Please enter the name of your league.")],
    )
    start_date = DateField(
        "Start date",
        default=date.today(),
        format="%m/%d/%Y",
        validators=[DataRequired(message="Please enter the start date")],
    )
    end_date = DateField(
        "End date",
        validators=[DataRequired(message="Please enter the end date.")],
        format="%m/%d/%Y",
    )

    location = StringField(
        "Location",
        validators=[DataRequired(message="Please enter the location of your league.")],
    )


class NewBowlerForTeamForm(FlaskForm):
    """Form for adding a song to playlist."""

    bowler = SelectField("Bowler To Add", coerce=int)


class NewTeamForLeagueForm(FlaskForm):
    """Form for adding a song to playlist."""

    team = SelectField("Team To Add", coerce=int)


class NewMatchForLeague(FlaskForm):
    """Form for adding a new match to league."""

    date = DateField(
        "Date",
        default=date.today(),
        format="%m/%d/%Y",
        validators=[DataRequired(message="Please enter a date")],
    )

    team_1 = SelectField(
        "Team 1", coerce=int, validators=[DataRequired(message="Please choose a team.")]
    )
    team_2 = SelectField(
        "Team 2", coerce=int, validators=[DataRequired(message="Please choose a team.")]
    )
