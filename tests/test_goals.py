def _signup_and_login(client, email="goaluser@example.com"):
    client.post("/auth/signup", data={
        "name": "Goal User",
        "email": email,
        "password": "StrongPass123!",
        "confirm_password": "StrongPass123!",
    })
    client.post("/auth/login",
                data={"email": email, "password": "StrongPass123!"},
                follow_redirects=True)

def _get_self_profile(client):
    for path in ("/api/profile/self", "/api/profile"):
        r = client.get(path)
        if r.status_code != 404:
            return r.get_json() or {}
    return {}

def test_create_goal_success(client):
    _signup_and_login(client)
    me = _get_self_profile(client)
    user_id = me.get("user_id") or me.get("id")
    assert user_id is not None

    payload = {
        "user_id": user_id,
        "start_date": "2025-01-01",
        "end_date":   "2025-12-31",
        "steps": 1000,
    }

    resp = client.post("/api/goals/", json=payload, follow_redirects=True)
    assert resp.status_code in (200, 201), f"{resp.status_code} {resp.data!r}"

    data = resp.get_json()
    assert data is not None
    # your model returns an id and the numeric fields
    assert "id" in data
    assert data["user_id"] == user_id
    assert data["start_date"] == "2025-01-01"
    assert data["end_date"] == "2025-12-31"
    assert data["steps"] == 1000


def test_get_goals_lists_created(client):
    _signup_and_login(client)
    me = _get_self_profile(client)
    user_id = me.get("user_id") or me.get("id")
    assert user_id is not None

    # Create a goal first
    payload = {
        "user_id": user_id,
        "start_date": "2025-01-01",
        "end_date": "2025-12-31",
        "steps": 5000,
    }
    resp = client.post("/api/goals/", json=payload)
    assert resp.status_code in (200, 201)
    created = resp.get_json()
    assert created is not None
    assert created["user_id"] == user_id

    # Now fetch goals list
    list_resp = client.get(f"/api/goals/{user_id}")
    assert list_resp.status_code == 200
    goals = list_resp.get_json()
    assert isinstance(goals, list)
    # Ensure the one we just created is in the list
    assert any(g["id"] == created["id"] for g in goals)


def _signup_and_login_as(client, name, email):
    client.post("/auth/signup", data={
        "name": name,
        "email": email,
        "password": "StrongPass123!",
        "confirm_password": "StrongPass123!",
    })
    client.post("/auth/login",
                data={"email": email, "password": "StrongPass123!"},
                follow_redirects=True)

def _get_me(client):
    """Return current user's profile JSON."""
    for path in ("/api/profile/self", "/api/profile"):
        r = client.get(path)
        if r.status_code != 404:
            return r.get_json() or {}
    return {}

def _create_goal_for_me(client,  **extra):
    me = _get_me(client)
    uid = me.get("user_id") or me.get("id")
    assert uid is not None, f"Could not determine user_id from profile: {me}"
    payload = {
        "user_id": uid,
        "start_date": "2025-01-01",
        "end_date": "2025-12-31",
        "steps": 1000,
        **extra,
    }
    r = client.post("/api/goals/", json=payload)
    assert r.status_code in (200, 201), f"{r.status_code} {r.data!r}"
    return r.get_json()

def test_update_goal_only_owner(client):
    # User A creates a goal
    _signup_and_login_as(client, "Alice", "alice@example.com")
    goal = _create_goal_for_me(client)
    goal_id = goal["id"]

    # User B logs in and attempts to update Alice's goal
    client.get("/auth/logout", follow_redirects=True)
    _signup_and_login_as(client, "Bob", "bob@example.com")

    resp = client.put(f"/api/goals/{goal_id}", json={"steps": 7777})

    # Expect forbidden (best), or 404 if you choose to hide existence
    assert resp.status_code in (403, 404)

def test_owner_can_update_goal(client):
    # Owner should be able to update their own goal
    _signup_and_login_as(client, "Carol", "carol@example.com")
    goal = _create_goal_for_me(client)
    goal_id = goal["id"]

    r = client.put(f"/api/goals/{goal_id}", json={"steps": 4321})
    assert r.status_code in (200, 204)
    data = r.get_json() or {}
    # depending on your update response; many of your routes return goal.as_dict()
    if data:
        assert data.get("steps") == 4321


def test_get_goals_lists_created(client):
    # sign up & login
    client.post("/auth/signup", data={
        "name": "Lister",
        "email": "lister@example.com",
        "password": "StrongPass123!",
        "confirm_password": "StrongPass123!",
    })
    client.post("/auth/login",
                data={"email": "lister@example.com", "password": "StrongPass123!"},
                follow_redirects=True)

    # get my user_id from profile
    me = None
    for path in ("/api/profile/self", "/api/profile"):
        r = client.get(path)
        if r.status_code != 404:
            me = r.get_json()
            break
    assert me is not None, "Could not fetch self profile"
    user_id = me.get("user_id") or me.get("id")
    assert user_id is not None

    # create a goal
    create_payload = {
        "user_id": user_id,
        "start_date": "2025-01-01",
        "end_date": "2025-12-31",
        "steps": 5000,
    }
    create_resp = client.post("/api/goals/", json=create_payload)
    assert create_resp.status_code in (200, 201), f"{create_resp.status_code} {create_resp.data!r}"
    created = create_resp.get_json()
    assert created and "id" in created
    created_id = created["id"]

    # list goals for this user
    list_resp = client.get(f"/api/goals/{user_id}")
    assert list_resp.status_code == 200
    goals = list_resp.get_json()
    assert isinstance(goals, list)
    # the new goal should be in the list
    assert any(g.get("id") == created_id for g in goals), f"Created goal {created_id} not found in {goals}"


def test_update_goal_validation_errors(client):
    _signup_and_login_as(client, "Val", "val@example.com")
    goal = _create_goal_for_me(client)
    gid = goal["id"]

    # bad date format
    r1 = client.put(f"/api/goals/{gid}", json={"start_date": "01-01-2025"})
    assert r1.status_code in (400, 422)

    # negative number
    r2 = client.put(f"/api/goals/{gid}", json={"steps": -10})
    assert r2.status_code in (400, 422)


def test_delete_goal_only_owner(client):
    # Owner creates a goal
    _signup_and_login_as(client, "Owner", "owner@example.com")
    g = _create_goal_for_me(client)
    gid = g["id"]

    # Another user attempts delete
    client.get("/auth/logout", follow_redirects=True)
    _signup_and_login_as(client, "Intruder", "intruder@example.com")
    r = client.delete(f"/api/goals/{gid}")
    assert r.status_code in (403, 404)

    # Owner can delete
    client.get("/auth/logout", follow_redirects=True)
    _signup_and_login_as(client, "Owner", "owner@example.com")
    r2 = client.delete(f"/api/goals/{gid}")
    assert r2.status_code in (200, 204)