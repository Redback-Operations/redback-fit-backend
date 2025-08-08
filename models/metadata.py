from models import db
from datetime import datetime

class ActivityMetadata(db.Model):
    __tablename__ = 'activity_metadata'

    id = db.Column(db.Integer, primary_key=True)
    datetime = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user_profile.id'), nullable=False)
    activity_id = db.Column(db.Integer, db.ForeignKey('activity.id'), unique=True, nullable=False)
    activity_name = db.Column(db.String(100), nullable=False)
    activity_type = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=True)

    temperature = db.Column(db.Float, nullable=True)
    humidity = db.Column(db.Float, nullable=True)
    wind_speed = db.Column(db.Float, nullable=True)
    wind_direction = db.Column(db.String(20), nullable=True)

    begin_longitude = db.Column(db.Float, nullable=True)
    end_longitude = db.Column(db.Float, nullable=True)
    begin_latitude = db.Column(db.Float, nullable=True)
    end_latitude = db.Column(db.Float, nullable=True)

    condition = db.Column(db.String(50), nullable=True)
    rainfall = db.Column(db.String(50), nullable=True)

    def as_dict(self):
        return {
            "id": self.id,
            "datetime": self.datetime.isoformat(),
            "user_id": self.user_id,
            "activity_id": self.activity_id,
            "activity_name": self.activity_name,
            "activity_type": self.activity_type,
            "description": self.description,
            "temperature": self.temperature,
            "humidity": self.humidity,
            "wind_speed": self.wind_speed,
            "wind_direction": self.wind_direction,
            "begin_longitude": self.begin_longitude,
            "end_longitude": self.end_longitude,
            "begin_latitude": self.begin_latitude,
            "end_latitude": self.end_latitude,
            "condition": self.condition,
            "rainfall": self.rainfall
        }
