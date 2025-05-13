import traceback
from flask import Blueprint, request, jsonify, current_app
from app.extensions import init_firebase_app, token_required
import firebase_admin
from firebase_admin import auth as firebase_auth, db as firebase_db
import requests
from requests.exceptions import HTTPError, Timeout, ConnectionError, RequestException

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

@auth_bp.route('/register', methods=['POST'])
def register():
    """
    Register a new user with Firebase Auth and store profile in Realtime Database.
    Expects JSON: { name or full_name, email, password }.
    """
    data = request.get_json() or {}
    full_name = data.get('full_name') or data.get('name')
    email = data.get('email')
    password = data.get('password')
    if not full_name or not email or not password:
        return jsonify({'msg': 'Full Name, Email and password required'}), 400

    try:
        # Initialize Firebase if necessary (usually done in create_app)
        if not firebase_admin._apps:
            init_firebase_app(app) 
        # Create user in Firebase Auth
        user_record = firebase_auth.create_user(email=email, password=password)
        
        print(full_name)
        uid = user_record.uid
        # Store user profile in Firebase Realtime Database
        ref = firebase_db.reference(f'users/{uid}')
        ref.set({'name': full_name, 'email': email})

        return jsonify({
            'msg': 'Registration successful',
            'user': {'uid': uid, 'name': full_name, 'email': email}
        }), 201

    except Exception as e:
        # Print full stack to console to log error description
        traceback.print_exc()
        return jsonify({'msg': str(e)}), 400

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json() or {}
    email = data.get('email')
    password = data.get('password')
    if not email or not password:
        return jsonify({'msg': 'Email and password required'}), 400

    api_key = current_app.config.get('FIREBASE_API_KEY')
    if not api_key:
        current_app.logger.error("FIREBASE_API_KEY not set")
        return jsonify({'msg': 'Server misconfiguration'}), 500

    url = f'https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={api_key}'
    payload = {'email': email, 'password': password, 'returnSecureToken': True}

    try:
        resp = requests.post(url, json=payload, timeout=5)
        resp.raise_for_status()
        return jsonify(resp.json()), 200

    except HTTPError:
        # Attempt to parse the Firebase error payload
        try:
            err = resp.json().get('error', {})
            code = err.get('message', '')
        except ValueError:
            # Non-JSON or empty body
            return jsonify({'msg': 'Authentication failed'}), 502

        # Map known Firebase error codes to responses
        if code == 'EMAIL_NOT_FOUND':
            return jsonify({'msg': 'No user found with that email'}), 404
        if code == 'INVALID_PASSWORD':
            return jsonify({'msg': 'Incorrect password'}), 401
        if code == 'USER_DISABLED':
            return jsonify({'msg': 'User account has been disabled'}), 403

        # Fallback for other errors
        return jsonify({'msg': code}), resp.status_code

    except Timeout:
        current_app.logger.error("Firebase Auth request timed out")
        return jsonify({'msg': 'Authentication service timed out'}), 504

    except ConnectionError:
        current_app.logger.error("Could not connect to Firebase Auth endpoint")
        return jsonify({'msg': 'Cannot reach authentication service'}), 503

    except RequestException as e:
        current_app.logger.exception("Unexpected error calling Firebase Auth")
        return jsonify({'msg': 'Authentication service error'}), 503

    except Exception as e:
        current_app.logger.exception("Unhandled exception in login")
        return jsonify({'msg': 'Internal server error'}), 500

@auth_bp.route('/logout', methods=['POST'])
@token_required
def logout(current_uid):
    """
    Revoke user refresh tokens to force logout on client side.
    """
    try:
        firebase_auth.revoke_refresh_tokens(current_uid)
        return jsonify({'msg': 'Logged out successfully'}), 200
    except Exception as e:
        return jsonify({'msg': str(e)}), 400

@auth_bp.route('/status', methods=['GET'])
@token_required
def status(current_uid):
    """
    Check authentication status; return user profile from Realtime Database.
    """
    try:
        user_ref = firebase_db.reference(f'users/{current_uid}')
        user_data = user_ref.get() or {}
        return jsonify({'authenticated': True, 'user': {'uid': current_uid, **user_data}}), 200
    except Exception as e:
        return jsonify({'authenticated': False, 'msg': str(e)}), 500
