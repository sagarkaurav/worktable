import os


class BaseConfig:
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SERVER_NAME = os.environ.get("SERVER_NAME", "localhost:5000")
    SECRET_KEY = os.environ.get("SECRET_KEY")
    MAIL_SERVER = os.environ.get("MAIL_SERVER", "localhost")
    MAIL_PORT = os.environ.get("MAIL_PORT", "25")
    MAIL_USE_TLS = bool(int(os.environ.get("MAIL_USE_TLS", "1")))
    MAIL_USE_SSL = bool(int(os.environ.get("MAIL_USE_SSL", "1")))
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")


class ProductionConfig(BaseConfig):
    pass


class DevelopmentConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", "sqlite:///database.db")
    SECRET_KEY = "secretkey"
    MAIL_SERVER = os.environ.get("MAIL_SERVER", "mailserver")
    MAIL_USE_TLS = bool(int(os.environ.get("MAIL_USE_TLS", "0")))
    MAIL_USE_SSL = bool(int(os.environ.get("MAIL_USE_SSL", "0")))


class TestConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = "sqlite:///database.db"
