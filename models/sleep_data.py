from models import db
from datetime import date

class SleepData(db.Model):
    __tablename__ = 'sleep_data'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user_profile.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)  # The night the sleep occurred
    duration_minutes = db.Column(db.Integer, nullable=False)   # Total sleep in minutes
    sleep_score = db.Column(db.Float, nullable=True)           # Optional sleep quality score (0-100)

    def as_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "date": self.date.isoformat(),
            "duration_minutes": self.duration_minutes,
            "hours": self.duration_minutes // 60,
            "minutes": self.duration_minutes % 60,
            "sleep_score": self.sleep_score
        }
