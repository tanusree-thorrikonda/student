from backend import create_app
from backend.database import db
from backend.models import User

# Instantiate application factory
app = create_app()

print("==================================================")
print("     STARTING AUTHENTICATION VERIFICATION TEST    ")
print("==================================================")

try:
    with app.app_context():
        # 1. Cleanup any previous test user
        print("[1/5] Cleaning up existing auth test records...")
        User.query.filter_by(username="auth_test_admin").delete()
        db.session.commit()

        # 2. CREATE Test Admin User
        print("[2/5] Testing administrator CREATE operation...")
        test_user = User(username="auth_test_admin")
        test_user.set_password("SecurePassword789!")
        db.session.add(test_user)
        db.session.commit()
        print(f"  -> SUCCESS: Created test user: {test_user}")

        # 3. VERIFY password hash isn't plaintext
        print("[3/5] Checking password hash string properties...")
        assert test_user.password_hash != "SecurePassword789!", "Verification Error: Password was stored in raw plaintext!"
        assert test_user.password_hash.startswith("scrypt:") or test_user.password_hash.startswith("pbkdf2:"), "Verification Error: Password hash does not match standard hashing patterns."
        print("  -> SUCCESS: Password successfully hashed.")

        # 4. VERIFY credentials checking
        print("[4/5] Testing password verification methods...")
        fetched_user = User.query.filter_by(username="auth_test_admin").first()
        assert fetched_user is not None, "Verification Error: Test user not found in database."
        assert fetched_user.check_password("SecurePassword789!"), "Verification Error: Valid password check failed."
        assert not fetched_user.check_password("IncorrectPassword"), "Verification Error: Invalid password check failed to reject."
        print("  -> SUCCESS: Password check validation works perfectly.")

        # 5. DELETE Test Admin User
        print("[5/5] Testing administrator DELETE operation...")
        db.session.delete(fetched_user)
        db.session.commit()
        
        deleted_user = User.query.filter_by(username="auth_test_admin").first()
        assert deleted_user is None, "Verification Error: User record was not removed from database."
        print("  -> SUCCESS: Removed test user record successfully.")

    print("\n==================================================")
    print("   AUTHENTICATION INTEGRATION TEST: ALL PASSED   ")
    print("==================================================")

except Exception as e:
    print("\n==================================================")
    print(f"   VERIFICATION FAILED: {str(e)}")
    print("==================================================")
    import sys
    sys.exit(1)
