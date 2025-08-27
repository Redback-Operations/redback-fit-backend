from extensions import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

class UserCredential(db.Model, UserMixin):
    __tablename__="user_credential"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), index=True, nullable=False, unique=True)
    password_hash = db.Column(db.String(255), nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    created_at =db.Column(db.DateTime, server_default=db.func.now(), nullable=False)

    profile = db.relationship("UserProfile", back_populates="user", uselist=False, cascade="all, delete-orphan")

    def set_password(self, raw_password: str):
        self.password_hash = generate_password_hash(raw_password)

    def check_password(self, raw_password: str) -> bool:
        return check_password_hash(self.password_hash, raw_password)
    
    def __repr__(self):
        return f"<UserCredential id=self.id email={self.email}>"