import json
from datetime import datetime
import pytest

API = "/api/synced"  

def test_update_missing_id(client):
    resp = client.post(f"{API}/update", json={})
    assert resp.status_code == 400
    assert "Missing user_id" in resp.get_data(as_text=True)

def test_update_not_found(client):
    resp = client.post(f"{API}/update", json={"user_id": 999})
    assert resp.status_code == 404
    assert "User not found" in resp.get_data(as_text=True)

def test_update_success(client, sample_user):
    resp = client.post(f"{API}/update", json={"user_id": sample_user.id})
    data = resp.get_json()
    assert resp.status_code == 200
    assert data["user_id"] == str(sample_user.id)

    dt = datetime.strptime(data["last_synced"], "%Y-%m-%dT%H:%M:%SZ")
    assert abs((dt - datetime.utcnow()).total_seconds()) < 5

def test_last_missing_id(client):
    resp = client.get(f"{API}/last")
    assert resp.status_code == 400
    assert "Missing user_id" in resp.get_data(as_text=True)

def test_last_not_found(client):
    resp = client.get(f"{API}/last?user_id=999")
    assert resp.status_code == 404
    assert "User not found" in resp.get_data(as_text=True)

def test_last_success(client, sample_user):
    # first set a sync
    client.post(f"{API}/update", json={"user_id": sample_user.id})
    # then retrieve
    resp = client.get(f"{API}/last?user_id={sample_user.id}")
    data = resp.get_json()
    assert resp.status_code == 200
    # the last_synced we get back matches the DB
    assert data["user_id"] == str(sample_user.id)
    assert "last_synced" in data
