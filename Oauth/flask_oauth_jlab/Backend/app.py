import os
from flask import Flask, jsonify, redirect, url_for
from flask_dance.contrib.google import make_google_blueprint, google
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from flask_cors import CORS
from dotenv import load_dotenv

# 🔐 Load environment variables from .env file
load_dotenv()

# ✅ Allow HTTP for local development (OAuth)
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

# ✅ Initialize Flask app
app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")

# ✅ Fix cookie/session behavior for local dev
app.config.update(
    SESSION_COOKIE_SAMESITE="Lax",     # Allow cookie to be sent across ports (5000 → 5500)
    SESSION_COOKIE_SECURE=False        # Don't require HTTPS for dev
)

# ✅ CORS setup to allow cross-origin cookies
CORS(app, supports_credentials=True)

# ✅ Google OAuth configuration from .env
app.config["GOOGLE_OAUTH_CLIENT_ID"] = os.getenv("GOOGLE_OAUTH_CLIENT_ID")
app.config["GOOGLE_OAUTH_CLIENT_SECRET"] = os.getenv("GOOGLE_OAUTH_CLIENT_SECRET")

# ✅ Register Google OAuth blueprint
google_bp = make_google_blueprint(
    scope=["openid", "https://www.googleapis.com/auth/userinfo.email"],
    redirect_url="/api/login/callback"
)
app.register_blueprint(google_bp, url_prefix="/api/login")

# ✅ Flask-Login setup
login_manager = LoginManager(app)
users = {}  # Temporary in-memory storage

class User(UserMixin):
    def __init__(self, id_, email):
        self.id = id_
        self.email = email

    def get_id(self):
        return self.id

@login_manager.user_loader
def load_user(user_id):
    return users.get(user_id)

# ✅ Route to initiate login
@app.route("/api/login")
def login():
    return redirect(url_for("google.login"))

# ✅ OAuth callback route
@app.route("/api/login/callback")
def callback():
    if not google.authorized:
        return redirect(url_for("google.login"))
    
    resp = google.get("/oauth2/v2/userinfo")
    if not resp.ok:
        return "Failed to fetch user info", 400

    info = resp.json()
    user = User(info["id"], info["email"])
    users[user.id] = user
    login_user(user)

    # ✅ Redirect back to frontend after login
    return redirect("http://localhost:5500/index.html")

# ✅ Authenticated user info endpoint
@app.route("/api/user")
def user_info():
    if current_user.is_authenticated:
        return jsonify({"email": current_user.email})
    return jsonify({"error": "not logged in"}), 401

# ✅ Logout endpoint
@app.route("/api/logout")
@login_required
def logout():
    logout_user()
    return jsonify({"message": "Logged out"})

# ✅ Start app on localhost:5000
if __name__ == "__main__":
    import os
    debug_mode = os.getenv("FLASK_DEBUG", "False").lower() == "true"
    app.run(host="localhost", port=5000, debug=debug_mode)

