import os, sys
import pytest

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from app import create_app
from models import db


@pytest.fixture()
def app():
    os.environ["SECRET_KEY"] = "test"
    app = create_app()
    app.config.update(
        TESTING = True,
        SQLALCHEMY_DATABASE_URI = ":memory:",
        SQLALCHEMY_TRACK_MODIFICATIONS = False,
        WTF_CSRF_ENABLED = False,  # Disable CSRF for testing  
        SERVER_NAME = "localhost.localdomain",  # Needed for url_for() during tests
        RATE_LIMIT_ENABLED = False,  # Disable rate limiting for tests
        RATELIMIT_STORAGE_URL = "memory://",  # Use in-memory storage for rate limiting
        SESSION_COOKIE_SECURE = None,  # Disable secure cookies for testing
    )
    with app.app_context():
        db.drop_all()
        db.create_all()
    yield app


@pytest.fixture()
def client(app):
    return app.test_client()    