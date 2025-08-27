from flask import Blueprint, request, jsonify
from models.activity import Activity, ActivityTimeSeries
from models import db
from datetime import datetime

activity_bp = Blueprint('activity', __name__, url_prefix='/api/activity')

@activity_bp.route('', methods=['POST'])
def create_activity():
    data = request.get_json()

    try:
        activity = Activity(
            user_id=data['user_id'],
            begin_time=datetime.fromisoformat(data['begin_time']),
            end_time=datetime.fromisoformat(data['end_time']),
            activity_type=data['activity_type'],
            coach=data.get('coach'),
            average_speed=data['average_speed'],
            max_speed=data['max_speed'],
            average_heart_rate=data['average_heart_rate'],
            max_heart_rate=data['max_heart_rate'],
            calories=data['calories'],
            duration=data['duration'],
            moving_duration=data['moving_duration'],
            average_moving_speed=data['average_moving_speed'],
            distance=data['distance'],
            elevation_gain=data['elevation_gain'],
            elevation_loss=data['elevation_loss'],
            max_elevation=data['max_elevation'],
            min_elevation=data['min_elevation']
        )

        # Handle optional time series data
        time_series_list = data.get('time_series', [])
        for point in time_series_list:
            ts = ActivityTimeSeries(
                timestamp=datetime.fromisoformat(point['timestamp']),
                longitude=point['longitude'],
                latitude=point['latitude'],
                elevation=point['elevation'],
                heart_rate=point['heart_rate'],
                cadence=point['cadence']
            )
            activity.time_series.append(ts)

        db.session.add(activity)
        db.session.commit()

        return jsonify({"message": "Activity and time series created", "activity_id": activity.id}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

    