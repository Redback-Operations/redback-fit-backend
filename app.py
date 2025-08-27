import os
from flask import Flask, jsonify, session, render_template, redirect, url_for
from flask_cors import CORS
from flask_login import login_required, current_user
from dotenv import load_dotenv

# Local imports
from models import UserCredential
from extensions import db, login_manager, migrate, limiter, csrf
from api.routes import api
from api.goals import goals_bp
from api.profile import api as profile_api
from api.dashboard import dashboard_bp
from auth.routes import auth_bp

# Import scripts here 
from scripts.add_default_user import add_default_user


# Load environment variables from .env file
load_dotenv()


@login_manager.user_loader
def load_user(user_id: str):
    try:
        return db.session.get(UserCredential, int(user_id))
    except (TypeError, ValueError):
        return None 

def create_app():
    app = Flask(__name__)

    # Flask config (Core)
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "dev-secret")
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL", "sqlite:///goals.db")
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config["WTF_CSRF_ENABLED"] = True

    # Security settings for cookies
    app.config.update(
        SESSION_COOKIE_HTTPONLY=True,
        SESSION_COOKIE_SAMESITE="Lax",
        SESSION_COOKIE_SECURE=False,  
        REMEMBER_COOKIE_HTTPONLY=True,
        REMEMBER_COOKIE_SECURE=False, 
    )


    # Initialize database
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    if limiter:
        limiter.init_app(app)
    csrf.init_app(app)
    CORS(
        app,
        resources={r"/api/*": {"origins": os.getenv("CORS_ORIGINS", "http://localhost:5173")}},
        supports_credentials=True,
    )

    app.cli.add_command(add_default_user)

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
        return render_template('home.html', user=current_user)

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


