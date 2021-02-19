from flask import Blueprint, current_app, redirect, render_template, request

home = Blueprint("home", __name__, template_folder="templates")


@home.route("/")
def index():
    return render_template("home/index.html")
