#!/usr/bin/env python3
import os, sys
from dotenv import load_dotenv

# Ensure project root is on the import path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Load environment variables from .env
load_dotenv()

from app import create_app
from app.extensions import db
from app.models import UserProfile, Goal
from datetime import date


def main():
    # Initialize Flask app and push context
    app = create_app()
    with app.app_context():
        #  Drop all existing tables to avoid stale schemas
        db.drop_all()

        #  Create all tables based on current SQLAlchemy models
        db.create_all()

        #  Seed a default user if not already present
        UserProfile.add_default_user()

        #  Optionally seed a sample goal for the default user
        default_user = UserProfile.query.filter_by(
            account='redback.operations@deakin.edu.au'
        ).first()
        if default_user and default_user.goals.count() == 0:
            sample_goal = Goal(
                user_id=default_user.id,
                start_date=date.today(),
                end_date=date.today(),
                steps=10000,
                minutes_running=30,
                minutes_cycling=0,
                minutes_swimming=0,
                minutes_exercise=45,
                calories=500
            )
            db.session.add(sample_goal)
            db.session.commit()

        print("Dev database reset and created with schema v", 
              app.config['SQLALCHEMY_DATABASE_URI'])

if __name__ == '__main__':
    main()