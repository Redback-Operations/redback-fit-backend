from flask import Blueprint, jsonify, request
from app.extensions import token_required, db
from app.models import UserProfile
from datetime import datetime


profile_bp = Blueprint('profile', __name__, url_prefix='/api/profile')

@profile_bp.route('/', methods=['GET'])
@token_required
def get_profile(current_uid):
    """
    Fetch the authenticated user's profile. Returns defaults if none exists.
    """
    print("hit")
    profile = UserProfile.query.get(current_uid)
    if not profile:
        return jsonify({
            'uid': current_uid,
            'name': None,
            'email': None,
            'birth_date': None,
            'gender': None,
            'avatar': None
        }), 200

    return jsonify({
        'uid': profile.uid,
        'name': profile.name,
        'email': profile.email,
        'birth_date': profile.birth_date.isoformat() if profile.birth_date else None,
        'gender': profile.gender,
        'avatar': profile.avatar
    }), 200

@profile_bp.route('/', methods=['PUT'])
@token_required
def update_profile(current_uid):
    """
    Update or create the user's profile fields. Accepts JSON with any of:
    name, email, birth_date (YYYY-MM-DD), gender, avatar.
    """
    data = request.get_json() or {}
    profile = UserProfile.query.get(current_uid)
    if not profile:
        profile = UserProfile(uid=current_uid)
        db.session.add(profile)

    if 'name' in data:
        profile.name = data['name'].strip()
    if 'email' in data:
        profile.email = data['email'].lower().strip()
    if 'birth_date' in data:
        try:
            profile.birth_date = datetime.fromisoformat(data['birth_date']).date()
        except (ValueError, TypeError):
            return jsonify({'error': 'birth_date must be YYYY-MM-DD'}), 400
    if 'gender' in data:
        profile.gender = data['gender']
    if 'avatar' in data:
        profile.avatar = data['avatar'].strip()

    db.session.commit()
    return jsonify({
        'message': 'Profile updated successfully',
        'profile': {
            'uid': profile.uid,
            'name': profile.name,
            'email': profile.email,
            'birth_date': profile.birth_date.isoformat() if profile.birth_date else None,
            'gender': profile.gender,
            'avatar': profile.avatar
        }
    }), 200
