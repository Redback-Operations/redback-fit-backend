import pytest

def _signup_and_login(client, email="activity@example.com"):
    client.post("/auth/signup", data={
        "name": "Act User",
        "email": email,
        "password": "StrongPass123!",
        "confirm_password": "StrongPass123!",
    })
    client.post("/auth/login",
                data={"email": email, "password": "StrongPass123!"},
                follow_redirects=True)

ACTIVITY_PATH = "/api/dashboard/activity"

def _route_exists(app, path):
    with app.app_context():
        return any(r.rule == path for r in app.url_map.iter_rules())

def test_post_activity_valid(client, app):
    if not _route_exists(app, ACTIVITY_PATH):
        pytest.skip(f"Activity endpoint not implemented yet: expected {ACTIVITY_PATH}")

    _signup_and_login(client)

    payload = {
        "date": "2025-01-02",      # YYYY-MM-DD
        "steps": 6200,
        "minutes_running": 20,
        "minutes_cycling": 0,
        "minutes_swimming": 0,
        "minutes_exercise": 30,
        "calories": 450
    }
    r = client.post(ACTIVITY_PATH, json=payload)
    assert r.status_code in (200, 201), f"{r.status_code} {r.data!r}"
    data = r.get_json() or {}
    # minimal expectations
    assert data.get("date") == "2025-01-02"
    assert data.get("steps") == 6200

def test_post_activity_missing_field(client, app):
    if not _route_exists(app, ACTIVITY_PATH):
        pytest.skip(f"Activity endpoint not implemented yet: expected {ACTIVITY_PATH}")

    _signup_and_login(client)

    bad_payload = {  # missing 'date'
        "steps": 3000
    }
    r = client.post(ACTIVITY_PATH, json=bad_payload)
    assert r.status_code in (400, 422), f"{r.status_code} {r.data!r}"
