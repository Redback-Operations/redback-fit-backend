from app.extensions import oauth

def register_oauth_clients(app):
    # Example for a generic provider; adjust URLs and params as needed
    oauth.register(
        name='provider',
        client_id=app.config['OAUTH_CLIENT_ID'],
        client_secret=app.config['OAUTH_CLIENT_SECRET'],
        access_token_url=app.config['OAUTH_TOKEN_URL'],
        authorize_url=app.config['OAUTH_AUTHORIZE_URL'],
        api_base_url=app.config['OAUTH_API_BASE_URL'],
        client_kwargs={'scope': 'openid email profile'},
    )
