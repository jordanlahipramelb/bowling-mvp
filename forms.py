from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField
from wtforms.validators import DataRequired, Email, Length, Optional

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


class LoginForm(FlaskForm):
    """Login form."""

    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[Length(min=6)])


class BowlerEditForm(FlaskForm):
    """User Edit Form"""

    username = StringField("Username", validators=[DataRequired()])
    first_name = StringField("First Name", validators=[DataRequired()])
    last_name = StringField("Last Name", validators=[DataRequired()])
    email = StringField("E-mail", validators=[DataRequired(), Email()])
    image_url = StringField("(Optional) Image URL")
    password = PasswordField("Password", validators=[Length(min=6)])
