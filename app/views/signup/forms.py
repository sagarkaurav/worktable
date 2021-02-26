from app.models import Organization
from flask_wtf import FlaskForm
from usernames import is_safe_username
from wtforms import StringField, ValidationError
from wtforms.validators import DataRequired, Email, Length


class SignupForm(FlaskForm):
    organization_name = StringField(
        "Organization name", validators=[DataRequired(), Length(min=3, max=255)]
    )
    organization_username = StringField(
        "Organization username", validators=[DataRequired(), Length(min=4, max=255)]
    )
    admin_email = StringField("Admin Email", validators=[DataRequired(), Email()])

    def validate_organization_username(form, field):
        username = field.data.lower()
        if not is_safe_username(username):
            raise ValidationError("Username must only contain _, A-Z, a-z characters.")
        org = Organization.query.filter_by(username=username).first()
        if org:
            raise ValidationError("Username already in use.")
