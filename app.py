from flask import Flask, jsonify, session, render_template, redirect, url_for
from flask_cors import CORS
from flask_migrate import Migrate
from flask_login import LoginManager, login_required
from dotenv import load_dotenv
import os

# Local imports
from models import db, UserCredential
from api.routes import api
from api.goals import goals_bp
from api.profile import api as profile_api
from api.dashboard import dashboard_bp
from auth.routes import auth_bp

# Import scripts here 
from scripts.add_default_user import add_default_user

# Load environment variables from .env file
load_dotenv()

login_manager = LoginManager()
login_manager.login_view = "auth.login"

@login_manager.user_loader
def load_user(user_id: str):
    try:
        return db.session.get(UserCredential, int(user_id))
    except (TypeError, ValueError):
        return None 

def create_app():
    app = Flask(__name__)

    # Flask config (Core)
    app.secret_key = os.getenv("SECRET_KEY", "default_secret_key")
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL", "sqlite:///goals.db")
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize database
    db.init_app(app)
    login_manager.init_app(app)
    Migrate(app, db)
    CORS(
        app,
        resources={r"/api/*": {"origins": os.getenv("CORS_ORIGINS", "http://localhost:5173")}},
        supports_credentials=True,
    )

    # Register Blueprints
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(api, url_prefix='/api')
    app.register_blueprint(goals_bp, url_prefix='/api/goals')
    app.register_blueprint(dashboard_bp, url_prefix='/api/dashboard')
    app.register_blueprint(profile_api, url_prefix='/api/profile')

    # Routes
    @app.route('/')
    def index():
        # send to login if not logged in
        return redirect(url_for('auth.login'))
    
    @app.route('/home')
    @login_required
    def home():
        return render_template('home.html', user=session.get('user_id'))

    # Example API route
    @app.route('/api/hello', methods=['GET'])
    def hello():
        return jsonify({'message': 'Hello from Flask!'}), 200

    # Create database tables if they don't exist
    with app.app_context():
        db.create_all()

    return app


if __name__ == '__main__':
    app = create_app()
    debug_mode = os.getenv("FLASK_DEBUG", "False").lower() == "true"
    port = int(os.getenv("PORT", 5000))
    app.run(debug=debug_mode, port=port)


