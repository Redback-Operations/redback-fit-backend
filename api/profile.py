# /api/profile.py
from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from extensions import db, csrf
import re
from models import db, UserProfile
from flask_cors import CORS

api = Blueprint('profile_api', __name__)


# Profile Endpoints #
DATE_RX = re.compile(r"^\d{4}-\d{2}-\d{2}$")
# These routes are used by the frontend to fetch/update the user profile.
# Requires frontend request structure from ProfilePage.tsx

@api.route('', methods=['GET'])
@login_required
def get_profile():
    # In future develpment get the user_id from a session or token 
    # user_id = 1  # Replace with authenticated user ID
    # user = UserProfile.query.filter_by(id=user_id).first()

    # if user:
    #     return jsonify({
    #         'name': user.name,
    #         'account': user.account,
    #         'birthDate': user.birthDate,
    #         'gender': user.gender,
    #         'avatar': user.avatar
    #     })
    # return jsonify({'message': 'User not found'}), 404

    profile = UserProfile.query.filter_by(user_id=current_user.id).first()
    if not profile:
        return jsonify({"message": "User not found"}), 404

    return jsonify({
        "user_id": profile.user_id,
        "name": profile.name,
        "account": profile.account,
        "birthDate": profile.birthDate,
        "gender": profile.gender,
    }), 200


@api.route('', methods=['POST'])
@login_required
@csrf.exempt 
def update_profile():
    data = request.get_json(silent=True) or {}  # Get the JSON data sent from the frontend
    errors = {}

    if "name" in data:
        if not isinstance(data["name"], str) or not data["name"].strip():
            errors["name"] = "must be a non-empty string"

    if "account" in data:
        if not isinstance(data["account"], str) or not data["account"].strip():
            errors["account"] = "must be a non-empty string"

    if "birthDate" in data:
        if not isinstance(data["birthDate"], str) or not DATE_RX.match(data["birthDate"]):
            errors["birthDate"] = "use YYYY-MM-DD"

    if "gender" in data:
        if not isinstance(data["gender"], str):
            errors["gender"] = "must be a string"

    if errors:
        return jsonify({"error": "validation_error", "fields": errors}), 422

    profile = UserProfile.query.filter_by(user_id=current_user.id).first()
    if not profile:
        return jsonify({"message": "User not found"}), 404

    # Only update fields that were provided
    if "name" in data:
        profile.name = data["name"].strip()
    if "account" in data:
        profile.account = data["account"].strip()
    if "birthDate" in data:
        profile.birthDate = data["birthDate"]
    if "gender" in data:
        profile.gender = data["gender"]

    db.session.commit()  # Save changes to the database

    return jsonify({'message': "Profile Updated Successfully", "user_id": profile.user_id}), 200