from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
migrate = Migrate()


def create_app(config="app.config.ProductionConfig"):
    app = Flask(__name__, subdomain_matching=True)
    app.config.from_object(config)
    login_manager = LoginManager()
    login_manager.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db, directory="app/db/migrations", compare_type=True)
    from app.models import Member, Organization  # noqa F401
    from app.views.auth import auth
    from app.views.dashboard import dashboard
    from app.views.home import home

    app.register_blueprint(home)
    app.register_blueprint(auth, url_prefix="/organizations")
    app.register_blueprint(dashboard, url_prefix="/dashboard")

    @login_manager.user_loader
    def load_user(user_id):
        return Member.query.get(user_id)

    return app
