from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField
from wtforms.validators import DataRequired, Email, EqualTo, Length


class MemberInviteForm(FlaskForm):
    email = StringField("Email address", validators=[DataRequired(), Email()])


class MemberJoinForm(FlaskForm):
    first_name = StringField("First Name", validators=[DataRequired()])
    last_name = StringField("Last Name", validators=[DataRequired()])
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
