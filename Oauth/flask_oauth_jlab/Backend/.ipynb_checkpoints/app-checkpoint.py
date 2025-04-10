import os
from flask import Flask, jsonify, redirect, url_for
from flask_dance.contrib.google import make_google_blueprint, google
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from flask_cors import CORS

# ✅ Allow HTTP for local development
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

app = Flask(__name__)
app.secret_key = "test123"  # 🔐 Replace with a secure random secret in production
CORS(app, supports_credentials=True)

# ✅ Replace with your actual Google OAuth credentials
app.config["GOOGLE_OAUTH_CLIENT_ID"] = "1062579474786-6amk0lplnd08foeridr2jhtrikpqnv9k.apps.googleusercontent.com"
app.config["GOOGLE_OAUTH_CLIENT_SECRET"] = "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"

# ✅ Set up Google OAuth blueprint
google_bp = make_google_blueprint(
    scope=["openid", "https://www.googleapis.com/auth/userinfo.email"],
    redirect_url="/api/login/callback"
)
app.register_blueprint(google_bp, url_prefix="/api/login")

# ✅ Flask-Login setup
login_manager = LoginManager(app)
users = {}  # In-memory user storage

class User(UserMixin):
    def __init__(self, id_, email):
        self.id = id_
        self.email = email

    def get_id(self):
        return self.id

@login_manager.user_loader
def load_user(user_id):
    return users.get(user_id)

# ✅ Entry point to initiate login
@app.route("/api/login")
def login():
    return redirect(url_for("google.login"))

# ✅ Callback route after successful Google login
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

    # ✅ Redirect to your frontend hosted locally (served with python -m http.server 5500)
    return redirect("http://localhost:5500/index.html")

# ✅ Endpoint to get user info
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

# ✅ Start the Flask app
if __name__ == "__main__":
    app.run(port=5000, debug=True)
