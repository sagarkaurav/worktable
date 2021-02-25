import datetime

from app import db, mail
from app.models import Member, MemberInvite
from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user
from flask_mail import Message

from .forms import MemberInviteForm, MemberJoinForm

members = Blueprint("members", __name__, template_folder="templates")


@members.route("/", subdomain="<org_username>")
@login_required
def index(org_username):
    member_page = request.args.get("member_page", 1)
    members = Member.query.filter_by(organization=current_user.organization).paginate(
        int(member_page), 5
    )
    all_invites = MemberInvite.query.filter_by(
        organization=current_user.organization
    ).all()
    return render_template(
        "members/index.html", all_invites=all_invites, members=members
    )


@members.route(
    "/invite/<invite_id>/remove", subdomain="<org_username>", methods=["POST"]
)
@login_required
def remove_invite(org_username, invite_id):
    invite = MemberInvite.query.filter_by(
        organization=current_user.organization, id=invite_id
    ).first()
    if invite is None:
        flash("Unable to find invite to remove", "error")
    else:
        db.session.delete(invite)
        db.session.commit()
        flash("Invite removed successfully", "success")
    return redirect(
        url_for(
            "members.index",
            org_username=current_user.organization.username,
        )
    )


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
            flash("Email is already a member", "error")
            return redirect(
                url_for(
                    "members.index",
                    org_username=current_user.organization.username,
                )
            )
        invite = MemberInvite.query.filter_by(
            organization=current_user.organization, email=email
        ).first()
        if invite:
            flash("Invite already sent.", "warning")
            return redirect(
                url_for(
                    "members.index",
                    org_username=current_user.organization.username,
                )
            )

        new_invite = MemberInvite(email=email, organization=current_user.organization)
        db.session.add(new_invite)
        db.session.commit()
        invite_link = url_for(
            ".join",
            org_username=current_user.organization.username,
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
            org_name=current_user.organization.name,
        )
        msg.html = render_template(
            "members/invite_mail.html",
            join_link=invite_link,
            org_name=current_user.organization.name,
        )
        mail.send(msg)

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
        return redirect(url_for("auth.login", org_username=org_username))
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
        db.session.delete(invite)
        db.session.commit()
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
