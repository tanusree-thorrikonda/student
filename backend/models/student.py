from datetime import datetime, timezone
from backend.database import db

class Student(db.Model):
    """
    ORM Model representing the 'students' table in the database.
    """
    __tablename__ = 'students'

    id = db.Column(db.Integer, primary_key=True)
    
    # We assign a readable unique student identifier (e.g. 'STU-2026-0001')
    student_id = db.Column(db.String(20), unique=True, nullable=False)
    
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    major = db.Column(db.String(100), nullable=False)
    
    # GPA represents Grade Point Average, usually between 0.0 and 4.0
    gpa = db.Column(db.Float, nullable=False)
    
    # Auto-recorded timestamp using timezone-aware UTC datetime
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def __repr__(self):
        return f"<Student {self.student_id}: {self.first_name} {self.last_name}>"

    def to_dict(self):
        """
        Helper method to serialize the model into a dictionary format.
        Useful if we want to return JSON data or manipulate it in Python.
        """
        return {
            'id': self.id,
            'student_id': self.student_id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'major': self.major,
            'gpa': self.gpa,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S') if self.created_at else None
        }
