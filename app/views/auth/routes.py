from app.models import Member, Organization
from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_user, logout_user

from .forms import MemberLoginForm, SelectOrganizationForm

auth = Blueprint("auth", __name__, template_folder="templates")


@auth.route("/login/", methods=["GET"])
@auth.route("/login/", subdomain="<org_username>", methods=["GET", "POST"])
def login(org_username=None):
    org = Organization.query.filter_by(username=org_username).first()
    if org is None and request.method == "POST":
        flash("organization not found", "error")
        return redirect(url_for("auth.select"))
    if org is None and request.method == "GET":
        return redirect(url_for("auth.select"))

    member_login_form = MemberLoginForm()
    if member_login_form.validate_on_submit():
        email = member_login_form.email.data
        password = member_login_form.password.data
        member = Member.query.filter_by(email=email, organization=org).first()
        if member is None:
            flash("Account not found")
        elif not member.verify_password(password):
            flash("username or password is invalid")
        else:
            login_user(member)
            flash("login successfully")
            return redirect(url_for("dashboard.index", org_username=org_username))
    return render_template(
        "auth/login.html", form=member_login_form, org_username=org_username
    )


@auth.route("/select/", methods=["GET", "POST"])
def select():
    select_org_form = SelectOrganizationForm()
    if select_org_form.validate_on_submit():
        org = Organization.query.filter_by(
            username=select_org_form.username.data
        ).first()
        if org is None:
            flash("Organization not found")
        else:
            return redirect(url_for("auth.login", org_username=org.username))

    return render_template("auth/select_org.html", form=select_org_form)


@auth.route("/logout/", subdomain="<org_username>")
def logout(org_username):
    if current_user.is_authenticated:
        flash("Logged out successfully")
        org_username = current_user.organization.username
        logout_user()
        return redirect(url_for("auth.login", org_username=org_username))
    else:
        flash("You are not logged in")
        return redirect(url_for("auth.select"))
