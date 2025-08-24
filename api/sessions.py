from flask import Blueprint, jsonify
from models.activity import Activity
from models import db
from datetime import datetime

sessions_bp = Blueprint('sessions_api', __name__)

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
