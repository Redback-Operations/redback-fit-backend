from models import db
from datetime import datetime

class Session(db.Model):
    __tablename__ = 'sessions'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    sport = db.Column(db.String(50), nullable=True)
    distance_km = db.Column(db.Float, default=0.0)
    avg_hr = db.Column(db.Integer, nullable=True)
    calories = db.Column(db.Integer, nullable=True)
    steps = db.Column(db.Integer, nullable=True)
    lat = db.Column(db.Float, nullable=False)
    lon = db.Column(db.Float, nullable=False)

    def as_dict(self):
        return {
            "id": self.id, "user_id": self.user_id,
            "start_time": self.start_time.isoformat(),
            "end_time": self.end_time.isoformat(),
            "sport": self.sport,
            "distance_km": self.distance_km,
            "avg_hr": self.avg_hr, "calories": self.calories, "steps": self.steps,
            "lat": self.lat, "lon": self.lon,
        }

class WeatherObservation(db.Model):
    __tablename__ = 'weather_observations'
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.Integer, db.ForeignKey('sessions.id'), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)
    temperature_c = db.Column(db.Float, nullable=True)
    apparent_temp_c = db.Column(db.Float, nullable=True)
    humidity_pct = db.Column(db.Float, nullable=True)
    precipitation_mm = db.Column(db.Float, nullable=True)
    wind_speed_ms = db.Column(db.Float, nullable=True)

    def as_dict(self):
        return {
            "timestamp": self.timestamp.isoformat(),
            "temperature_c": self.temperature_c,
            "apparent_temp_c": self.apparent_temp_c,
            "humidity_pct": self.humidity_pct,
            "precipitation_mm": self.precipitation_mm,
            "wind_speed_ms": self.wind_speed_ms,
        }
