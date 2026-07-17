import os

# Get the base directory path of this file (project root)
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    """
    Configuration settings class for the Flask Application.
    """
    # Secret key is crucial for securing sessions and flashing messages.
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-session-key-change-in-production'
    
    # 1. Look for the production database URL from the environment variables
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    
    # 2. If it's a Heroku/Render Postgres URL, fix the 'postgres://' vs 'postgresql://' compatibility issue
    if SQLALCHEMY_DATABASE_URI:
        if SQLALCHEMY_DATABASE_URI.startswith("postgres://"):
            SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI.replace("postgres://", "postgresql://", 1)
    else:
        # Fallback to local SQLite file for development
        SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(BASE_DIR, 'students.db')}"
    
    # Disable tracking modifications to save memory and performance
    SQLALCHEMY_TRACK_MODIFICATIONS = False
