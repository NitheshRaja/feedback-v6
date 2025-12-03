"""
Feedback and sentiment analysis models
"""
from sqlalchemy import Column, Integer, String, Float, Text, DateTime, ForeignKey, JSON, Enum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import enum
from app.core.database import Base


class SentimentCategory(str, enum.Enum):
    """Sentiment category enumeration"""
    POSITIVE = "positive"
    NEUTRAL = "neutral"
    NEGATIVE = "negative"


class EmotionalTone(str, enum.Enum):
    """Emotional tone enumeration"""
    CONFUSION = "confusion"
    STRESS = "stress"
    MOTIVATION = "motivation"
    SATISFACTION = "satisfaction"
    FRUSTRATION = "frustration"
    APPRECIATION = "appreciation"


class FeedbackCategory(str, enum.Enum):
    """Feedback category enumeration"""
    TRAINER = "trainer"
    MENTOR = "mentor"
    BATCH_OWNER = "batch_owner"
    INFRASTRUCTURE = "infrastructure"
    TRAINING_PROGRAM = "training_program"
    ENGAGEMENT = "engagement"


class TraineeStage(str, enum.Enum):
    """Trainee lifecycle stage"""
    NEW_JOINER = "new_joiner"  # 0-4 weeks
    INTERMEDIATE = "intermediate"  # 5-12 weeks
    ABOUT_TO_GRADUATE = "about_to_graduate"  # 13+ weeks


class Feedback(Base):
    """Feedback record model"""
    __tablename__ = "feedback"
    
    id = Column(Integer, primary_key=True, index=True)
    trainee_id = Column(String(100), index=True, nullable=False)  # Masked/anonymized
    location = Column(String(100), index=True, nullable=False)
    training_batch = Column(String(100), index=True, nullable=False)
    week_start_date = Column(DateTime(timezone=True), index=True, nullable=False)
    week_end_date = Column(DateTime(timezone=True), nullable=False)
    rating_score = Column(Integer, nullable=True)  # 1-5
    open_text = Column(Text, nullable=False)
    category_tags = Column(String(500), nullable=True)  # Comma-separated tags
    trainee_stage = Column(Enum(TraineeStage), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    sentiment_analysis = relationship("SentimentAnalysis", back_populates="feedback", uselist=False)
    category_mappings = relationship("CategoryMapping", back_populates="feedback")


class SentimentAnalysis(Base):
    """Sentiment analysis results"""
    __tablename__ = "sentiment_analysis"
    
    id = Column(Integer, primary_key=True, index=True)
    feedback_id = Column(Integer, ForeignKey("feedback.id"), unique=True, nullable=False)
    sentiment_category = Column(Enum(SentimentCategory), nullable=False)
    emotional_tone = Column(Enum(EmotionalTone), nullable=True)
    confidence_score = Column(Float, nullable=False)  # 0.0-1.0
    raw_sentiment_scores = Column(JSON, nullable=True)  # Store all class probabilities
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    feedback = relationship("Feedback", back_populates="sentiment_analysis")


class CategoryMapping(Base):
    """Category mapping for feedback"""
    __tablename__ = "category_mappings"
    
    id = Column(Integer, primary_key=True, index=True)
    feedback_id = Column(Integer, ForeignKey("feedback.id"), nullable=False)
    category = Column(Enum(FeedbackCategory), nullable=False)
    relevance_score = Column(Float, nullable=False)  # 0.0-1.0
    keywords_matched = Column(JSON, nullable=True)  # List of matched keywords
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    feedback = relationship("Feedback", back_populates="category_mappings")




