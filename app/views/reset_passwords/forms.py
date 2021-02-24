from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField
from wtforms.validators import DataRequired, Email, EqualTo, Length


class RequestResetPassForm(FlaskForm):
    email = StringField("Email address", validators=[DataRequired(), Email()])


class ResetPassForm(FlaskForm):
    password = PasswordField(
        label="Password",
        validators=[
            Length(min=6, max=10),
            EqualTo("password_confirm", message="Passwords must match"),
        ],
    )
    password_confirm = PasswordField(
        label="Password confirm", validators=[Length(min=6, max=10)]
    )
