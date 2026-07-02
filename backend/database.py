from flask_sqlalchemy import SQLAlchemy

# Initialize SQLAlchemy with no app context yet.
# This prevents circular imports because models and routes can import 'db'
# without needing the main Flask 'app' object.
db = SQLAlchemy()
