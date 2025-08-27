def test_signup_rejects_short_password(client):
    response = client.post('/auth/signup', data={
        'name': 'Test User',
        'email': 'a@b.com',
        'password': 'short'
    }, follow_redirects=True)
    assert b'Signup failed. Password must be at least 8 characters long.' in response.data

def test_duplicate_email(client):
    client.post('/auth/signup', data={
        'name': 'Test User',
        'email': 'b@c.com',
        'password': 'Password123'
    })

    response = client.post('/auth/signup', data={
        'name': 'Another User',
        'email': 'b@c.com',
        'password': 'Password123'
    }, follow_redirects=True)
    assert b'signup failed. email already registered.' in response.data.lower()