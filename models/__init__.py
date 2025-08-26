from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .user_credential import UserCredential
from .user_profile import UserProfile
from .goal import Goal

