# /api/profile.py
from flask import Blueprint, jsonify, request
from models.user import db, UserProfile

from utils.privacy import(
    stable_hash, initials, pseudonym, 
    birth_year_from_iso, age_bucket_from_year
)

api = Blueprint('profile_api', __name__)

def anonymize_user_record(u):
    """Build an anonymized profile payload from a UserProfile row.
    Hides raw PII (name/email/DOB) and exposes safe equivalents."""

    if not u:
        return None

    # Choose a stable raw key for pseudonymization
    raw_key = getattr(u, "email", None) or getattr(u, "name", None) or str(getattr(u, "id", ""))

    # Your model uses 'birthDate' (ISO string) rather than 'dob'
    by = birth_year_from_iso(getattr(u, "birthDate", None))

    return {
        "id": getattr(u, "id", None),  # safe to keep if your API expects it
        "pseudoId":     pseudonym("https://redback.fit/user", raw_key),
        "nameInitials": initials(getattr(u, "name", None)),
        "emailHash":    stable_hash(getattr(u, "email", None)),
        "ageBucket":    age_bucket_from_year(by),

        # keep non-PII fields you were already returning
        "account": getattr(u, "account", None),
        "gender":  getattr(u, "gender", None),
        "avatar":  getattr(u, "avatar", None),
    }

# Profile Endpoints #

# These routes are used by the frontend to fetch/update the user profile.
# Requires frontend request structure from ProfilePage.tsx

@api.route('', methods=['GET'])
def get_profile():
    # In future develpment get the user_id from a session or token 
    user_id = 1  # Replace with authenticated user ID
    user = UserProfile.query.filter_by(id=user_id).first()

    if not user:
        return jsonify({'message': 'User not found'}), 404

    return jsonify(anonymize_user_record(user)), 200


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