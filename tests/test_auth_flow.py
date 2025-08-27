from models import db, UserCredential, UserProfile

def test_login_wrong_password(client, app):
    with app.app_context():
        u = UserCredential(email="x@y.com")
        u.set_password("Password123")
        db.session.add(u)
        db.session.flush()
        db.session.add(UserProfile(user_id=u.id, name="Test User", account="x@y", birthDate="2000-01-01"))
        db.session.commit()

    res = client.post('/auth/login', data={"email": "x@y.com", "password": "badpw"}, follow_redirects=False)
    assert res.status_code == 400
    assert b'Login failed. Incorrect email or password.' in res.data

def test_logout_requires_login(client):
    res = client.get('/auth/logout')
    assert res.status_code == 302 # Redirect to login

def test_next_param_is_safe(client):
    response = client.get("/auth/login?next=/home")
    assert response.status_code == 200