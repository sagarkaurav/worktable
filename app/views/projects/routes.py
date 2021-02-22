from app import db
from app.models import MemberProject, Project
from flask import Blueprint, abort, redirect, render_template, url_for
from flask_login import current_user, login_required

from .forms import CreateComment, CreateProject

projects = Blueprint("projects", __name__, template_folder="templates")


@projects.route("/create/", subdomain="<org_username>", methods=["GET", "POST"])
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


@projects.route("/<project_id>/", subdomain="<org_username>", methods=["GET", "POST"])
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
    if new_comment.validate_on_submit():
        comment = Project(
            description=new_comment.description.data,
            project=project,
            created_by_id=current_user.id,
        )
        permission = MemberProject(member=current_user)
        comment.permissions.append(permission)
        db.session.add(comment)
        db.session.add(comment)
        db.session.commit()
        return redirect(
            url_for(".detail", org_username=org_username, project_id=project_id)
        )
    return render_template("projects/detail.html", project=project, form=new_comment)
