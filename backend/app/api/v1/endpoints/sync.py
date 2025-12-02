"""
API endpoint for automated data sync
"""
from fastapi import APIRouter, Depends, HTTPException, status, File, UploadFile
from sqlalchemy.orm import Session
from typing import Optional
from datetime import datetime, timedelta
from app.core.database import get_db
from app.api.v1.endpoints.auth import get_current_user
from app.models.user import User, UserRole
from app.services.file_processor import FileProcessor
from app.ml.sentiment_analyzer import SentimentAnalyzer
from app.ml.category_mapper import CategoryMapper
import logging

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/upload")
async def sync_upload_feedback(
    file: UploadFile = File(...),
    week_start: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Automated sync endpoint for feedback data upload.
    Accepts CSV/Excel files and processes them automatically.
    """
    # Check if user has permission (Admin or System Owner)
    if current_user.role not in [UserRole.ADMIN, UserRole.SYSTEM_OWNER]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Insufficient permissions. Only Admin and System Owner can sync data."
        )
    
    # Validate file type
    if not file.filename:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No file provided"
        )
    
    file_ext = file.filename.split('.')[-1].lower()
    if file_ext not in ['csv', 'xlsx', 'xls']:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid file type. Only CSV, XLSX, and XLS files are supported."
        )
    
    try:
        # Read file content
        contents = await file.read()
        
        # Process file
        processor = FileProcessor()
        feedback_data = processor.process_file(contents, file.filename)
        
        if not feedback_data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No valid feedback data found in file"
            )
        
        # Parse week_start if provided
        week_start_date = None
        if week_start:
            try:
                week_start_date = datetime.fromisoformat(week_start.replace('Z', '+00:00'))
            except:
                try:
                    week_start_date = datetime.strptime(week_start, '%Y-%m-%d')
                except:
                    pass
        
        # Process feedback with sentiment analysis
        analyzer = SentimentAnalyzer()
        category_mapper = CategoryMapper()
        
        processed_count = 0
        for data in feedback_data:
            # Use provided week_start or extract from data
            if not week_start_date and data.get('week_start_date'):
                try:
                    week_start_date = datetime.fromisoformat(str(data['week_start_date']))
                except:
                    pass
            
            # If still no week_start, use current week
            if not week_start_date:
                today = datetime.now()
                week_start_date = today - timedelta(days=today.weekday())
            
            # Import models
            from app.models.feedback import Feedback, SentimentAnalysis, FeedbackCategory, CategoryMapping
            
            feedback = Feedback(
                trainee_id=data.get('trainee_id', ''),
                location=data.get('location', ''),
                training_batch=data.get('training_batch', ''),
                rating_score=data.get('rating_score'),
                open_text=data.get('open_text', ''),
                week_start_date=week_start_date
            )
            db.add(feedback)
            db.flush()
            
            # Perform sentiment analysis
            sentiment_result = analyzer.analyze(data.get('open_text', ''))
            sentiment_analysis = SentimentAnalysis(
                feedback_id=feedback.id,
                sentiment_category=sentiment_result['sentiment'],
                confidence_score=sentiment_result['confidence'],
                emotional_tone=sentiment_result.get('emotional_tone')
            )
            db.add(sentiment_analysis)
            
            # Map categories
            categories = category_mapper.map_categories(data.get('open_text', ''), data.get('category_tags'))
            for cat, keywords in categories.items():
                category_mapping = CategoryMapping(
                    feedback_id=feedback.id,
                    category=FeedbackCategory(cat),
                    keywords_matched=keywords
                )
                db.add(category_mapping)
            
            processed_count += 1
        
        db.commit()
        
        return {
            "message": "Feedback data synced successfully",
            "processed_count": processed_count,
            "week_start": week_start_date.isoformat() if week_start_date else None
        }
    
    except Exception as e:
        logger.error(f"Error syncing feedback data: {e}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing file: {str(e)}"
        )


@router.get("/status")
async def get_sync_status(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get sync status and last sync time"""
    from app.models.feedback import Feedback
    from sqlalchemy import func
    
    # Get last feedback entry
    last_feedback = db.query(Feedback).order_by(Feedback.created_at.desc()).first()
    
    # Get total feedback count
    total_count = db.query(func.count(Feedback.id)).scalar()
    
    return {
        "last_sync": last_feedback.created_at.isoformat() if last_feedback else None,
        "total_feedback_count": total_count or 0,
        "status": "active"
    }

