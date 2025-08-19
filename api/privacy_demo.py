from flask import Blueprint, request, jsonify
from utils.privacy import (
    stable_hash, initials, pseudonym,
    birth_year_from_iso, age_bucket_from_year
)

# Create a Blueprint for privacy demo that can be plugged into the main Flask app
bp = Blueprint('privacy_demo', __name__, url_prefix = "/debug")

@bp.post("/anonymize")

def anonymize_demo():
    data = request.get_json(silent = True) or {}
    email = data.get("email")
    name = data.get("name")
    dob = data.get("dob")

    by = birth_year_from_iso(dob)

    return jsonify({
        "email_hash": stable_hash(email) if email else None,
        "name_initials": initials(name),
        "pseudonymId": pseudonym("http://redback.fit/user", email or name or "temp"),
        "birth_year": by,
        "age_bucket": age_bucket_from_year(by)
    })
