from app import db
from datetime import datetime
import pytz
from werkzeug.security import generate_password_hash, check_password_hash

jakarta = pytz.timezone('Asia/Jakarta')

def now_jakarta():
    return datetime.now(jakarta)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(64), index=True, unique=True, nullable=False)
    email = db.Column(db.String(120), index=True, unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=now_jakarta)
    updated_at = db.Column(db.DateTime, default=now_jakarta)
    last_seen = db.Column(db.DateTime, default=now_jakarta, onupdate=now_jakarta)
    is_active = db.Column(db.Boolean, default=True)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'last_seen': self.last_seen,
            'is_active': self.is_active
        }
    def update_last_seen(self):
        self.last_seen = now_jakarta()
        db.session.commit()
    
    def __repr__(self):
        return f'<User {self.username}>'