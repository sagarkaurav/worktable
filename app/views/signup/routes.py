from app import db, mail
from app.models import MemberInvite, Organization
from flask import Blueprint, flash, render_template, url_for
from flask_mail import Message

from .forms import SignupForm

signup = Blueprint("signup", __name__, template_folder="templates")


@signup.route("/", methods=["GET", "POST"])
def index():
    form = SignupForm()
    if form.validate_on_submit():
        org = Organization(
            name=form.organization_name.data,
            username=form.organization_username.data.lower(),
        )
        new_invite = MemberInvite(email=form.admin_email.data.lower(), organization=org)
        db.session.add(org)
        db.session.add(new_invite)
        db.session.commit()
        invite_link = url_for(
            "members.join",
            org_username=org.username,
            token=new_invite.token,
            _external=True,
        )
        msg = Message(
            "Worktable organization join invite",
            sender="no-reply@example.com",
            recipients=[new_invite.email],
        )
        msg.body = render_template(
            "members/invite_mail.txt",
            join_link=invite_link,
            org_name=org.name,
        )
        msg.html = render_template(
            "members/invite_mail.html",
            join_link=invite_link,
            org_name=org.name,
        )
        mail.send(msg)
        flash("Confirmation link has been sent to admin email address")
    return render_template("signup/index.html", form=form)
