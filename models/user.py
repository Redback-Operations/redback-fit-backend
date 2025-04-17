from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class UserProfile(db.Model):
    __tablename__ = 'user_profile'

    id = db.Column(db.Integer, primary_key=True)
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
#Adds the default user if not already in the database
def add_default_user():
    user = UserProfile.query.filter_by(account='redback.operations@deakin.edu.au').first()
    if not user:
        default_user = UserProfile(
            name='Austin Blaze',
            account='redback.operations@deakin.edu.au',
            birthDate='2000-01-01',
            gender='Male',
            avatar='src/assets/ProfilePic.png'
        )
        db.session.add(default_user)
        db.session.commit()
