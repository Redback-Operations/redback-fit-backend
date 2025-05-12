from flask_sqlalchemy import SQLAlchemy
from flask_migrate    import Migrate
from flask_cors       import CORS
from authlib.integrations.flask_client import OAuth
import firebase_admin
from firebase_admin import credentials

db       = SQLAlchemy()
migrate  = Migrate()
cors     = CORS()
oauth    = OAuth()

def init_firebase_app(app):
    cred_path = app.config.get('FIREBASE_CREDENTIALS')
    # Sanity check
    if not cred_path:
        raise RuntimeError(
          "FIREBASE_CREDENTIALS (GOOGLE_APPLICATION_CREDENTIALS) "
          "must be set to your service account JSON file path"
        )
    
    cred = credentials.Certificate(app.config['FIREBASE_CREDENTIALS'])
    firebase_admin.initialize_app(cred, {
        'databaseURL': app.config['FIREBASE_DATABASE_URL']
    })
