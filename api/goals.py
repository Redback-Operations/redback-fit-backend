from flask import Blueprint, request, jsonify
from models.goal import db, Goal  # Correctly import db and Goal
from datetime import datetime
from sqlalchemy import and_, or_

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
def update_goal(goal_id):
    data = request.get_json()

    # Retrieve the goal with the specified goal_id
    goal = Goal.query.get_or_404(goal_id)

    # Loop through all the fields to update and check if they exist in the data
    for field in ['start_date', 'end_date', 'steps', 'minutes_running', 'minutes_cycling',
                  'minutes_swimming', 'minutes_exercise', 'calories']:
        if field in data:
            # If it's a date field, convert it
            if field in ['start_date', 'end_date']:
                setattr(goal, field, datetime.strptime(data[field], '%Y-%m-%d').date())
            else:
                setattr(goal, field, data[field])

    # Commit the changes to the database
    db.session.commit()
    
    # Return the updated goal as a response
    return jsonify(goal.as_dict())

# Delete Goal
@goals_bp.route('/<int:goal_id>', methods=['DELETE'])
def delete_goal(goal_id):
    # Retrieve the goal by goal_id
    goal = Goal.query.get_or_404(goal_id)
    
    # Delete the goal from the session
    db.session.delete(goal)
    db.session.commit()
    
    # Return a 204 status code (no content)
    return '', 204

#adding new endpoint (/similar)

@goals_bp.route('/similar', methods=['POST'])
def similar_goals():
    data = request.get_json()

    required_fields = [
        'steps', 'minutes_running', 'minutes_cycling',
        'minutes_swimming', 'minutes_exercise', 'calories'
    ]

    # Validate input
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"{field} is required"}), 400

    # Set tolerance for matching (10%)
    tolerance = 0.1  

    # Define filters to find similar goals within ±10% tolerance
    filters = [
        Goal.steps.between(data['steps'] * (1 - tolerance), data['steps'] * (1 + tolerance)),
        Goal.minutes_running.between(data['minutes_running'] * (1 - tolerance), data['minutes_running'] * (1 + tolerance)),
        Goal.minutes_cycling.between(data['minutes_cycling'] * (1 - tolerance), data['minutes_cycling'] * (1 + tolerance)),
        Goal.minutes_swimming.between(data['minutes_swimming'] * (1 - tolerance), data['minutes_swimming'] * (1 + tolerance)),
        Goal.minutes_exercise.between(data['minutes_exercise'] * (1 - tolerance), data['minutes_exercise'] * (1 + tolerance)),
        Goal.calories.between(data['calories'] * (1 - tolerance), data['calories'] * (1 + tolerance)),
    ]

    similar_goals = Goal.query.filter(
        and_(*filters)
    ).order_by(Goal.created_at.desc()).limit(10).all()

    return jsonify([g.as_dict() for g in similar_goals]), 200
