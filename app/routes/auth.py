from flask import Blueprint, request, jsonify, session, redirect, url_for, current_app
from app.extensions import db, oauth
from app.models import UserProfile

import secrets

auth_bp = Blueprint('auth', __name__)

# Manual Registration
@auth_bp.route('/register', methods=['POST'])
def register():
   
    
    """Register a new user with full name, email and password."""
    data = request.get_json() or {}
    print("▶️ register payload:", request.get_json())

    full_name = data.get('full_name') or data.get('name')
    email = data.get('email')
    password = data.get('password')

    if not full_name or not email or not password:
        return jsonify({'msg': 'Full Name, Email and password required'}), 400
    if UserProfile.query.filter_by(email=email).first():
        return jsonify({'msg': 'User already exists'}), 409
    
    user = UserProfile(name=full_name, email=email)
    
    db.session.add(user)
    db.session.commit()
    return jsonify({'msg': 'Registration successful', 'user': {'id': user.id, 'full_name': user.name, 'email': user.email}}), 201

# OAuth Authentication
@auth_bp.route('/login')
def login():
    """Start OAuth login/signup flow by redirecting to provider."""
    state = secrets.token_urlsafe(16)
    session['oauth_state'] = state
    redirect_uri = url_for('auth.callback', _external=True)
    return oauth.provider.authorize_redirect(redirect_uri, state=state)

@auth_bp.route('/callback')
def callback():
    """Handle OAuth callback, provision local user if new, then redirect."""
    incoming_state = request.args.get('state')
    stored_state = session.pop('oauth_state', None)
    if incoming_state != stored_state:
        return jsonify({'error': 'Invalid state'}), 400

    token = oauth.provider.authorize_access_token()
    user_info = oauth.provider.parse_id_token(token)
    # Find or create local user
    user = UserProfile.query.filter_by(oauth_id=user_info['sub']).first()
    if not user:
        user = UserProfile(oauth_id=user_info['sub'], email=user_info.get('email'))
        db.session.add(user)
        db.session.commit()

    # Store user session
    session['user_id'] = user.id
    # Redirect to front-end dashboard
    return redirect(current_app.config['FRONTEND_URL'] + '/dashboard')

# Logout & Status
@auth_bp.route('/logout')
def logout():
    """Clear session and logout user."""
    session.clear()
    return redirect(current_app.config['FRONTEND_URL'] + '/login')

@auth_bp.route('/status')
def status():
    """Return authentication status and user info if logged in."""
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'authenticated': False}), 200
    user = UserProfile.query.get(user_id)
    return jsonify({'authenticated': True, 'user': {'id': user.id, 'email': user.email}}), 200
