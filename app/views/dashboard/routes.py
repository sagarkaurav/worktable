from app.models import Project
from flask import Blueprint, render_template, request
from flask_login import current_user, login_required

dash = Blueprint("dashboard", __name__, template_folder="templates")


@dash.route("/", subdomain="<org_username>", methods=["GET"])
@login_required
def index(org_username):
    page = request.args.get("page", 1)
    projects = (
        Project.query.filter(Project.permissions.any(member=current_user))
        .filter_by(project_id=None)
        .order_by(Project.id.desc())
        .paginate(int(page), 5)
    )
    return render_template("dashboard/index.html", projects=projects)
