import os

# Get the base directory path of this file (project root)
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    """
    Configuration settings class for the Flask Application.
    """
    # Secret key is crucial for securing sessions and flashing messages.
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-session-key-change-in-production'
    
    # Path to SQLite database file. We save it in the root folder as 'students.db'
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(BASE_DIR, 'students.db')}"
    
    # Disable tracking modifications to save memory and performance
    SQLALCHEMY_TRACK_MODIFICATIONS = False
