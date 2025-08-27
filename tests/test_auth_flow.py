def test_next_param_is_safe(client):
    response = client.get("/auth/login?next=/home")
    assert response.status_code == 200