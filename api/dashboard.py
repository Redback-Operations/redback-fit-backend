# will require edits to the frontend to ensure user data persists:
                            # src/components/DashboardLanding/DashboardLanding.tsx
                            # src/components/ProfileAvatar/ProfileAvatar.tsx
# alternatively, find edited files on planner board > 'Add Endpoint for the Dashboard'.
import sys

from flask import Blueprint, jsonify, request
from models import db, UserProfile
from flask_cors import CORS
from datetime import datetime, timezone
from flask_login import login_required, current_user
from extensions import csrf

# Create the Blueprint for dashboard
dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/api/dashboard')

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


def _is_intlike(x):
    try:
        int(x)
        return True
    except Exception:
        return False
    
@dashboard_bp.route('/activity', methods=['POST'])
@login_required
@csrf.exempt 
def post_activity():
    body = request.get_json(silent=True) or {}

    # required field
    date = body.get("date")
    if not isinstance(date, str):
        return jsonify({"error": "date is required (YYYY-MM-DD)"}), 400

    # optional numeric fields; default to 0 if missing but validate type if present
    numeric_fields = [
        "steps",
        "minutes_running",
        "minutes_cycling",
        "minutes_swimming",
        "minutes_exercise",
        "calories",
    ]
    out = {"date": date, "user_id": getattr(current_user, "id", None)}
    for f in numeric_fields:
        v = body.get(f, 0)
        if v != 0 and not _is_intlike(v):
            return jsonify({"error": f"{f} must be an integer"}), 400
        out[f] = int(v)

    return jsonify(out), 201
