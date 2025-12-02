"""
Report and analytics models
"""
from sqlalchemy import Column, Integer, String, Float, Text, DateTime, ForeignKey, JSON, Enum, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import enum
from app.core.database import Base


class ActionPriority(str, enum.Enum):
    """Action item priority"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"


class ActionStatus(str, enum.Enum):
    """Action item status"""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class WeeklyReport(Base):
    """Weekly sentiment analysis report"""
    __tablename__ = "weekly_reports"
    
    id = Column(Integer, primary_key=True, index=True)
    week_start_date = Column(DateTime(timezone=True), index=True, nullable=False)
    week_end_date = Column(DateTime(timezone=True), nullable=False)
    overall_sentiment_score = Column(Float, nullable=False)  # Percentage
    sentiment_change = Column(Float, nullable=True)  # Week-over-week change percentage
    heat_index = Column(Float, nullable=False)  # 0-100
    total_feedback_count = Column(Integer, nullable=False)
    positive_count = Column(Integer, nullable=False)
    neutral_count = Column(Integer, nullable=False)
    negative_count = Column(Integer, nullable=False)
    report_data = Column(JSON, nullable=True)  # Full report data as JSON
    pdf_path = Column(String(500), nullable=True)  # Path to generated PDF
    executive_summary = Column(Text, nullable=True)  # AI-generated summary
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    action_items = relationship("ActionItem", back_populates="report")


class ActionItem(Base):
    """Actionable recommendations"""
    __tablename__ = "action_items"
    
    id = Column(Integer, primary_key=True, index=True)
    report_id = Column(Integer, ForeignKey("weekly_reports.id"), nullable=False)
    priority = Column(Enum(ActionPriority), nullable=False)
    category = Column(String(100), nullable=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    assigned_to = Column(String(255), nullable=True)
    status = Column(Enum(ActionStatus), default=ActionStatus.PENDING)
    confidence_score = Column(Float, nullable=True)  # Confidence in recommendation
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    report = relationship("WeeklyReport", back_populates="action_items")


class TrendData(Base):
    """Trend analysis data"""
    __tablename__ = "trend_data"
    
    id = Column(Integer, primary_key=True, index=True)
    week_start_date = Column(DateTime(timezone=True), index=True, nullable=False)
    category = Column(String(100), index=True, nullable=True)  # Null for overall
    sentiment_distribution = Column(JSON, nullable=False)  # {positive: %, neutral: %, negative: %}
    volume = Column(Integer, nullable=False)  # Feedback count
    average_rating = Column(Float, nullable=True)
    trainee_stage = Column(String(50), nullable=True)  # For lifecycle tracking
    created_at = Column(DateTime(timezone=True), server_default=func.now())



