from flask import Blueprint, redirect, url_for, session, request, jsonify
from app.extensions import oauth

# OAuth blueprint
auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login')
def login():
    """Redirect user to the OAuth provider's authorization page."""
    # Ensure redirect URI matches registered callback
    redirect_uri = url_for('auth.callback', _external=True)
    return oauth.provider.authorize_redirect(redirect_uri)

@auth_bp.route('/callback')
def callback():
    """Handle OAuth provider callback and fetch user info."""
    # Exchange code for tokens
    token = oauth.provider.authorize_access_token()
    # Fetch user information (adjust method per provider)
    user_info = oauth.provider.parse_id_token(token)

    # Store user in session
    session['user'] = user_info
    return jsonify({'message': 'Logged in', 'user': user_info}), 200

@auth_bp.route('/logout')
def logout():
    """Clear user session."""
    session.pop('user', None)
    return jsonify({'message': 'Logged out'}), 200

@auth_bp.route('/status')
def status():
    """Check current login status."""
    user = session.get('user')
    if not user:
        return jsonify({'authenticated': False}), 200
    return jsonify({'authenticated': True, 'user': user}), 200
