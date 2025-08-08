#Use to POST and Get data to/from body_insight table
from flask import Blueprint, request, jsonify
from models.body_insight import BodyInsight
from models import db
from models.activity import Activity

body_insight_bp = Blueprint('body_insight', __name__, url_prefix='/api/body_insight')

@body_insight_bp.route('', methods=['POST'])
def add_body_insight():
    data = request.get_json()

    # Require either activity_id or user_id
    activity_id = data.get('activity_id')
    user_id = data.get('user_id')

    if not activity_id:
        if not user_id:
            return jsonify({"error": "Missing required field 'activity_id' or 'user_id'"}), 400
        # Find latest activity for user_id
        latest_activity = (
            Activity.query
            .filter_by(user_id=user_id)
            .order_by(Activity.begin_time.desc())
            .first()
        )
        if not latest_activity:
            return jsonify({"error": "No activities found for user"}), 404
        activity_id = latest_activity.id

    try:
        insight = BodyInsight(
            activity_id=activity_id,
            vo2_max=data.get('vo2_max'),
            lactate_threshold=data.get('lactate_threshold'),
            race_time_prediction=data.get('race_time_prediction'),
            real_time_stamina=data.get('real_time_stamina'),
            functional_threshold_power=data.get('functional_threshold_power'),
            power_to_weight_ratio=data.get('power_to_weight_ratio'),
            critical_power=data.get('critical_power'),
            threshold_heart_rate=data.get('threshold_heart_rate'),
            performance_index=data.get('performance_index'),
            fatigue_index=data.get('fatigue_index'),
            peak_power_5s=data.get('peak_power_5s'),
            peak_power_1min=data.get('peak_power_1min'),
            peak_power_5min=data.get('peak_power_5min'),
            peak_power_20min=data.get('peak_power_20min'),
            heat_acclimation=data.get('heat_acclimation'),
            altitude_acclimation=data.get('altitude_acclimation'),
            training_readiness=data.get('training_readiness'),
            endurance_score=data.get('endurance_score'),
        )
        db.session.add(insight)
        db.session.commit()
        return jsonify({
            "message": "BodyInsight created",
            "id": insight.id,
            "activity_id": activity_id  # Return the actual activity_id linked
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500



@body_insight_bp.route('/<int:activity_id>', methods=['GET'])
def get_body_insight(activity_id):
    insight = BodyInsight.query.filter_by(activity_id=activity_id).first()
    if not insight:
        return jsonify({"error": "BodyInsight not found for this activity_id"}), 404
    return jsonify(insight.as_dict()), 200

@body_insight_bp.route('/latest', methods=['GET'])
def get_latest_body_insight():
    # Get latest BodyInsight entry by most recent activity
    latest = (
        BodyInsight.query
        .join(Activity, Activity.id == BodyInsight.activity_id)
        .order_by(Activity.begin_time.desc())
        .first()
    )
    
    if not latest:
        return jsonify({"error": "No body insight data found"}), 404

    return jsonify(latest.as_dict()), 200
