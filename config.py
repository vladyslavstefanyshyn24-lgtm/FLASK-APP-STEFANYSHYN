from pathlib import Path
class Config:
    SECRET_KEY = "supersecretkey"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

BASE_DIR = Path(__file__).resolve().parent
class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{BASE_DIR / 'instance' / 'app.db'}"

class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{BASE_DIR / 'instance' / 'app.db'}"


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"


config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "testing": TestingConfig
}
