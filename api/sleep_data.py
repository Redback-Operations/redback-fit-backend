# /api/sleep_data.py
from flask import Blueprint, request, jsonify
from models.sleep_data import SleepData
from models import db
from datetime import datetime

sleep_data_bp = Blueprint('sleep_data', __name__, url_prefix='/api/sleep_data')

# For now, mimic authenticated user
def get_current_user_id():
    return 1  # Replace with token/session in future


# POST new sleep record
@sleep_data_bp.route('', methods=['POST'])
def add_sleep_data():
    data = request.get_json()
    user_id = get_current_user_id()

    if not data.get('date') or not data.get('duration_minutes'):
        return jsonify({"error": "Missing required fields: date, duration_minutes"}), 400

    try:
        sleep_date = datetime.strptime(data['date'], "%Y-%m-%d").date()
    except ValueError:
        return jsonify({"error": "Invalid date format. Use YYYY-MM-DD"}), 400

    sleep_entry = SleepData(
        user_id=user_id,
        date=sleep_date,
        duration_minutes=data['duration_minutes'],
        sleep_score=data.get('sleep_score')
    )

    db.session.add(sleep_entry)
    db.session.commit()

    return jsonify(sleep_entry.as_dict()), 201


# GET all sleep records for the current user
@sleep_data_bp.route('', methods=['GET'])
def get_all_sleep():
    user_id = get_current_user_id()
    entries = SleepData.query.filter_by(user_id=user_id).order_by(SleepData.date.desc()).all()
    return jsonify([e.as_dict() for e in entries]), 200


# GET sleep record by ID (scoped to current user)
@sleep_data_bp.route('/<int:id>', methods=['GET'])
def get_sleep_by_id(id):
    user_id = get_current_user_id()
    entry = SleepData.query.filter_by(id=id, user_id=user_id).first()
    if not entry:
        return jsonify({"error": "Sleep record not found for this user"}), 404
    return jsonify(entry.as_dict()), 200
