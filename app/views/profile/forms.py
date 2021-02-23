from flask_wtf import FlaskForm
from wtforms import PasswordField
from wtforms.validators import EqualTo, Length


class ChangePasswordForm(FlaskForm):
    password_confirm = PasswordField(
        label="Password confirm", validators=[Length(min=6, max=10)]
    )
    password = PasswordField(
        label="New Password",
        validators=[
            Length(min=6, max=10),
            EqualTo("password_confirm", message="Passwords must match"),
        ],
    )
    password_confirm = PasswordField(
        label="Password confirm", validators=[Length(min=6, max=10)]
    )
