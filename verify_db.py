from backend import create_app
from backend.database import db
from backend.models import Student

# Instantiate app with default configuration
app = create_app()

print("==================================================")
print("     STARTING DATABASE ORM VERIFICATION TEST     ")
print("==================================================")

try:
    with app.app_context():
        # 1. Cleanup previous test entries to ensure state purity
        print("[1/5] Cleaning up existing test records...")
        Student.query.filter(Student.student_id.like("TEST-%")).delete(synchronize_session=False)
        db.session.commit()

        # 2. CREATE Test
        print("[2/5] Testing database CREATE operation...")
        test_student = Student(
            student_id="TEST-0001",
            first_name="Jordan",
            last_name="Miller",
            email="jordan.test@university.edu",
            major="Advanced Robotics",
            gpa=3.87
        )
        db.session.add(test_student)
        db.session.commit()
        print(f"  -> SUCCESS: Created student record: {test_student}")

        # 3. READ Test
        print("[3/5] Testing database READ operation...")
        record = Student.query.filter_by(student_id="TEST-0001").first()
        assert record is not None, "Verification Error: Student record was not found in database."
        assert record.email == "jordan.test@university.edu", "Verification Error: Email attribute mismatch."
        print(f"  -> SUCCESS: Fetched student: {record.first_name} {record.last_name} ({record.major})")

        # 4. UPDATE Test
        print("[4/5] Testing database UPDATE operation...")
        record.gpa = 3.95
        record.major = "Cybernetics & AI"
        db.session.commit()
        
        updated_record = Student.query.filter_by(student_id="TEST-0001").first()
        assert updated_record.gpa == 3.95, "Verification Error: Updated GPA value mismatch."
        assert updated_record.major == "Cybernetics & AI", "Verification Error: Updated Major value mismatch."
        print(f"  -> SUCCESS: Updated details: GPA={updated_record.gpa}, Major='{updated_record.major}'")

        # 5. DELETE Test
        print("[5/5] Testing database DELETE operation...")
        db.session.delete(updated_record)
        db.session.commit()
        
        deleted_record = Student.query.filter_by(student_id="TEST-0001").first()
        assert deleted_record is None, "Verification Error: Student record was not removed from database."
        print("  -> SUCCESS: Deleted student record successfully.")

    print("\n==================================================")
    print("   DATABASE INTEGRATION VERIFICATION: ALL PASSED  ")
    print("==================================================")

except Exception as e:
    print("\n==================================================")
    print(f"   VERIFICATION FAILED: {str(e)}")
    print("==================================================")
    import sys
    sys.exit(1)
