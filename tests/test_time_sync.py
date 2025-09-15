import time
import pytest

TIME_SYNC_PATH = "/api/time-sync"  # implement this in your API when ready

def _ensure_logged_in(client):
    client.post("/auth/signup", data={
        "name": "Time User",
        "email": "timeuser@example.com",
        "password": "StrongPass123!",
        "confirm_password": "StrongPass123!",
    })
    client.post("/auth/login",
                data={"email": "timeuser@example.com", "password": "StrongPass123!"},
                follow_redirects=True)

def test_sync_returns_server_time(client, app):
    # Skip cleanly if the route isn't registered yet
    with app.app_context():
        paths = {r.rule for r in app.url_map.iter_rules()}
    if TIME_SYNC_PATH not in paths:
        pytest.skip(f"Time-sync endpoint not implemented yet: expected {TIME_SYNC_PATH}")

    _ensure_logged_in(client)  # in case your endpoint is protected

    # Call the endpoint (GET or POST—adjust when you implement it)
    resp = client.get(TIME_SYNC_PATH)
    if resp.status_code == 405:  # method not allowed -> try POST
        resp = client.post(TIME_SYNC_PATH, json={})

    assert resp.status_code in (200, 201)
    data = resp.get_json()
    assert data is not None and "server_time" in data

    server_time = int(float(data["server_time"]))
    now = int(time.time())
    assert abs(server_time - now) < 10


def test_sync_rejects_invalid_request(client, app):
    # Skip until the endpoint exists
    with app.app_context():
        paths = {r.rule for r in app.url_map.iter_rules()}
    if TIME_SYNC_PATH not in paths:
        pytest.skip(f"Time-sync endpoint not implemented yet: expected {TIME_SYNC_PATH}")

    _ensure_logged_in(client)

    # Example invalid body; adjust to your schema once implemented
    bad_payloads = [
        {},                           # missing required fields
        {"device_id": ""},            # empty id
        {"device_id": "abc", "readings": "not-a-list"},
    ]
    for body in bad_payloads:
        r = client.post(TIME_SYNC_PATH, json=body)
        assert r.status_code in (400, 422)
