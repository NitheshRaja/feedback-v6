"""
Reset admin password script
"""
from app.core.database import SessionLocal
from app.models.user import User
from app.core.security import get_password_hash

def reset_admin_password():
    """Reset admin user password"""
    db = SessionLocal()
    try:
        admin_user = db.query(User).filter(User.email == "admin@example.com").first()
        
        if admin_user:
            # Update password with new hashing method
            admin_user.hashed_password = get_password_hash("admin123")
            db.commit()
            print("✅ Admin password reset successfully!")
            print("   Email: admin@example.com")
            print("   Password: admin123")
        else:
            # Create admin user if it doesn't exist
            admin_user = User(
                email="admin@example.com",
                hashed_password=get_password_hash("admin123"),
                full_name="System Administrator",
                role=UserRole.ADMIN,
                is_active=True
            )
            db.add(admin_user)
            db.commit()
            print("✅ Admin user created!")
            print("   Email: admin@example.com")
            print("   Password: admin123")
    except Exception as e:
        print(f"❌ Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    from app.models.user import UserRole
    reset_admin_password()



