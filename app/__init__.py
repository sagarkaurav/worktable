from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
migrate = Migrate()


def create_app(config="app.config.ProductionConfig"):
    app = Flask(__name__, subdomain_matching=True)
    app.config.from_object(config)
    db.init_app(app)
    migrate.init_app(app, db, directory="app/db/migrations", compare_type=True)
    from app.views.home import home

    app.register_blueprint(home)

    return app
