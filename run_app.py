import os

from app import create_app

config_map = {
    "development": "app.config.DevelopmentConfig",
    "production": "app.config.ProductionConfig",
    "testing": "app.config.TestConfig",
}

config = config_map[os.environ.get("FLASK_ENV")]
app = create_app(config=config)

if __name__ == "__main__":
    app.run()
