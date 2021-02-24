from app import db, mail
from app.models import Member, Organization
from flask import Blueprint, abort, flash, redirect, render_template, url_for
from flask_mail import Message

from .forms import RequestResetPassForm, ResetPassForm

resetpass = Blueprint("resetpass", __name__, template_folder="templates")


@resetpass.route("/", subdomain="<org_username>", methods=["GET", "POST"])
def index(org_username):
    org = Organization.query.filter_by(username=org_username).first()
    if org is None:
        abort(404)
    request_reset_pass_form = RequestResetPassForm()
    if request_reset_pass_form.validate_on_submit():
        email = request_reset_pass_form.email.data
        member = Member.query.filter_by(organization=org, email=email).first()
        if member is None:
            flash("Member account not found in selected organization", "error")
            return redirect(url_for(".index", org_username=org.username))
        token = member.create_reset_password_token()
        db.session.commit()
        reset_link = url_for(
            ".reset", org_username=org.username, token=token, _external=True
        )
        msg = Message(
            "Worktable reset password link",
            sender="no-reply@example.com",
            recipients=[member.email],
        )
        msg.body = render_template(
            "reset_passwords/reset_password_mail.txt", link=reset_link
        )
        msg.html = render_template(
            "reset_passwords/reset_password_mail.html", link=reset_link
        )
        mail.send(msg)
        flash(
            "Reset password instructions has been sent to your email address", "success"
        )

        return redirect(url_for("auth.login", org_username=org.username))

    return render_template(
        "reset_passwords/index.html", org=org, form=request_reset_pass_form
    )


@resetpass.route("/<token>/", subdomain="<org_username>", methods=["GET", "POST"])
def reset(org_username, token):
    org = Organization.query.filter_by(username=org_username).first()
    if org is None:
        abort(404)
    member = Member.query.filter_by(
        reset_password_token=token, organization=org
    ).first()
    if member is None:
        abort(404)

    if not member.is_reset_token_valid(token):
        flash("Reset password link is invalid or expired", "error")
        return redirect(url_for("auth.login", org_username=org.username))

    reset_pass_form = ResetPassForm()
    if reset_pass_form.validate_on_submit():
        member.password = reset_pass_form.password.data
        member.remove_reset_token()
        db.session.commit()
        flash("Your password has been reseted", "success")
        return redirect(url_for("auth.login", org_username=org.username))

    return render_template(
        "reset_passwords/reset_pass.html", token=token, org=org, form=reset_pass_form
    )
