# will require edits to the frontend to ensure user data persists:
                            # src/components/DashboardLanding/DashboardLanding.tsx
                            # src/components/ProfileAvatar/ProfileAvatar.tsx
# alternatively, find edited files on planner board > 'Add Endpoint for the Dashboard'.
import sys

from flask import Blueprint, jsonify
from models.user import db, UserProfile
from flask_cors import CORS
from datetime import datetime, timezone

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
        vo2_max = 45

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
