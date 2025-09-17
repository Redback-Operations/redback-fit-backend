from models import db
from models.user import UserProfile

def upsert_user_from_claims(claims):
    uid = claims["uid"]
    email = claims.get("email")

    u = UserProfile.query.filter_by(firebase_uid=uid).one_or_none()
    if not u and email:
        u = UserProfile.query.filter_by(account=email).one_or_none()
        if u:
            u.firebase_uid = uid

    if not u:
        u = UserProfile(firebase_uid=uid, account=email or "", name="New User",
                        birthDate="N/A", gender="N/A", avatar="")
        db.session.add(u)

    if email and u.account != email:
        u.account = email

    db.session.commit()
    return u
