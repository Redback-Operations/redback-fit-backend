from flask import Flask, jsonify, session, render_template, request, redirect, g
from flask_cors import CORS
from api.routes import api
from api.goals import goals_bp
from api.profile import api as profile_api
from api.dashboard import dashboard_bp
from api.body_insight import body_insight_bp
from api.activity import activity_bp
from api.sessions import sessions_bp
from api.sleep_data import sleep_data_bp
from api.sync import sync_bp
from models import db
from dotenv import load_dotenv
from services.firebase_admin import init_firebase_admin
from middlewares.auth import require_auth
from sqlalchemy import inspect, text
from models.user import UserProfile 
from services.user_link import upsert_user_from_claims
import os
import pyrebase


# Import scripts here 
from scripts.add_default_user import add_default_user

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
CORS(app, resources={r"/api/*": {
    "origins": ["http://localhost:5173", "https://app.redbackfit.com"],
    "allow_headers": ["Content-Type", "Authorization"],
    "methods": ["GET","POST","PUT","DELETE","OPTIONS"]
}})


# Firebase configuration
config = {
    'apiKey': os.getenv('FIREBASE_API_KEY'),
    'authDomain': os.getenv('FIREBASE_AUTH_DOMAIN'),
    'projectId': os.getenv('FIREBASE_PROJECT_ID'),
    'storageBucket': os.getenv('FIREBASE_STORAGE_BUCKET'),
    'messagingSenderId': os.getenv('FIREBASE_MESSAGING_SENDER_ID'),
    'appId': os.getenv('FIREBASE_APP_ID'),
    'measurementId': os.getenv('FIREBASE_MEASUREMENT_ID'),
    'databaseURL': os.getenv('FIREBASE_DATABASE_URL')
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()

# Flask config
app.secret_key = os.getenv("SECRET_KEY", "default_secret_key")
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL", "sqlite:///goals.db")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# DB init and create user
db.init_app(app)
with app.app_context():
    db.create_all()
    add_default_user()


    insp = inspect(db.engine)
    existing_cols = {c['name'] for c in insp.get_columns(UserProfile.__tablename__)}
    if 'firebase_uid' not in existing_cols:
        db.session.execute(text('ALTER TABLE user_profile ADD COLUMN firebase_uid VARCHAR(128)'))
        db.session.commit()

    
    db.session.execute(text('CREATE INDEX IF NOT EXISTS ix_user_profile_firebase_uid ON user_profile(firebase_uid)'))
    db.session.commit()
    
    

# Register Blueprints
app.register_blueprint(api, url_prefix='/api')
app.register_blueprint(goals_bp, url_prefix='/api/goals')
app.register_blueprint(dashboard_bp, url_prefix='/api/dashboard')
app.register_blueprint(profile_api, url_prefix='/api/profile')
app.register_blueprint(sync_bp, url_prefix='/api/synced')
app.register_blueprint(body_insight_bp, url_prefix='/api/body_insight')
app.register_blueprint(activity_bp, url_prefix='/api/activity')
app.register_blueprint(sessions_bp, url_prefix='/api/sessions')
app.register_blueprint(sleep_data_bp, url_prefix='/api/sleep_data')

# Main index route (login + welcome)
@app.route('/', methods=['GET', 'POST'])
def index():
    error = None
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        try:
            user = auth.sign_in_with_email_and_password(email, password)
            session['user'] = email
            return redirect('/home')
        except:
            error = "Login failed. Please check your credentials."

    return render_template('index.html', user=session.get('user'), error=error)

# Signup route
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    error = None
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        try:
            auth.create_user_with_email_and_password(email, password)
            session['user'] = email
            return redirect('/home')
        except Exception as e:
            error = "Signup failed. " + str(e).split("]")[-1].strip().strip('"')
    return render_template('signup.html', error=error)

# Logout route
@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/')

@app.route('/home')
def home():
    if 'user' in session:
        return render_template('home.html', user=session['user'])
    return redirect('/')

# Example API route
@app.route('/api/hello', methods=['GET'])
def hello():
    return jsonify({'message': 'Hello from Flask!'}), 200

@app.get("/api/me")
@require_auth
def me():
    claims = getattr(g, "firebase_user", {})
    user = upsert_user_from_claims(claims)
    return {
        "uid": claims.get("uid"),
        "email": claims.get("email"),
        "db_user_id": getattr(user, "id", None),
        "email_verified": claims.get("email_verified", False),
        "provider": (claims.get("firebase") or {}).get("sign_in_provider")
    }, 200


@app.errorhandler(401)
def _401(e):
    return jsonify(error="Unauthorized"), 401

@app.errorhandler(403)
def _403(e):
    return jsonify(error="Forbidden"), 403

@app.errorhandler(404)
def _404(e):
    return jsonify(error="Not found"), 404

@app.errorhandler(500)
def _500(e):
    return jsonify(error="Server error"), 500



#Entry point
if __name__ == '__main__':
    debug_mode = os.getenv("FLASK_DEBUG", "False").lower() == "true"
    app.run(debug=debug_mode, port=int(os.getenv("PORT", 5000)))



