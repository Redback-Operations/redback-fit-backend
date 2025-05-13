from models import db
from models.user import UserProfile

def add_default_user():
    # Only add a default user if the user_profile table is completely empty
    if UserProfile.query.first() is None:
        default_user = UserProfile(
            name='Austin Blaze',
            account='redback.operations@deakin.edu.au',
            birthDate='2000-01-01',
            gender='Male',
            avatar='src/assets/ProfilePic.png'
        )
        db.session.add(default_user)
        db.session.commit()
        print("Default user added because user table was empty.")
    else:
        print("User table is not empty. Default user not added.")
