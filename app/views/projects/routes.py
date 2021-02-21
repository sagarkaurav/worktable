from app import db
from app.models import Project
from flask import Blueprint, abort, redirect, render_template, request, url_for
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
            owner=current_user,
        )
        db.session.add(project)
        db.session.commit()
        return redirect(
            url_for(".detail", project_id=project.public_id, org_username=org_username)
        )
    return render_template("projects/create.html", form=new_project)


@projects.route("/<project_id>/", subdomain="<org_username>", methods=["GET", "POST"])
@login_required
def detail(org_username, project_id):
    project = Project.query.filter_by(
        owner=current_user, public_id=project_id, project_id=None
    ).first()
    if project is None:
        abort(404)
    new_comment = CreateComment()
    if new_comment.validate_on_submit():
        comment = Project(
            name="",
            description=new_comment.description.data,
            owner=current_user,
            project=project,
        )
        new_comment = CreateComment()
        db.session.add(comment)
        db.session.commit()
    page = request.args.get("page", 1)
    comments = Project.query.filter_by(project=project).paginate(page, 10)
    return render_template(
        "projects/detail.html", project=project, comments=comments, form=new_comment
    )
