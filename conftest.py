import pytest
from app import app as flask_app, db
from models.user import UserProfile

@pytest.fixture
def app():
    # tell Flask to use testing config & in‑memory sqlite
    flask_app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "SQLALCHEMY_TRACK_MODIFICATIONS": False,
    })
    with flask_app.app_context():
        db.create_all()
        yield flask_app
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def sample_user(app):
    u = UserProfile(name="Test", account="acct1", birthDate="2000-01-01", gender="F")
    db.session.add(u)
    db.session.commit()
    return u
