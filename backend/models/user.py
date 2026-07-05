from datetime import datetime, timezone
from werkzeug.security import generate_password_hash, check_password_hash
from backend.database import db

class User(db.Model):
    """
    ORM Model representing the 'users' table in the database for administrators.
    """
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    
    # Unique administrator username
    username = db.Column(db.String(50), unique=True, nullable=False)
    
    # Store only the secure password hashes, never the raw passwords
    password_hash = db.Column(db.String(255), nullable=False)
    
    # Time of registration
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def set_password(self, password):
        """
        Hashes the provided plain text password and saves the secure hash.
        """
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """
        Validates the provided password against the stored hash.
        """
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<User {self.username}>"
