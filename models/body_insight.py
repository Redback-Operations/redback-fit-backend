from models import db

class BodyInsight(db.Model):
    __tablename__ = 'body_insight'

    id = db.Column(db.Integer, primary_key=True)
    activity_id = db.Column(db.Integer, db.ForeignKey('activity.id'), nullable=False, unique=True)

    activity = db.relationship(
        'Activity',
        backref=db.backref('body_insight', uselist=False)  # Makes SQLAlchemy treat it as one-to-one
    )
    
    # Performance Metrics
    vo2_max = db.Column(db.Float, nullable=True)
    lactate_threshold = db.Column(db.Float, nullable=True)
    race_time_prediction = db.Column(db.String(100), nullable=True)
    real_time_stamina = db.Column(db.Float, nullable=True)
    functional_threshold_power = db.Column(db.Float, nullable=True)
    power_to_weight_ratio = db.Column(db.Float, nullable=True)
    critical_power = db.Column(db.Float, nullable=True)
    threshold_heart_rate = db.Column(db.Integer, nullable=True)
    performance_index = db.Column(db.Float, nullable=True)
    fatigue_index = db.Column(db.Float, nullable=True)

    # Peak Power for durations
    peak_power_5s = db.Column(db.Float, nullable=True)
    peak_power_1min = db.Column(db.Float, nullable=True)
    peak_power_5min = db.Column(db.Float, nullable=True)
    peak_power_20min = db.Column(db.Float, nullable=True)

    # Acclimation and Readiness
    heat_acclimation = db.Column(db.Float, nullable=True)
    altitude_acclimation = db.Column(db.Float, nullable=True)
    training_readiness = db.Column(db.Float, nullable=True)
    endurance_score = db.Column(db.Float, nullable=True)

    # Health Metrics
    blood_oxygen = db.Column(db.Float, nullable=True)
    def as_dict(self):
        return {
            "id": self.id,
            "activity_id": self.activity_id,
            "vo2_max": self.vo2_max,
            "lactate_threshold": self.lactate_threshold,
            "race_time_prediction": self.race_time_prediction,
            "real_time_stamina": self.real_time_stamina,
            "functional_threshold_power": self.functional_threshold_power,
            "power_to_weight_ratio": self.power_to_weight_ratio,
            "critical_power": self.critical_power,
            "peak_power": {
                "5s": self.peak_power_5s,
                "1min": self.peak_power_1min,
                "5min": self.peak_power_5min,
                "20min": self.peak_power_20min
            },
            "threshold_heart_rate": self.threshold_heart_rate,
            "performance_index": self.performance_index,
            "fatigue_index": self.fatigue_index,
            "heat_acclimation": self.heat_acclimation,
            "altitude_acclimation": self.altitude_acclimation,
            "training_readiness": self.training_readiness,
            "endurance_score": self.endurance_score,
            #
            "blood_oxygen": self.blood_oxygen
        }
