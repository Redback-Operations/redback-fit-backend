from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_wtf import CSRFProtect
import os


db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate() 
csrf = CSRFProtect()
limiter = Limiter(
    key_func=get_remote_address, 
    default_limits=["200 per hour"],
    storage_uri=os.getenv("RATELIMIT_STORAGE_URL", "memory://"),
)