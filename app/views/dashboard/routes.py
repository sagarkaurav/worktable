from flask import Blueprint, render_template
from flask_login import login_required

dash = Blueprint("dashboard", __name__, template_folder="templates")


@dash.route("/", subdomain="<org_username>", methods=["GET"])
@login_required
def index(org_username):
    return render_template("dashboard/index.html")
