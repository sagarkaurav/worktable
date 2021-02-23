import datetime

from app import db
from app.models import Member, MemberInvite
from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user

from .forms import MemberInviteForm, MemberJoinForm

members = Blueprint("members", __name__, template_folder="templates")


@members.route("/", subdomain="<org_username>")
@login_required
def index(org_username):
    member_page = request.args.get("member_page", 1)
    members = Member.query.filter_by(organization=current_user.organization).paginate(
        int(member_page), 5
    )
    return render_template("members/index.html", members=members)


@members.route("/invite/", subdomain="<org_username>", methods=["GET", "POST"])
@login_required
def invite(org_username):
    member_invite = MemberInviteForm()
    if member_invite.validate_on_submit():
        email = member_invite.email.data.lower()
        member = Member.query.filter_by(
            email=email, organization=current_user.organization
        ).first()
        if member:
            flash("Email is alreay a member", "error")
        new_invite = MemberInvite(email=email, organization=current_user.organization)
        db.session.add(new_invite)
        db.session.commit()
        flash("New member invite has been sent", "success")
        return redirect(
            url_for("members.index", org_username=current_user.organization.username)
        )
    return render_template("members/invite.html", form=member_invite)


@members.route("/join/<token>", subdomain="<org_username>", methods=["GET", "POST"])
def join(org_username, token):
    invite = MemberInvite.query.filter_by(token=token).first()
    if not invite:
        flash("Invalid invite link", "error")
        return redirect(
            url_for(
                "members.join", token=token, org_username=invite.organization.username
            )
        )
    member_join = MemberJoinForm()
    if member_join.validate_on_submit():
        new_member = Member(
            first_name=member_join.first_name.data,
            last_name=member_join.last_name.data,
            email=invite.email,
            organization=invite.organization,
        )
        new_member.password = member_join.password.data
        db.session.add(new_member)
        db.session.commit()
        db.session.delete(invite)
        login_user(new_member)
        flash("New member invite has been sent", "success")
        return redirect(
            url_for("dashboard.index", org_username=invite.organization.username)
        )
    return render_template(
        "members/join.html", invite=invite, form=member_join, token=token
    )


@members.route("/disable/", subdomain="<org_username>", methods=["POST"])
@login_required
def disable_account(org_username):
    member_id = request.form.get("member_id")
    member = Member.query.filter_by(
        id=member_id, organization=current_user.organization
    ).first()
    if member is None:
        flash("Member account is not found", "error")
    elif member.disabled_at:
        flash("Member account is already disabled", "error")
    elif member == current_user:
        flash("You can not disabled your own account", "error")
    else:
        member.disabled_at = datetime.datetime.utcnow()
        db.session.commit()
        flash("Member account has been disabled", "success")
    redirect_url = url_for(".index", org_username=current_user.organization.username)
    return redirect(redirect_url)


@members.route("/enable/", subdomain="<org_username>", methods=["POST"])
@login_required
def enable_account(org_username):
    member_id = request.form.get("member_id")
    member = Member.query.filter_by(
        id=member_id, organization=current_user.organization
    ).first()
    if member is None:
        flash("Member account is not found", "error")
    elif member.disabled_at is None:
        flash("Member account is already enabled", "error")
    elif member == current_user:
        flash("You can not enable your own account", "error")
    else:
        member.disabled_at = None
        db.session.commit()
        flash("Member account has been enabled", "success")
    redirect_url = url_for(".index", org_username=current_user.organization.username)
    return redirect(redirect_url)
