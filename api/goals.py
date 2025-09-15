from flask import Blueprint, request, jsonify
from models import db, Goal  # Correctly import db and Goal
from datetime import datetime
from flask_login import login_required, current_user

# Create the Blueprint for goals
goals_bp = Blueprint('goals', __name__, url_prefix='/api/goals')

# Create Goal
@goals_bp.route('/', methods=['POST'])
def create_goal():
    data = request.get_json()

    # Check if user_id exists in the request body
    if 'user_id' not in data:
        return jsonify({"error": "user_id is required"}), 400

    # Convert string dates to datetime.date objects
    start_date = datetime.strptime(data['start_date'], '%Y-%m-%d').date()
    end_date = datetime.strptime(data['end_date'], '%Y-%m-%d').date()

    # Create a new Goal object and populate it with data
    goal = Goal(
        user_id=data['user_id'],  # user_id now comes from the request body
        start_date=start_date,
        end_date=end_date,
        steps=data.get('steps', 0),
        minutes_running=data.get('minutes_running', 0),
        minutes_cycling=data.get('minutes_cycling', 0),
        minutes_swimming=data.get('minutes_swimming', 0),
        minutes_exercise=data.get('minutes_exercise', 0),
        calories=data.get('calories', 0)
    )

    # Add the goal to the session and commit to the database
    db.session.add(goal)
    db.session.commit()

    # Return the goal as a response with a 201 status
    return jsonify(goal.as_dict()), 201

@goals_bp.route('/<int:user_id>', methods=['POST'])
def create_goal_for_user(user_id):
    data = request.get_json()

    # Check if required fields are in the request
    if 'start_date' not in data or 'end_date' not in data:
        return jsonify({"error": "start_date and end_date are required"}), 400

    # Convert string dates to datetime.date objects
    start_date = datetime.strptime(data['start_date'], '%Y-%m-%d').date()
    end_date = datetime.strptime(data['end_date'], '%Y-%m-%d').date()

    # Create a new Goal object and associate it with the user_id
    goal = Goal(
        user_id=user_id,  # user_id passed from URL
        start_date=start_date,
        end_date=end_date,
        steps=data.get('steps', 0),
        minutes_running=data.get('minutes_running', 0),
        minutes_cycling=data.get('minutes_cycling', 0),
        minutes_swimming=data.get('minutes_swimming', 0),
        minutes_exercise=data.get('minutes_exercise', 0),
        calories=data.get('calories', 0)
    )
    
    # Add the goal to the session and commit to the database
    db.session.add(goal)
    db.session.commit()

    # Return the goal as a response with a 201 status
    return jsonify(goal.as_dict()), 201

# Get Goals for a user
@goals_bp.route('/<int:user_id>', methods=['GET'])
def get_user_goals(user_id):
    # Retrieve all goals for a specific user_id and order by the created_at date
    goals = Goal.query.filter_by(user_id=user_id).order_by(Goal.created_at.desc()).all()
    
    # Return the goals as a list of dictionaries
    return jsonify([g.as_dict() for g in goals])

# Update Goal
@goals_bp.route('/<int:goal_id>', methods=['PUT'])
@login_required
def update_goal(goal_id):
    data = request.get_json()

    # Retrieve the goal with the specified goal_id
    goal = Goal.query.get_or_404(goal_id)
    
    # Validation: dates must be ISO format (YYYY-MM-DD)
    if "start_date" in data:
        try:
            goal.start_date = datetime.strptime(data["start_date"], "%Y-%m-%d").date()
        except ValueError:
            return jsonify({"error": "Invalid start_date format, expected YYYY-MM-DD"}), 422

    if "end_date" in data:
        try:
            goal.end_date = datetime.strptime(data["end_date"], "%Y-%m-%d").date()
        except ValueError:
            return jsonify({"error": "Invalid end_date format, expected YYYY-MM-DD"}), 422

    # Loop through all the fields to update and check if they exist in the data
    for field in ['start_date', 'end_date', 'steps', 'minutes_running', 'minutes_cycling',
                  'minutes_swimming', 'minutes_exercise', 'calories']:
        if field in data:
            try:
                val = int(data[field])
            except (TypeError, ValueError):
                return jsonify({"error": f"{field} must be a number"}), 422
            if val < 0:
                return jsonify({"error": f"{field} cannot be negative value"}), 422
            setattr(goal, field, val)

    # Commit the changes to the database
    db.session.commit()
    
    # Return the updated goal as a response
    return jsonify(goal.as_dict()), 200

# Delete Goal
@goals_bp.route('/<int:goal_id>', methods=['DELETE'])
def delete_goal(goal_id):
    # Retrieve the goal by goal_id
    goal = Goal.query.get_or_404(goal_id)

    if goal.user_id != current_user.id:
        return jsonify({"error": "forbidden"}), 403
    
    # Delete the goal from the session
    db.session.delete(goal)
    db.session.commit()
    
    # Return a 204 status code (no content)
    return '', 204