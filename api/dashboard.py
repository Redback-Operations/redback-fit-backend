# will require edits to the frontend to ensure user data persists:
                            # src/components/DashboardLanding/DashboardLanding.tsx
                            # src/components/ProfileAvatar/ProfileAvatar.tsx
# alternatively, find edited files on planner board > 'Add Endpoint for the Dashboard'.
import sys

from flask import Blueprint, jsonify
from models.user import db, UserProfile
from flask_cors import CORS
from datetime import datetime, timezone
from flask import request, jsonify, g
from firebase_admin import auth as admin_auth

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

    if user:
        current_utc_time = datetime.now(timezone.utc)
        vo2_max = 45 # placeholder for further implementation

        # DEBUG LOGGING
        print(f"User fetched: {user.as_dict()}", file=sys.stderr)

        return jsonify({
            'name': user.name,
            'account': user.account,
            'birthDate': user.birthDate,
            'gender': user.gender,
            'avatar': user.avatar,
            'lastLogin': current_utc_time.isoformat(),
            'vo2Max': vo2_max
        })

    return jsonify({'message': 'User not found'}), 404
