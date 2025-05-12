from app import create_app
from app.extensions import db
from app.models import UserProfile, Goal

app = create_app()
with app.app_context():
    # List all users
    users = UserProfile.query.all()
    print([u.as_dict() for u in users])

    # List all goals
    goals = Goal.query.all()
    print([g.as_dict() for g in goals])
