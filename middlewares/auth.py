from functools import wraps
from flask import request, jsonify, g
from firebase_admin import auth as admin_auth

def require_auth(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        auth_header = request.headers.get("Authorization", "")
        if not auth_header.startswith("Bearer "):
            return jsonify({"error": "Unauthorized"}), 401
        token = auth_header.split(" ", 1)[1].strip()
        try:
            g.firebase_user = admin_auth.verify_id_token(token)
        except Exception:
            return jsonify({"error": "Unauthorized"}), 401
        return fn(*args, **kwargs)
    return wrapper

