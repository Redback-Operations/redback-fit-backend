def _post_signup(client, payload):
    r = client.post("/signup", data=payload, follow_redirects=False)
    if r.status_code == 404:
        r = client.post("/auth/signup", data=payload, follow_redirects=False)
    return r

def _post_login(client, payload, follow_redirects=False):
    r = client.post("/login", data=payload, follow_redirects=follow_redirects)
    if r.status_code == 404:
        r = client.post("/auth/login", data=payload, follow_redirects=follow_redirects)
    return r

def _get_protected(client):
    """
    Try a few likely protected endpoints.
    Adjust this list to match your repo if you know the exact route.
    """
    candidates = [
        "/api/profile",        # likely from your earlier anonymized profile work
        "/profile",
        "/auth/me",
        "/dashboard",
        "/home",
    ]
    last = None
    for path in candidates:
        last = client.get(path)
        if last.status_code != 404:
            return last, path
    return last, candidates[-1]

def test_protected_route_with_valid_token(client):
    # Sign up and log in (session cookie is stored in client)
    client.post("/auth/signup", data={
        "name": "Token User",
        "email": "tokenuser@example.com",
        "password": "StrongPass123!",
        "confirm_password": "StrongPass123!",
    })

    r = client.post("/auth/login",
                    data={"email": "tokenuser@example.com", "password": "StrongPass123!"},
                    follow_redirects=True)
    assert r.status_code in (200, 302)

    # Hit a known protected route
    resp = client.get("/home")
    assert resp.status_code == 200


def test_protected_route_without_token(client):
    # Not logged in → should redirect to auth.login or 401/403 (depending on config)
    resp = client.get("/home")
    assert resp.status_code in (302, 401, 403)
