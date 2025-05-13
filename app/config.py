import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///redback.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    FIREBASE_CREDENTIALS = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
    FIREBASE_DATABASE_URL = os.getenv('FIREBASE_DATABASE_URL')
    FIREBASE_API_KEY = os.getenv('FIREBASE_API_KEY')
    # OAuth client credentials
    OAUTH_CLIENT_ID     = os.getenv('OAUTH_CLIENT_ID')
    OAUTH_CLIENT_SECRET = os.getenv('OAUTH_CLIENT_SECRET')
    OAUTH_AUTHORIZE_URL = os.getenv('OAUTH_AUTHORIZE_URL')
    OAUTH_TOKEN_URL     = os.getenv('OAUTH_TOKEN_URL')
    OAUTH_API_BASE_URL  = os.getenv('OAUTH_API_BASE_URL')