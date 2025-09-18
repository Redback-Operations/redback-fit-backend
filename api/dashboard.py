import sys

from flask import Blueprint, jsonify
from models.user import db, UserProfile
from flask_cors import CORS
from datetime import datetime, timezone
from flask import request, jsonify, g
from firebase_admin import auth as admin_auth

from models.body_insight import BodyInsight
from models.activity import Activity
# Create the Blueprint for dashboard
dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/api/dashboard')

# protect dashboard route with Firebase ID token
@dashboard_bp.before_request
def dashboard_auth_gate():
    if request.method == "OPTIONS":
        return None
    header = request.headers.get("Authorization", "")
    if not header.startswith("Bearer "):
        return jsonify({"error": "Unauthorized"}), 401
    token = header.split(" ", 1)[1].strip()
    try:
        g.firebase_user = admin_auth.verify_id_token(token)
    except Exception:
        return jsonify({"error": "Unauthorized"}), 401




# Dashboard Endpoints #

# Endpoint to get the user's dashboard data, including profile info and metrics like VO2 Max
@dashboard_bp.route('', methods=['GET'])
def get_dashboard_data():
    user_id = 1  # Temporary fixed user
    user = UserProfile.query.filter_by(id=user_id).first()

    if not user:
        return jsonify({'message': 'User not found'}), 404

    # Find latest activity for this user
    latest_activity = (
        Activity.query
        .filter_by(user_id=user_id)
        .order_by(Activity.begin_time.desc())
        .first()
    )

    # Default vo2_max if no data found
    vo2_max = None

    if latest_activity:
        body_insight = BodyInsight.query.filter_by(activity_id=latest_activity.id).first()
        if body_insight:
            vo2_max = body_insight.vo2_max

    current_utc_time = datetime.now(timezone.utc)

    # DEBUG LOGGING
    print(f"User fetched: {user.as_dict()}", file=sys.stderr)
    print(f"VO2 Max fetched: {vo2_max}", file=sys.stderr)

    return jsonify({
        'name': user.name,
        'account': user.account,
        'birthDate': user.birthDate,
        'gender': user.gender,
        'avatar': user.avatar,
        'lastLogin': current_utc_time.isoformat(),
        'vo2Max': vo2_max  # Can be None if no data found
    })