from flask import Flask, jsonify, session, render_template, request, redirect
from flask_migrate import Migrate
from flask_cors import CORS
from api.routes import api
from api.goals import goals_bp
from api.profile import api as profile_api
from api.dashboard import dashboard_bp
<<<<<<< HEAD
=======
from api.body_insight import body_insight_bp
from api.activity import activity_bp
>>>>>>> upstream/main
from api.sessions import sessions_bp
from models import db
from dotenv import load_dotenv
from api.sync import sync_bp
from logging.handlers import RotatingFileHandler
import logging
import os
import pyrebase

# Import scripts here 
from scripts.add_default_user import add_default_user

# ensure a folder for logs exists
os.makedirs('logs', exist_ok=True)

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "http://localhost:5173"}})


# set up a rotating file handler
file_handler = RotatingFileHandler(
    'logs/app.log', maxBytes=10*1024, backupCount=5
)
file_handler.setFormatter(logging.Formatter(
    '%(asctime)s %(levelname)s in %(module)s: %(message)s'
))
file_handler.setLevel(logging.INFO)

app.logger.addHandler(file_handler)
app.logger.setLevel(logging.INFO)
app.logger.info("🟢 App startup complete")

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
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL", "sqlite:///reflexionpro_backend.db")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database
db.init_app(app)
migrate = Migrate(app, db)

with app.app_context():
    db.create_all()

    # Call function to create the default user
    add_default_user()

# Register Blueprints
app.register_blueprint(api, url_prefix='/api')
app.register_blueprint(goals_bp, url_prefix='/api/goals')
app.register_blueprint(dashboard_bp, url_prefix='/api/dashboard')
app.register_blueprint(profile_api, url_prefix='/api/profile')
<<<<<<< HEAD
app.register_blueprint(sessions_bp)

=======
app.register_blueprint(sync_bp, url_prefix='/api/synced')
app.register_blueprint(body_insight_bp, url_prefix='/api/body_insight')
app.register_blueprint(activity_bp, url_prefix='/api/activity')
app.register_blueprint(sessions_bp, url_prefix='/api/sessions')
>>>>>>> upstream/main
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

if __name__ == '__main__':
    debug_mode = os.getenv("FLASK_DEBUG", "False").lower() == "true"
    app.run(debug=debug_mode, port=int(os.getenv("PORT", 5000)))


