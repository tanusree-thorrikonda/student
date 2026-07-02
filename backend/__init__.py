import os
from flask import Flask
from backend.database import db
from backend.routes import student_bp
from config import Config

def create_app(config_class=Config):
    """
    Application Factory Pattern.
    Creates and configures an instance of the Flask application.
    """
    # Define absolute paths for custom template and static files inside 'frontend' directory
    current_dir = os.path.abspath(os.path.dirname(__file__))
    frontend_path = os.path.join(current_dir, '..', 'frontend')
    template_path = os.path.join(frontend_path, 'templates')
    static_path = os.path.join(frontend_path, 'static')

    app = Flask(
        __name__,
        template_folder=template_path,
        static_folder=static_path
    )
    
    # Load configuration
    app.config.from_object(config_class)

    # Bind SQLAlchemy to this app instance
    db.init_app(app)

    # Register the student blueprint (CRUD routes)
    app.register_blueprint(student_bp)

    # Automatically create tables in SQLite if they don't exist yet
    # Running db.create_all() within app_context ensures database handles are active
    with app.app_context():
        # Imports models here to register them with SQLAlchemy metadata
        from backend import models
        db.create_all()

    return app
