import os


class BaseConfig:
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SERVER_NAME = os.environ.get("SERVER_NAME", "localhost:5000")
    SECRET_KEY = os.environ.get("SECRET_KEY")


class ProductionConfig(BaseConfig):
    pass


class DevelopmentConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", "sqlite:///database.db")
    SECRET_KEY = "secretkey"


class TestConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = "sqlite:///database.db"
