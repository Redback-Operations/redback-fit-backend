from models import db
from datetime import datetime


class Goal(db.Model):
    __tablename__ = 'goals'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)  # Link to OAuth user later
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    steps = db.Column(db.Integer, default=0)
    minutes_running = db.Column(db.Integer, default=0)
    minutes_cycling = db.Column(db.Integer, default=0)
    minutes_swimming = db.Column(db.Integer, default=0)
    minutes_exercise = db.Column(db.Integer, default=0)
    calories = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def as_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "start_date": self.start_date.isoformat(),
            "end_date": self.end_date.isoformat(),
            "steps": self.steps,
            "minutes_running": self.minutes_running,
            "minutes_cycling": self.minutes_cycling,
            "minutes_swimming": self.minutes_swimming,
            "minutes_exercise": self.minutes_exercise,
            "calories": self.calories,
            "created_at": self.created_at.isoformat()
        }