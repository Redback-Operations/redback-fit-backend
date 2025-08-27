from models import db, UserCredential, UserProfile
from flask.cli import with_appcontext
import click

def ensure_default_user():
    
    email = 'redback.operations@deakin.edu.au'
    name = 'Austin Blaze'
    password = 'Redback2024'
    birthDate = '2000-01-01'
    gender = "Male"
    avatar='src/assets/ProfilePic.png'

    # 1) Ensure credential exists
    user = UserCredential.query.filter_by(email=email.strip().lower()).first()
    if not user:
        user = UserCredential(email=email.strip().lower())
        user.set_password(password)
        db.session.add(user)
        db.session.flush()

    # 2) Ensure profile exists and is linked
    profile = UserProfile.query.filter_by(user_id=user.id).first()
    if not profile:
        profile = UserProfile(
            user_id=user.id,
            name=name,
            account=email,
            birthDate=birthDate,
            gender=gender,
            avatar=avatar,
        )
        db.session.add(profile)

    db.session.commit()
    return email
    

@click.command('add-default-user')
@with_appcontext
def add_default_user():
    email = ensure_default_user()
    click.echo(f"Default user ensured with email: {email}")
