# /api/profile.py
from flask import Blueprint, jsonify, request
from models.user import db, UserProfile
from flask_cors import CORS

api = Blueprint('profile_api', __name__)


# Profile Endpoints #

# These routes are used by the frontend to fetch/update the user profile.
# Requires frontend request structure from ProfilePage.tsx

@api.route('', methods=['GET'])
def get_profile():
    # In future develpment get the user_id from a session or token 
    user_id = 1  # Replace with authenticated user ID
    user = UserProfile.query.filter_by(id=user_id).first()

    if user:
        return jsonify({
            'name': user.name,
            'account': user.account,
            'birthDate': user.birthDate,
            'gender': user.gender,
            'avatar': user.avatar
        })
    return jsonify({'message': 'User not found'}), 404


@api.route('', methods=['POST'])
def update_profile():
    data = request.get_json()  # Get the JSON data sent from the frontend

    # In future develpment get the user_id from a session or token
    user_id = 1  # Replace with authenticated user ID
    user = UserProfile.query.filter_by(id=user_id).first()

    if not user:
        return jsonify({'message': 'User not found'}), 404

    # Update the user's profile with the new data
    user.name = data['name']
    user.account = data['account']
    user.birthDate = data['birthDate']
    user.gender = data['gender']
    user.avatar = data.get('avatar', user.avatar)  # Only update avatar if provided

    db.session.commit()  # Save changes to the database

    return jsonify({'message': 'Profile updated successfully'}), 200
