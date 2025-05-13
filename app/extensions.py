from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from authlib.integrations.flask_client import OAuth
import firebase_admin
from firebase_admin import credentials, auth as firebase_auth
from functools import wraps
from flask import request, jsonify

# Initialize Flask extensions
# To be initialized in create_app() via .init_app(app)
db = SQLAlchemy()
migrate = Migrate()
cors = CORS()
oauth = OAuth()


def init_firebase_app(app):
    """
    Initialize Firebase Admin SDK with service account credentials.
    Expects FIREBASE_CREDENTIALS and FIREBASE_DATABASE_URL in app config.
    """
    cred_path = app.config.get('FIREBASE_CREDENTIALS')
    if not cred_path:
        raise RuntimeError(
            "FIREBASE_CREDENTIALS (path to service account JSON) must be set"
        )
    cred = credentials.Certificate(cred_path)
    firebase_admin.initialize_app(cred, {
        'databaseURL': app.config.get('FIREBASE_DATABASE_URL')
    })


def token_required(f):
    """
    Decorator that validates Firebase ID tokens on incoming requests.
    Injects current_uid as the first argument to the decorated function.
    """
    @wraps(f)
    def wrapper(*args, **kwargs):
        auth_header = request.headers.get('Authorization', '')
        if not auth_header.startswith('Bearer '):
            return jsonify({'error': 'Missing or invalid Authorization header'}), 401
        id_token = auth_header.split(' ')[1]
        try:
            decoded_token = firebase_auth.verify_id_token(id_token)
            current_uid = decoded_token.get('uid')
        except Exception as e:
            return jsonify({'error': str(e)}), 401
        return f(current_uid, *args, **kwargs)
    return wrapper
