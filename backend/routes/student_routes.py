import re
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, session
from backend.database import db
from backend.models import Student

# Create a Flask blueprint for student routes
student_bp = Blueprint('student', __name__)

@student_bp.before_request
def check_login():
    """
    Guard function that restricts all student management routes
    to logged-in administrators only.
    """
    if 'user_id' not in session:
        flash("Please sign in to access the registry.", "warning")
        return redirect(url_for('auth.login'))

# Regular expression for basic email validation
EMAIL_REGEX = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

def validate_student_data(data, is_update=False, current_student_id=None):
    """
    Validates form data for adding or updating a student.
    Returns a list of error messages (empty if valid).
    """
    errors = []
    
    # 1. Required Field Checks
    student_id = str(data.get('student_id') or '').strip()
    first_name = str(data.get('first_name') or '').strip()
    last_name = str(data.get('last_name') or '').strip()
    email = str(data.get('email') or '').strip()
    major = str(data.get('major') or '').strip()
    
    gpa_val = data.get('gpa')
    gpa_str = str(gpa_val).strip() if gpa_val is not None else ''
    
    if not is_update and not student_id:
        errors.append("Student ID is required.")
    if not first_name:
        errors.append("First Name is required.")
    if not last_name:
        errors.append("Last Name is required.")
    if not email:
        errors.append("Email Address is required.")
    if not major:
        errors.append("Major/Course is required.")
    if not gpa_str:
        errors.append("GPA is required.")
        
    # If initial fields are missing, return early
    if errors:
        return errors

    # 2. Email Pattern Validation
    if not re.match(EMAIL_REGEX, email):
        errors.append("Please enter a valid email address.")

    # 3. GPA Value Validation
    try:
        gpa = float(gpa_str)
        if gpa < 0.0 or gpa > 4.0:
            errors.append("GPA must be between 0.0 and 4.0.")
    except ValueError:
        errors.append("GPA must be a valid decimal number.")

    # 4. Database Uniqueness Checks
    # For Student ID (only check on create)
    if not is_update:
        existing_id = Student.query.filter_by(student_id=student_id).first()
        if existing_id:
            errors.append(f"A student with Student ID '{student_id}' already exists.")
            
    # For Email (on create, or on update if the email changed)
    existing_email = Student.query.filter_by(email=email).first()
    if existing_email:
        if not is_update or (is_update and existing_email.id != current_student_id):
            errors.append(f"A student with Email '{email}' already exists.")

    return errors


@student_bp.route('/')
def dashboard():
    """
    Renders the main dashboard containing all students list.
    Supports a 'q' query parameter for server-side search.
    """
    search_query = request.args.get('q', '').strip()
    
    if search_query:
        # Search by student_id, first_name, last_name, email, or major
        students = Student.query.filter(
            (Student.student_id.ilike(f"%{search_query}%")) |
            (Student.first_name.ilike(f"%{search_query}%")) |
            (Student.last_name.ilike(f"%{search_query}%")) |
            (Student.email.ilike(f"%{search_query}%")) |
            (Student.major.ilike(f"%{search_query}%"))
        ).order_by(Student.student_id.asc()).all()
    else:
        students = Student.query.order_by(Student.student_id.asc()).all()
        
    return render_template('index.html', students=students, search_query=search_query)


@student_bp.route('/add', methods=['GET', 'POST'])
def add_student():
    """
    Endpoint to add a new student.
    GET: Renders the blank registration form.
    POST: Processes registration with full validation.
    """
    if request.method == 'POST':
        # Retrieve form data
        form_data = {
            'student_id': request.form.get('student_id', '').strip(),
            'first_name': request.form.get('first_name', '').strip(),
            'last_name': request.form.get('last_name', '').strip(),
            'email': request.form.get('email', '').strip(),
            'major': request.form.get('major', '').strip(),
            'gpa': request.form.get('gpa', '').strip()
        }
        
        # Validate data
        errors = validate_student_data(form_data, is_update=False)
        
        if errors:
            for error in errors:
                flash(error, 'danger')
            # Render page again, passing back form_data so fields remain populated
            return render_template('add.html', form_data=form_data)
            
        try:
            # Create new student object and save to DB
            new_student = Student(
                student_id=form_data['student_id'],
                first_name=form_data['first_name'],
                last_name=form_data['last_name'],
                email=form_data['email'],
                major=form_data['major'],
                gpa=float(form_data['gpa'])
            )
            db.session.add(new_student)
            db.session.commit()
            flash("Student added successfully!", "success")
            return redirect(url_for('student.dashboard'))
        except Exception as e:
            db.session.rollback()
            flash(f"An error occurred while saving to database: {str(e)}", "danger")
            return render_template('add.html', form_data=form_data)

    # For GET request, render blank form
    return render_template('add.html', form_data={})


@student_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_student(id):
    """
    Endpoint to edit an existing student.
    GET: Renders form populated with current database details.
    POST: Updates fields after validation.
    """
    student = Student.query.get_or_404(id)
    
    if request.method == 'POST':
        # Retrieve form data (Student ID cannot be changed to prevent key tampering)
        form_data = {
            'student_id': student.student_id,  # Readonly display field
            'first_name': request.form.get('first_name', '').strip(),
            'last_name': request.form.get('last_name', '').strip(),
            'email': request.form.get('email', '').strip(),
            'major': request.form.get('major', '').strip(),
            'gpa': request.form.get('gpa', '').strip()
        }
        
        # Validate data
        errors = validate_student_data(form_data, is_update=True, current_student_id=student.id)
        
        if errors:
            for error in errors:
                flash(error, 'danger')
            return render_template('edit.html', student=student, form_data=form_data)
            
        try:
            # Update fields
            student.first_name = form_data['first_name']
            student.last_name = form_data['last_name']
            student.email = form_data['email']
            student.major = form_data['major']
            student.gpa = float(form_data['gpa'])
            
            db.session.commit()
            flash("Student details updated successfully!", "success")
            return redirect(url_for('student.dashboard'))
        except Exception as e:
            db.session.rollback()
            flash(f"An error occurred while updating database: {str(e)}", "danger")
            return render_template('edit.html', student=student, form_data=form_data)
            
    # GET Request: Populate form with existing student details
    form_data = {
        'student_id': student.student_id,
        'first_name': student.first_name,
        'last_name': student.last_name,
        'email': student.email,
        'major': student.major,
        'gpa': str(student.gpa)
    }
    return render_template('edit.html', student=student, form_data=form_data)


@student_bp.route('/delete/<int:id>', methods=['POST'])
def delete_student(id):
    """
    Endpoint to delete a student.
    Uses POST method to prevent accidental trigger via GET crawler pre-fetching.
    """
    student = Student.query.get_or_404(id)
    try:
        db.session.delete(student)
        db.session.commit()
        flash(f"Student {student.first_name} {student.last_name} deleted successfully.", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"An error occurred while deleting: {str(e)}", "danger")
        
    return redirect(url_for('student.dashboard'))


# ==========================================================================
# RESTFUL JSON API ENDPOINTS (FOR POSTMAN INTEGRATION)
# ==========================================================================

@student_bp.route('/api/students', methods=['GET'])
def api_get_students():
    """
    Returns a list of all students as JSON.
    """
    students = Student.query.order_by(Student.student_id.asc()).all()
    return jsonify([student.to_dict() for student in students]), 200


@student_bp.route('/api/students/<int:id>', methods=['GET'])
def api_get_student(id):
    """
    Returns details of a specific student by primary key ID.
    """
    student = Student.query.get(id)
    if not student:
        return jsonify({"error": "Student not found"}), 404
    return jsonify(student.to_dict()), 200


@student_bp.route('/api/students', methods=['POST'])
def api_create_student():
    """
    Creates a new student via JSON payload.
    """
    data = request.get_json() or {}
    errors = validate_student_data(data, is_update=False)
    if errors:
        return jsonify({"errors": errors}), 400
        
    try:
        new_student = Student(
            student_id=str(data.get('student_id')).strip(),
            first_name=str(data.get('first_name')).strip(),
            last_name=str(data.get('last_name')).strip(),
            email=str(data.get('email')).strip(),
            major=str(data.get('major')).strip(),
            gpa=float(data.get('gpa'))
        )
        db.session.add(new_student)
        db.session.commit()
        return jsonify(new_student.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Failed to save student: {str(e)}"}), 500


@student_bp.route('/api/students/<int:id>', methods=['PUT'])
def api_update_student(id):
    """
    Updates student details via JSON payload.
    """
    student = Student.query.get(id)
    if not student:
        return jsonify({"error": "Student not found"}), 404
        
    data = request.get_json() or {}
    errors = validate_student_data(data, is_update=True, current_student_id=student.id)
    if errors:
        return jsonify({"errors": errors}), 400
        
    try:
        student.first_name = str(data.get('first_name')).strip()
        student.last_name = str(data.get('last_name')).strip()
        student.email = str(data.get('email')).strip()
        student.major = str(data.get('major')).strip()
        student.gpa = float(data.get('gpa'))
        
        db.session.commit()
        return jsonify(student.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Failed to update student: {str(e)}"}), 500


@student_bp.route('/api/students/<int:id>', methods=['DELETE'])
def api_delete_student(id):
    """
    Deletes a student.
    """
    student = Student.query.get(id)
    if not student:
        return jsonify({"error": "Student not found"}), 404
        
    try:
        db.session.delete(student)
        db.session.commit()
        return jsonify({"message": f"Student {student.first_name} {student.last_name} deleted successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Failed to delete student: {str(e)}"}), 500
