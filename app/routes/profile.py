# /api/profile.py
from flask import Blueprint, jsonify, request, session
from app.models import UserProfile
from app.extensions import db

profile_bp = Blueprint('profile', __name__)


# Profile Endpoints #

# These routes are used by the frontend to fetch/update the user profile.
# Requires frontend request structure from ProfilePage.tsx

@profile_bp.route('', methods=['GET'])
def get_profile():
    """Fetch the authenticated user's profile."""
    user_info = session.get('user')
    if not user_info:
        return jsonify({'message': 'Unauthorized'}), 401

    user_id = user_info.get('id') or user_info.get('sub')
    user = UserProfile.query.get(user_id)
    if not user:
        return jsonify({'message': 'User not found'}), 404

    return jsonify({
        'id': user.id,
        'name': user.name,
        'email': user.email,
        'birth_date': user.birth_date,
        'gender': user.gender,
        'avatar': user.avatar
    }), 200

@profile_bp.route('', methods=['PUT'])
def update_profile():
    """Update the authenticated user's profile."""
    user_info = session.get('user')
    if not user_info:
        return jsonify({'message': 'Unauthorized'}), 401

    user_id = user_info.get('id') or user_info.get('sub')
    user = UserProfile.query.get(user_id)
    if not user:
        return jsonify({'message': 'User not found'}), 404

    data = request.get_json() or {}
    user.name = data.get('name', user.name)
    user.email= data.get('email', user.email)
    user.birthi_date = data.get('birth_date', user.birth_date)
    user.gender = data.get('gender', user.gender)
    user.avatar = data.get('avatar', user.avatar)

    db.session.commit()
    return jsonify({'message': 'Profile updated successfully'}), 200
