from datetime import datetime
from app.extensions import db

class UserProfile(db.Model):
    __tablename__ = 'user_profile'

    id          = db.Column(db.Integer, primary_key=True)
    name        = db.Column(db.String(100), nullable=False)
    email       = db.Column(db.String(100), unique=True, nullable=False)
    birth_date  = db.Column(db.String(10), nullable=True)
    gender      = db.Column(db.String(10), nullable=True)
    avatar      = db.Column(db.String(200), nullable=True)

    # backref for goals
    goals       = db.relationship('Goal', back_populates='user', lazy='dynamic')

    def as_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "birth_date": self.birth_date,
            "gender": self.gender,
            "avatar": self.avatar,
        }
# Make add_default_user a @staticmethod (or move it out of the class) since it doesn’t take self.
    @staticmethod
    def add_default_user():
        """Seed a default user if none exists."""
        if not UserProfile.query.filter_by(email='redback.operations@deakin.edu.au').first():
            default = UserProfile(
                name='Austin Blaze',
                email='redback.operations@deakin.edu.au',
                birth_date='2000-01-01',
                gender='Male',
                avatar='src/assets/ProfilePic.png'
            )
            db.session.add(default)
            db.session.commit()


class Goal(db.Model):
    __tablename__ = 'goals'

    id               = db.Column(db.Integer, primary_key=True)
    user_id          = db.Column(db.Integer, db.ForeignKey('user_profile.id'), nullable=False)
    start_date       = db.Column(db.Date,  nullable=False)
    end_date         = db.Column(db.Date,  nullable=False)
    steps            = db.Column(db.Integer, default=0)
    minutes_running  = db.Column(db.Integer, default=0)
    minutes_cycling  = db.Column(db.Integer, default=0)
    minutes_swimming = db.Column(db.Integer, default=0)
    minutes_exercise = db.Column(db.Integer, default=0)
    calories         = db.Column(db.Integer, default=0)
    created_at       = db.Column(db.DateTime, default=datetime.utcnow)

    # link back to user
    user             = db.relationship('UserProfile', back_populates='goals')

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
            "created_at": self.created_at.isoformat(),
        }
