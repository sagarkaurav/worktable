from flask_wtf import FlaskForm
from wtforms import HiddenField, SelectMultipleField, StringField
from wtforms.validators import DataRequired, Length


class CreateProject(FlaskForm):
    name = StringField(
        "New Project name", validators=[DataRequired(), Length(min=3, max=255)]
    )
    description = HiddenField("Project description", validators=[DataRequired()])


class EditProject(FlaskForm):
    name = StringField(
        "Project name", validators=[DataRequired(), Length(min=3, max=255)]
    )
    description = HiddenField("Project description", validators=[DataRequired()])


class CreateComment(FlaskForm):
    description = HiddenField("New comment", validators=[DataRequired()])


class EditComment(FlaskForm):
    description = HiddenField("New comment", validators=[DataRequired()])


class AddMemberForm(FlaskForm):
    members = SelectMultipleField("Add members", coerce=int, choices=[])
