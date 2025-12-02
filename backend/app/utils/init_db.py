"""
Database initialization script
"""
from app.core.database import Base, engine, SessionLocal
from app.models.user import User, UserRole
from app.core.security import get_password_hash


def init_db():
    """Initialize database with tables and default admin user"""
    # Create all tables
    Base.metadata.create_all(bind=engine)
    
    # Create default admin user if it doesn't exist
    db = SessionLocal()
    try:
        admin_user = db.query(User).filter(User.email == "admin@example.com").first()
        if not admin_user:
            admin_user = User(
                email="admin@example.com",
                hashed_password=get_password_hash("admin123"),  # Change in production!
                full_name="System Administrator",
                role=UserRole.ADMIN,
                is_active=True
            )
            db.add(admin_user)
            db.commit()
            print("Default admin user created: admin@example.com / admin123")
        else:
            print("Admin user already exists")
    except Exception as e:
        print(f"Error initializing database: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    init_db()



