import os
from flask import Flask
from app.config import Config
from app.extensions import db, migrate, cors, oauth, init_firebase_app
from app.routes.auth import auth_bp

from app.routes.web import web_bp 
from app.routes.goals import goals_bp 
# from app.routes.friends import friends_bp
from app.routes.profile import profile_bp 
from app.services.oauth_service import register_oauth_clients
from app.routes.routes import api_bp 


def create_app(config_class=Config):
    # Initialize Flask application
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object(config_class)

    # Enable CORS for API routes (allow frontend dev server)
    cors.init_app(app, resources={r"/api/*": {"origins": app.config.get('FRONTEND_URL', 'http://localhost:5173')}})

    # Initialize Firebase Admin SDK
    init_firebase_app(app)
    print('hjiss')

    # Initialize Flask extensions
    db.init_app(app)
    migrate.init_app(app, db)
    oauth.init_app(app)

    # Register OAuth provider clients
    register_oauth_clients(app)

    # Register Blueprints for API endpoints
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(profile_bp, url_prefix='/api/profile')
    app.register_blueprint(goals_bp, url_prefix='/api/goals')
    # app.register_blueprint(friends_bp, url_prefix='/api/friends')
    
    #endpoints for testing purposes
    app.register_blueprint(api_bp, url_prefix='/api')
    app.register_blueprint(web_bp, url_prefix='/api/web')

    # Health-check endpoint
    @app.route('/', methods=['GET'])
    def health_check():
        return {'status': 'ok'}, 200

    return app
