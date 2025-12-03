"""
Feedback upload and management endpoints
"""
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, status
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import List, Optional
from app.core.database import get_db
from app.api.v1.endpoints.auth import get_current_user
from app.models.user import User, UserRole
from app.models.feedback import Feedback, SentimentAnalysis, CategoryMapping, TraineeStage, SentimentCategory, FeedbackCategory
from app.services.file_processor import FileProcessor
from app.ml.sentiment_analyzer import sentiment_analyzer
from app.ml.category_mapper import category_mapper
from app.core.config import settings
from pydantic import BaseModel

router = APIRouter()


class FeedbackResponse(BaseModel):
    id: int
    trainee_id: str
    location: str
    training_batch: str
    rating_score: Optional[int]
    sentiment_category: Optional[str]
    confidence_score: Optional[float]
    
    class Config:
        from_attributes = True


@router.post("/upload")
async def upload_feedback_file(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Upload and process feedback file (CSV/Excel)"""
    # Check permissions
    if current_user.role not in [UserRole.ADMIN, UserRole.SYSTEM_OWNER]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to upload files"
        )
    
    # Process file
    processor = FileProcessor(settings.UPLOAD_DIR)
    result = await processor.process_file(file)
    
    if not result["success"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"errors": result["errors"], "total_rows": result["total_rows"]}
        )
    
    # Save feedback records
    saved_count = 0
    errors = []
    
    for record in result["data"]:
        try:
            # Determine week dates if not provided
            week_start = record.get("week_start_date")
            week_end = record.get("week_end_date")
            
            if not week_start:
                # Default to current week
                today = datetime.now()
                week_start = today - timedelta(days=today.weekday())
                week_end = week_start + timedelta(days=6)
            
            # Determine trainee stage (simplified - would need trainee start date)
            # For now, we'll leave it as None and update later
            
            # Create feedback record
            feedback = Feedback(
                trainee_id=record["trainee_id"],
                location=record["location"],
                training_batch=record["training_batch"],
                week_start_date=week_start,
                week_end_date=week_end,
                rating_score=record["rating_score"],
                open_text=record["open_text"],
                category_tags=record.get("category_tags")
            )
            
            db.add(feedback)
            db.flush()  # Get feedback ID
            
            # Perform sentiment analysis
            sentiment_result = sentiment_analyzer.analyze(record["open_text"])
            emotional_tone = sentiment_analyzer.detect_emotional_tone(
                record["open_text"],
                sentiment_result["sentiment"]
            )
            
            sentiment_analysis = SentimentAnalysis(
                feedback_id=feedback.id,
                sentiment_category=SentimentCategory(sentiment_result["sentiment"]),
                emotional_tone=emotional_tone,
                confidence_score=sentiment_result["confidence"],
                raw_sentiment_scores=sentiment_result["scores"]
            )
            db.add(sentiment_analysis)
            
            # Map categories
            category_mappings = category_mapper.map_categories(
                record["open_text"],
                record.get("category_tags")
            )
            
            for mapping in category_mappings:
                category_mapping = CategoryMapping(
                    feedback_id=feedback.id,
                    category=FeedbackCategory(mapping["category"]),
                    relevance_score=mapping["relevance_score"],
                    keywords_matched=mapping["keywords_matched"]
                )
                db.add(category_mapping)
            
            saved_count += 1
            
        except Exception as e:
            errors.append(f"Error saving record: {str(e)}")
            continue
    
    db.commit()
    
    return {
        "message": "File processed successfully",
        "total_rows": result["total_rows"],
        "processed_rows": result["processed_rows"],
        "saved_count": saved_count,
        "errors": errors
    }


@router.get("/", response_model=List[FeedbackResponse])
async def get_feedback(
    week_start: Optional[datetime] = None,
    batch: Optional[str] = None,
    location: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100
):
    """Get feedback records with filters"""
    query = db.query(Feedback)
    
    # Apply role-based filtering
    if current_user.role == UserRole.BATCH_OWNER:
        if current_user.batch_access:
            allowed_batches = current_user.batch_access.split(",")
            query = query.filter(Feedback.training_batch.in_(allowed_batches))
        else:
            # No batch access configured
            return []
    
    # Apply filters
    if week_start:
        week_end = week_start + timedelta(days=6)
        query = query.filter(
            Feedback.week_start_date >= week_start,
            Feedback.week_start_date <= week_end
        )
    
    if batch:
        query = query.filter(Feedback.training_batch == batch)
    
    if location:
        query = query.filter(Feedback.location == location)
    
    feedback_list = query.offset(skip).limit(limit).all()
    
    return feedback_list




