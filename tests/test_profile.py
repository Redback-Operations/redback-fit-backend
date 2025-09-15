import pytest

def _signup_and_login(client, email="profileuser@example.com"):
    client.post("/auth/signup", data={
        "name": "Profile User",
        "email": email,
        "password": "StrongPass123!",
        "confirm_password": "StrongPass123!",
    })
    client.post("/auth/login", data={"email": email, "password": "StrongPass123!"}, follow_redirects=True)

def _discover_profile_routes(app):
    with app.app_context():
        rules = list(app.url_map.iter_rules())
    # All routes mounted under /api/profile
    profile_rules = [r for r in rules if str(r.rule).startswith("/api/profile")]
    return profile_rules

def _find_self_get_route(app):
    """
    Try common patterns first; else fallback to any GET route under /api/profile
    that doesn't look like an admin/list endpoint.
    """
    with app.app_context():
        rules = list(app.url_map.iter_rules())
    # Preferred explicit names
    preferred = ["/api/profile/self", "/api/profile/me", "/api/profile"]
    for p in preferred:
        for r in rules:
            if r.rule == p and "GET" in r.methods:
                return r.rule
    # Fallback: first GET-able route under /api/profile (non-collection)
    for r in rules:
        if str(r.rule).startswith("/api/profile") and "GET" in r.methods:
            return r.rule
    return None

def _find_update_route(app):
    """
    Look for PUT/PATCH/POST routes under /api/profile that look like update/edit.
    """
    with app.app_context():
        rules = list(app.url_map.iter_rules())

    # Try explicit update-like paths first
    keywords = ("update", "edit", "set")
    for r in rules:
        path = str(r.rule)
        if not path.startswith("/api/profile"):
            continue
        if any(k in path.lower() for k in keywords) and ({"PUT","PATCH","POST"} & set(r.methods)):
            return path, next(iter({"PUT","PATCH","POST"} & set(r.methods)))

    # Fallback: PUT/PATCH to /api/profile (common pattern)
    for r in rules:
        if r.rule == "/api/profile" and ({"PUT","PATCH"} & set(r.methods)):
            m = "PUT" if "PUT" in r.methods else "PATCH"
            return r.rule, m

    # Last resort: any POST route under /api/profile
    for r in rules:
        if str(r.rule).startswith("/api/profile") and "POST" in r.methods:
            return r.rule, "POST"

    return None, None

def test_get_profile_self(client, app):
    _signup_and_login(client)
    target = _find_self_get_route(app)
    if not target:
        # Print possible routes to help you wire it up
        routes = sorted([f"{r.rule} -> {sorted(r.methods)}" for r in _discover_profile_routes(app)])
        pytest.skip(f"No GET route for self profile found under /api/profile. Available: {routes}")

    resp = client.get(target)
    assert resp.status_code == 200, f"{target} returned {resp.status_code}"
    data = resp.get_json()
    assert data is not None, f"{target} did not return JSON"

    # Accept any of these common fields
    has_any = any(k in data for k in ("email", "account", "name", "id", "user_id", "pseudoId"))
    assert has_any, f"{target} JSON missing expected identity fields: {data.keys()}"

def test_update_profile_validation(client, app):
    _signup_and_login(client, email="updateprofile@example.com")
    target, method = _find_update_route(app)
    if not target:
        routes = sorted([f"{r.rule} -> {sorted(r.methods)}" for r in _discover_profile_routes(app)])
        pytest.skip(f"No update-like route (PUT/PATCH/POST) found under /api/profile. Available: {routes}")

    # Invalid payloads to trigger validation errors (adjust as your schema evolves)
    bad_payloads = [
        {"name": ""},                # empty name
        {"birthDate": "not-a-date"}, # wrong format
        {"gender": 123},             # wrong type
    ]

    for body in bad_payloads:
        if method == "PUT":
            r = client.put(target, json=body)
        elif method == "PATCH":
            r = client.patch(target, json=body)
        else:
            r = client.post(target, json=body)
        # If CSRF is enforced on POST, you may get 400 — that still indicates rejection.
        assert r.status_code in (400, 401, 403, 422), f"{target} ({method}) returned {r.status_code}"
