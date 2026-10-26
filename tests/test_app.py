from app import create_app
from app.config import TestConfig

def app_test():
    app = create_app(TestConfig)
    # Comprobaciones Criticas
    assert app.config["TESTING"] is True
    assert app.config["SQLALCHEMY_DATABASE_URI"] == "sqlite:///:memory"    