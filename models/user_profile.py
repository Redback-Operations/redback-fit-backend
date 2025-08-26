from models import db

class UserProfile(db.Model):
    __tablename__ = 'user_profile'

    id = db.Column(db.Integer, primary_key=True)
    # Link to UserCredential 
    user_id = db.Column(db.Integer, db.ForeignKey("user_credential.id"), nullable=False, unique=True)
    user = db.relationship("UserCredential", back_populates="profile")

    name = db.Column(db.String(100), nullable=False)
    account = db.Column(db.String(100), unique=True, nullable=False)
    birthDate = db.Column(db.String(10), nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    avatar = db.Column(db.String(200), nullable=True)


    def as_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "account": self.account,
            "birthDate": self.birthDate,
            "gender": self.gender,
            "avatar": self.avatar
        }
