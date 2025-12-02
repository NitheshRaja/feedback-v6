"""Test password verification"""
from app.core.database import SessionLocal
from app.models.user import User
from app.core.security import verify_password

db = SessionLocal()
user = db.query(User).filter(User.email == "admin@example.com").first()

if user:
    result = verify_password("admin123", user.hashed_password)
    if result:
        print("✅ Password verification: CORRECT")
        print("✅ Login should work now!")
    else:
        print("❌ Password verification: FAILED")
else:
    print("❌ Admin user not found")

db.close()



