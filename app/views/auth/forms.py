from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField
from wtforms.validators import DataRequired


class SelectOrganizationForm(FlaskForm):
    username = StringField("Organization Username", validators=[DataRequired()])


class MemberLoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
