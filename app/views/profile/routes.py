from app import db
from flask import Blueprint, flash, redirect, render_template, url_for
from flask_login import current_user, login_required

from .forms import ChangePasswordForm

profile = Blueprint("profile", __name__, template_folder="templates")


@profile.route("/", subdomain="<org_username>", methods=["GET"])
@login_required
def index(org_username):
    change_pass_form = ChangePasswordForm()
    return render_template("profile/index.html", change_pass_form=change_pass_form)


@profile.route("/change-password", subdomain="<org_username>", methods=["POST"])
@login_required
def change_password(org_username):
    change_pass_form = ChangePasswordForm()
    if change_pass_form.validate_on_submit():
        current_user.password = change_pass_form.password.data
        db.session.commit()
        flash("Your password has been changed", "success")
        return redirect(
            url_for(".index", org_username=current_user.organization.username)
        )
    return render_template("profile/index.html", change_pass_form=change_pass_form)
