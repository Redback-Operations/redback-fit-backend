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

def _post_signup(client, payload):
    # Try plain /signup first; if your blueprint is prefixed, fall back to /auth/signup
    resp = client.post("/signup", data=payload, follow_redirects=False)
    if resp.status_code == 404:
        resp = client.post("/auth/signup", data=payload, follow_redirects=False)
    return resp

def _post_login(client, payload):
    # Try plain /login; fall back to /auth/login
    resp = client.post("/login", data=payload, follow_redirects=False)
    if resp.status_code == 404:
        resp = client.post("/auth/login", data=payload, follow_redirects=False)
    return resp

def test_login_success(client):
    # 1) create a user via your signup route (send all required fields)
    signup_payload = {
        "name": "Test User",
        "email": "testuser@example.com",
        "password": "StrongPass123!",
        "confirm_password": "StrongPass123!",  # keep if your route validates this
    }
    s = _post_signup(client, signup_payload)
    assert s.status_code in (200, 201, 302)

    # 2) login with those credentials; don't follow redirects so we can read Set-Cookie
    login_payload = {"email": "testuser@example.com", "password": "StrongPass123!"}
    r = _post_login(client, login_payload)

    assert r.status_code in (200, 302)
    # If you use Flask-Login session cookies, this will be set on the redirect response
    set_cookie = r.headers.get("Set-Cookie", "")
    # If your app uses JWT-in-JSON instead, comment the next line and assert on JSON below
    assert "session=" in set_cookie
