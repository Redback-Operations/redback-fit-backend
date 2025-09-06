from models import db
import json

class ActivitySummary(db.Model):
    __tablename__ = 'activity_summary'

    id = db.Column(db.Integer, primary_key=True)
    activity_id = db.Column(db.Integer, db.ForeignKey('activity.id'), nullable=False)

    training_status = db.Column(db.String(50), nullable=True)
    body_battery = db.Column(db.Float, nullable=True)
    recovery_time = db.Column(db.Float, nullable=True)
    training_load = db.Column(db.Float, nullable=True)
    training_load_focus = db.Column(db.String(50), nullable=True)

    training_effect_aerobic = db.Column(db.Float, nullable=True)
    training_effect_anaerobic = db.Column(db.Float, nullable=True)

    hrv = db.Column(db.Text, nullable=True)  # Stored as JSON string
    hr_zones = db.Column(db.Text, nullable=True)  # Stored as JSON string

    hydration_status = db.Column(db.Float, nullable=True)
    epoc = db.Column(db.Float, nullable=True)

    def as_dict(self):
        return {
            "id": self.id,
            "activity_id": self.activity_id,
            "trainingStatus": self.training_status,
            "bodyBattery": self.body_battery,
            "recoveryTime": self.recovery_time,
            "trainingLoad": self.training_load,
            "trainingLoadFocus": self.training_load_focus,
            "trainingEffect": {
                "aerobic": self.training_effect_aerobic,
                "anaerobic": self.training_effect_anaerobic
            },
            "hrv": json.loads(self.hrv) if self.hrv else [],
            "hrZones": json.loads(self.hr_zones) if self.hr_zones else {},
            "hydrationStatus": self.hydration_status,
            "epoc": self.epoc
        }

    def set_hrv(self, hrv_data):
        """Accepts a list of HRV dicts and serialises them to JSON text."""
        self.hrv = json.dumps(hrv_data)

    def set_hr_zones(self, zones_data):
        """Accepts a dict of HR zones and serialises them to JSON text."""
        self.hr_zones = json.dumps(zones_data)
