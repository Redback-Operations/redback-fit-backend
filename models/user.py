from models import db
from datetime import datetime, timezone

class UserProfile(db.Model):
    __tablename__ = 'user_profile'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    account = db.Column(db.String(100), unique=True, nullable=False)
    birthDate = db.Column(db.String(10), nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    avatar = db.Column(db.String(200), nullable=True)
    last_synced = db.Column(db.DateTime, nullable=True)


    def as_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "account": self.account,
            "birthDate": self.birthDate,
            "gender": self.gender,
            "avatar": self.avatar,
            "last_sync": self.last_synced.isoformat() if self.last_synced else None
        }