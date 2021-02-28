from app import db
from app.models import Member, MemberProject, Project
from flask import Blueprint, abort, flash, redirect, render_template, url_for
from flask_login import current_user, login_required

from .forms import AddMemberForm, CreateComment, CreateProject, EditComment, EditProject

projects = Blueprint(
    "projects", __name__, subdomain="<org_username>", template_folder="templates"
)


@projects.route("/create/", methods=["GET", "POST"])
@login_required
def create(org_username):
    new_project = CreateProject()
    if new_project.validate_on_submit():
        project = Project(
            name=new_project.name.data,
            description=new_project.description.data,
            created_by_id=current_user.id,
        )
        permission = MemberProject(member=current_user)
        project.permissions.append(permission)
        db.session.add(project)
        db.session.commit()
        return redirect(
            url_for(".detail", project_id=project.public_id, org_username=org_username)
        )
    return render_template("projects/create.html", form=new_project)


@projects.route("/<project_id>/edit/", methods=["GET", "POST"])
@login_required
def edit(org_username, project_id):
    project = (
        Project.query.filter(Project.members.any(id=current_user.id))
        .filter_by(public_id=project_id, project_id=None)
        .first()
    )
    if project is None:
        abort(404)
    edit_project_form = EditProject(name=project.name, description=project.description)
    if edit_project_form.validate_on_submit():
        project.name = edit_project_form.name.data
        project.description = edit_project_form.description.data
        project.last_updated_by_id = current_user.id
        db.session.commit()
        flash("Project has been edited successfully", "success")
        return redirect(
            url_for(".detail", project_id=project.public_id, org_username=org_username)
        )
    return render_template(
        "projects/edit.html", project=project, form=edit_project_form
    )


@projects.route("/<project_id>/", methods=["GET", "POST"])
@login_required
def detail(org_username, project_id):
    project = (
        Project.query.filter(Project.members.any(id=current_user.id))
        .filter_by(public_id=project_id, project_id=None)
        .first()
    )
    if project is None:
        abort(404)
    new_comment = CreateComment()
    add_members_form = AddMemberForm()
    for member in current_user.organization.members:
        if member not in project.members:
            add_members_form.members.choices.append((member.id, member.email))
    if new_comment.validate_on_submit():
        comment = Project(
            description=new_comment.description.data,
            project=project,
            created_by_id=current_user.id,
        )
        permission = MemberProject(member=current_user)
        comment.permissions.append(permission)
        db.session.add(comment)
        db.session.commit()
        return redirect(
            url_for(
                ".detail",
                org_username=org_username,
                project_id=project_id,
            )
        )
    return render_template(
        "projects/detail.html",
        add_members_form=add_members_form,
        project=project,
        form=new_comment,
    )


@projects.route("/<project_id>/comments/<comment_id>/edit/", methods=["GET", "POST"])
@login_required
def edit_comment(org_username, project_id, comment_id):
    project = (
        Project.query.filter(Project.members.any(id=current_user.id))
        .filter_by(public_id=project_id, project_id=None)
        .first()
    )
    if project is None:
        abort(404)
    comment = (
        Project.query.filter(Project.members.any(id=current_user.id))
        .filter_by(public_id=comment_id, project_id=project.id)
        .first()
    )
    if comment is None:
        flash("Comment not found", "error")
        return redirect(
            url_for(
                "projects.detail",
                org_username=current_user.organization.username,
                project_id=project.public_id,
            )
        )
    edit_comment = EditComment(description=comment.description)
    if edit_comment.validate_on_submit():
        comment.description = edit_comment.description.data
        db.session.commit()
        flash("Your comment has been edited")
        return redirect(
            url_for(".detail", org_username=org_username, project_id=project_id)
        )
    return render_template(
        "projects/edit_comment.html",
        project=project,
        edit_comment=comment,
        form=edit_comment,
    )


@projects.route("/<project_id>/members/<member_id>/remove/", methods=["POST"])
@login_required
def member_remove(org_username, project_id, member_id):
    project = (
        Project.query.filter(Project.members.any(id=current_user.id))
        .filter_by(public_id=project_id, project_id=None)
        .first()
    )
    if project is None:
        abort(404)
    member = Member.query.get(member_id)
    if member not in project.members:
        flash("Member is not part of this project", "error")
    elif member == current_user:
        flash("You can not remove yourself from the project", "error")
    else:
        project.members.remove(member)
        db.session.commit()
        flash("Member has been remove from the project", "success")
    return redirect(
        url_for(
            ".detail",
            project_id=project.public_id,
            org_username=current_user.organization.username,
        )
    )


@projects.route("/<project_id>/members/", methods=["POST"])
@login_required
def member_add(org_username, project_id):
    project = (
        Project.query.filter(Project.members.any(id=current_user.id))
        .filter_by(public_id=project_id, project_id=None)
        .first()
    )
    if project is None:
        abort(404)
    add_members_form = AddMemberForm()
    for member in current_user.organization.members:
        if member not in project.members:
            add_members_form.members.choices.append((member.id, member.email))
    if add_members_form.validate_on_submit():
        new_members = add_members_form.members.data
        if len(new_members) == 0:
            flash("Please select member(s) to add ", "warning")
        else:
            for new_member_id in new_members:
                member = Member.query.filter_by(
                    id=new_member_id, organization=current_user.organization
                ).first()
                if member:
                    db.session.add(
                        MemberProject(project_id=project.id, member_id=member.id)
                    )
            db.session.commit()
            flash("New member(s) has been added to project", "success")
    else:
        flash("Something went wrong please try again", "error")
    return redirect(
        url_for(
            ".detail",
            project_id=project.public_id,
            org_username=current_user.organization.username,
        )
    )
