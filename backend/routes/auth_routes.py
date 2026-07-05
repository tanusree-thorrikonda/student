from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from backend.database import db
from backend.models import User

# Create a Flask blueprint for authentication routes
auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    Renders login portal and validates user sessions.
    """
    # If user is already logged in, redirect them to dashboard
    if 'user_id' in session:
        return redirect(url_for('student.dashboard'))

    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')

        if not username or not password:
            flash("Username and password are required.", "danger")
            return render_template('login.html', username=username)

        # Query user from DB
        user = User.query.filter_by(username=username).first()

        # Validate username existence and password hash matches
        if user and user.check_password(password):
            session['user_id'] = user.id
            session['username'] = user.username
            flash(f"Welcome back, {user.username}!", "success")
            return redirect(url_for('student.dashboard'))
        else:
            flash("Invalid username or password.", "danger")
            return render_template('login.html', username=username)

    return render_template('login.html')


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """
    Handles registering new administrators.
    """
    if 'user_id' in session:
        return redirect(url_for('student.dashboard'))

    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')

        # Basic validations
        if not username or not password or not confirm_password:
            flash("All fields are required.", "danger")
            return render_template('register.html', username=username)

        if len(username) < 3 or len(username) > 30:
            flash("Username must be between 3 and 30 characters.", "danger")
            return render_template('register.html', username=username)

        if len(password) < 6:
            flash("Password must be at least 6 characters long.", "danger")
            return render_template('register.html', username=username)

        if password != confirm_password:
            flash("Passwords do not match.", "danger")
            return render_template('register.html', username=username)

        # Check if username is already taken
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash("Username is already taken.", "danger")
            return render_template('register.html', username=username)

        try:
            # Create user and hash password
            new_user = User(username=username)
            new_user.set_password(password)
            db.session.add(new_user)
            db.session.commit()
            flash("Registration successful! You can now log in.", "success")
            return redirect(url_for('auth.login'))
        except Exception as e:
            db.session.rollback()
            flash(f"An error occurred while saving: {str(e)}", "danger")
            return render_template('register.html', username=username)

    return render_template('register.html')


@auth_bp.route('/logout')
def logout():
    """
    Clears user session.
    """
    session.pop('user_id', None)
    session.pop('username', None)
    flash("You have been successfully logged out.", "success")
    return redirect(url_for('auth.login'))
