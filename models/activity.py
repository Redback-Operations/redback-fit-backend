from models import db
from datetime import datetime

class Activity(db.Model):
    __tablename__ = 'activity'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user_profile.id'), nullable=False)

    # Summary data
    begin_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    activity_type = db.Column(db.String(50), nullable=False)
    coach = db.Column(db.String(100), nullable=True)
    average_speed = db.Column(db.Float, nullable=False)
    max_speed = db.Column(db.Float, nullable=False)
    average_heart_rate = db.Column(db.Integer, nullable=False)
    max_heart_rate = db.Column(db.Integer, nullable=False)
    calories = db.Column(db.Float, nullable=False)
    duration = db.Column(db.String(20), nullable=False) 
    moving_duration = db.Column(db.String(20), nullable=False)
    average_moving_speed = db.Column(db.Float, nullable=False)
    distance = db.Column(db.Float, nullable=False)
    elevation_gain = db.Column(db.Float, nullable=False)
    elevation_loss = db.Column(db.Float, nullable=False)
    max_elevation = db.Column(db.Float, nullable=False)
    min_elevation = db.Column(db.Float, nullable=False)
    


    time_series = db.relationship('ActivityTimeSeries', backref='activity', cascade="all, delete-orphan")

    def as_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "begin_time": self.begin_time.isoformat(),
            "end_time": self.end_time.isoformat(),
            "activity_type": self.activity_type,
            "coach": self.coach,
            "average_speed": self.average_speed,
            "max_speed": self.max_speed,
            "average_heart_rate": self.average_heart_rate,
            "max_heart_rate": self.max_heart_rate,
            "calories": self.calories,
            "duration": self.duration,
            "moving_duration": self.moving_duration,
            "average_moving_speed": self.average_moving_speed,
            "distance": self.distance,
            "elevation_gain": self.elevation_gain,
            "elevation_loss": self.elevation_loss,
            "max_elevation": self.max_elevation,
            "min_elevation": self.min_elevation,
            "time_series": [ts.as_dict() for ts in self.time_series]
        }


class ActivityTimeSeries(db.Model):
    __tablename__ = 'activity_time_series'

    id = db.Column(db.Integer, primary_key=True)
    activity_id = db.Column(db.Integer, db.ForeignKey('activity.id'), nullable=False)

    timestamp = db.Column(db.DateTime, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    elevation = db.Column(db.Float, nullable=False)
    heart_rate = db.Column(db.Integer, nullable=False)
    cadence = db.Column(db.Float, nullable=False)

    def as_dict(self):
        return {
            "timestamp": self.timestamp.isoformat(),
            "longitude": self.longitude,
            "latitude": self.latitude,
            "elevation": self.elevation,
            "heart_rate": self.heart_rate,
            "cadence": self.cadence
        }
