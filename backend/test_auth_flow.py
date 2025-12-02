"""Test the complete authentication flow"""
from app.core.database import SessionLocal
from app.models.user import User
from app.core.security import verify_password, create_access_token, decode_access_token

# Test 1: Verify user exists and password works
print("=== Test 1: User Verification ===")
db = SessionLocal()
user = db.query(User).filter(User.email == "admin@example.com").first()
if user:
    print(f"✅ User found: {user.email}")
    print(f"   Role: {user.role.value}")
    print(f"   Is Active: {user.is_active}")
    
    # Test password
    password_ok = verify_password("admin123", user.hashed_password)
    print(f"   Password check: {'✅ CORRECT' if password_ok else '❌ WRONG'}")
else:
    print("❌ User not found")
    db.close()
    exit(1)

# Test 2: Create and decode token
print("\n=== Test 2: Token Creation & Decoding ===")
token = create_access_token({
    "sub": str(user.id),  # JWT requires sub to be a string
    "email": user.email,
    "role": user.role.value
})
print(f"✅ Token created: {token[:50]}...")

decoded = decode_access_token(token)
if decoded:
    print(f"✅ Token decoded successfully")
    print(f"   User ID: {decoded.get('sub')}")
    print(f"   Email: {decoded.get('email')}")
    print(f"   Role: {decoded.get('role')}")
else:
    print("❌ Token decode FAILED")
    print("   This is the problem!")

db.close()

print("\n=== Summary ===")
if password_ok and decoded:
    print("✅ All tests passed - login should work!")
else:
    print("❌ Some tests failed - check the output above")

