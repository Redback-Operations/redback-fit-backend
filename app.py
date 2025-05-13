from flask import Flask, jsonify, session, render_template, request, redirect
from flask_cors import CORS
from api.routes import api
from api.goals import goals_bp
from models.goal import db
from dotenv import load_dotenv
import os
import pyrebase

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "http://localhost:5173"}})

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

# Initialize database
db.init_app(app)
with app.app_context():
    db.create_all()

# Register Blueprints
app.register_blueprint(api, url_prefix='/api')
app.register_blueprint(goals_bp, url_prefix='/api/goals')

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

