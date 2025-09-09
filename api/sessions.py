from flask import Blueprint, jsonify
from models.activity import Activity
from models.body_insight import BodyInsight
from models.sleep_data import SleepData
from models import db
from datetime import datetime

sessions_bp = Blueprint('sessions_api', __name__)

# Get all sessions summary for table.
@sessions_bp.route('', methods=['GET'])
def get_sessions():
    # replace with authenticated user ID from session/token
    user_id = 1  

    activities = Activity.query.filter_by(user_id=user_id).order_by(Activity.begin_time.desc()).all()
    
    sessions = []
    for a in activities:
        sessions.append({
            'session_id': a.id,
            'coach': a.coach if a.coach else 'N/A',
            'duration': a.duration,
            'date': a.begin_time.strftime("%Y/%m/%d"),
            'training': a.activity_type
        })
    
    return jsonify(sessions), 200



# Get activity, body insight and sleep data details for a single session
@sessions_bp.route('/<int:session_id>/details', methods=['GET'])
def get_session_details(session_id):
    # Fetch the activity
    activity = Activity.query.get(session_id)
    if not activity:
        return jsonify({"error": "Session not found"}), 404

    # Fetch the linked BodyInsight, if it exists
    body_insight = BodyInsight.query.filter_by(activity_id=activity.id).first()

    # Fetch sleep data for the same date as the activity
    sleep_entry = SleepData.query.filter_by(
        user_id=activity.user_id,
        date=activity.begin_time.date()
    ).first()

    response = {
        "activity": activity.as_dict(),
        "body_insight": body_insight.as_dict() if body_insight else None,
        "sleep_data": sleep_entry.as_dict() if sleep_entry else None
    }

    return jsonify(response), 200