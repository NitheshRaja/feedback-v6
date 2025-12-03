"""
User model for authentication and authorization
"""
from sqlalchemy import Column, Integer, String, Enum, DateTime, Boolean
from sqlalchemy.sql import func
import enum
from app.core.database import Base


class UserRole(str, enum.Enum):
    """User role enumeration"""
    ADMIN = "admin"
    BATCH_OWNER = "batch_owner"
    LEADERSHIP = "leadership"
    SYSTEM_OWNER = "system_owner"


class User(Base):
    """User model"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=False)
    role = Column(Enum(UserRole), nullable=False, default=UserRole.BATCH_OWNER)
    is_active = Column(Boolean, default=True)
    batch_access = Column(String(500), nullable=True)  # Comma-separated batch IDs for batch owners
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())




