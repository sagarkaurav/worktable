from flask import Flask, flash, redirect, url_for
from flask_login import LoginManager, current_user, logout_user
from flask_mail import Mail
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
migrate = Migrate()
mail = Mail()


def create_app(config="app.config.ProductionConfig"):
    app = Flask(__name__, subdomain_matching=True)
    app.config.from_object(config)
    login_manager = LoginManager()
    login_manager.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db, directory="app/db/migrations", compare_type=True)
    mail.init_app(app)
    from app.models import Member, MemberInvite, MemberProject, Organization, Project
    from app.views.auth import auth
    from app.views.dashboard import dashboard
    from app.views.home import home
    from app.views.members import members
    from app.views.profile import profile
    from app.views.projects import projects
    from app.views.reset_passwords import reset_passwords

    app.register_blueprint(home)
    app.register_blueprint(auth, url_prefix="/organizations")
    app.register_blueprint(dashboard, url_prefix="/dashboard")
    app.register_blueprint(projects, url_prefix="/projects")
    app.register_blueprint(members, url_prefix="/members")
    app.register_blueprint(profile, url_prefix="/profile")
    app.register_blueprint(reset_passwords, url_prefix="/reset-passwords")

    @login_manager.user_loader
    def load_user(user_id):
        return Member.query.get(user_id)

    @app.before_request
    def bar():
        if current_user.is_authenticated and current_user.disabled_at is not None:
            redirect_url = url_for(
                "auth.login", org_username=current_user.organization.username
            )
            logout_user()
            flash("You account has been disabled", "error")
            return redirect(redirect_url)

    return app
