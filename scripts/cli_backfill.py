import click
from flask.cli import with_appcontext
from models import db, UserCredential, UserProfile

@click.command("backfill-user-links")
@with_appcontext
def backfill_user_links():
    count = 0
    for p in UserProfile.query.filter(UserProfile.user_id.is_(None)).all():
        email = (p.account or "").lower().strip()
        if not email:
            continue
        u = UserCredential.query.filter_by(email=email).first()
        if not u:
            u = UserCredential(email=email, firebase_uid=f"pending:{email}")
            db.session.add(u)
            db.session.flush()
        p.user_id = u.id
        count += 1
    db.session.commit()
    click.echo(f"Linked/created {count} profiles.")