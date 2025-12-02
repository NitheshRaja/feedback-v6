"""
Report generation endpoints
"""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import Optional
from app.core.database import get_db
from app.core.config import settings
from app.api.v1.endpoints.auth import get_current_user
from app.models.user import User
from app.models.feedback import Feedback, SentimentAnalysis, SentimentCategory
from app.models.report import WeeklyReport, ActionItem, ActionPriority, ActionStatus
from app.services.trend_analyzer import TrendAnalyzer
from app.services.heat_index_calculator import HeatIndexCalculator
from app.services.pdf_generator import PDFGenerator
from app.ml.insight_generator import InsightGenerator
from pydantic import BaseModel
import os

router = APIRouter()


class WeeklyReportResponse(BaseModel):
    id: int
    week_start_date: datetime
    week_end_date: datetime
    overall_sentiment_score: float
    sentiment_change: Optional[float]
    heat_index: float
    total_feedback_count: int
    executive_summary: Optional[str]
    
    class Config:
        from_attributes = True


@router.post("/weekly/generate")
async def generate_weekly_report(
    week_start: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Generate weekly sentiment analysis report"""
    # Parse week_start if it's a string
    if isinstance(week_start, str):
        try:
            week_start = datetime.fromisoformat(week_start.replace('Z', '+00:00'))
        except:
            # Try parsing as date string
            try:
                week_start = datetime.strptime(week_start, '%Y-%m-%d')
            except:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Invalid week_start format. Use ISO format or YYYY-MM-DD"
                )
    
    # If no week_start provided, use current week
    if week_start is None:
        today = datetime.now()
        week_start = today - timedelta(days=today.weekday())
    
    week_end = week_start + timedelta(days=6)
    previous_week_start = week_start - timedelta(days=7)
    previous_week_end = previous_week_start + timedelta(days=6)
    
    # Get feedback for the week
    feedback_list = db.query(Feedback).filter(
        Feedback.week_start_date >= week_start,
        Feedback.week_start_date <= week_end
    ).all()
    
    if not feedback_list:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No feedback found for the specified week"
        )
    
    # Calculate sentiment distribution
    total = len(feedback_list)
    positive = sum(1 for f in feedback_list 
                  if f.sentiment_analysis and 
                  f.sentiment_analysis.sentiment_category == SentimentCategory.POSITIVE)
    neutral = sum(1 for f in feedback_list 
                 if f.sentiment_analysis and 
                 f.sentiment_analysis.sentiment_category == SentimentCategory.NEUTRAL)
    negative = sum(1 for f in feedback_list 
                  if f.sentiment_analysis and 
                  f.sentiment_analysis.sentiment_category == SentimentCategory.NEGATIVE)
    
    overall_sentiment = (positive / total * 100) if total > 0 else 0
    
    # Calculate week-over-week change
    prev_feedback = db.query(Feedback).filter(
        Feedback.week_start_date >= previous_week_start,
        Feedback.week_start_date <= previous_week_end
    ).all()
    prev_total = len(prev_feedback)
    prev_positive = sum(1 for f in prev_feedback 
                       if f.sentiment_analysis and 
                       f.sentiment_analysis.sentiment_category == SentimentCategory.POSITIVE)
    prev_sentiment = (prev_positive / prev_total * 100) if prev_total > 0 else 0
    sentiment_change = overall_sentiment - prev_sentiment if prev_total > 0 else None
    
    # Calculate heat index
    calculator = HeatIndexCalculator()
    heat_index = calculator.calculate(feedback_list)
    
    # Generate insights
    generator = InsightGenerator(db)
    action_items_data = generator.generate_action_items(
        week_start, week_end, previous_week_start
    )
    
    # Generate top strengths and concerns from actual data
    strengths_concerns = generator.generate_top_strengths_and_concerns(week_start, week_end)
    top_strengths = strengths_concerns["strengths"]
    top_concerns = strengths_concerns["concerns"]
    
    executive_summary = generator.generate_executive_summary(
        week_start, week_end, overall_sentiment, sentiment_change,
        top_strengths, top_concerns
    )
    
    # Create or update report
    existing_report = db.query(WeeklyReport).filter(
        WeeklyReport.week_start_date == week_start
    ).first()
    
    if existing_report:
        existing_report.overall_sentiment_score = overall_sentiment
        existing_report.sentiment_change = sentiment_change
        existing_report.heat_index = heat_index
        existing_report.total_feedback_count = total
        existing_report.positive_count = positive
        existing_report.neutral_count = neutral
        existing_report.negative_count = negative
        existing_report.executive_summary = executive_summary
        report = existing_report
    else:
        report = WeeklyReport(
            week_start_date=week_start,
            week_end_date=week_end,
            overall_sentiment_score=overall_sentiment,
            sentiment_change=sentiment_change,
            heat_index=heat_index,
            total_feedback_count=total,
            positive_count=positive,
            neutral_count=neutral,
            negative_count=negative,
            executive_summary=executive_summary
        )
        db.add(report)
        db.flush()
    
    # Create action items
    for item_data in action_items_data:
        action_item = ActionItem(
            report_id=report.id,
            priority=ActionPriority(item_data["priority"]),
            category=item_data.get("category"),
            title=item_data["title"],
            description=item_data["description"],
            confidence_score=item_data.get("confidence_score"),
            assigned_to=item_data.get("assigned_to")
        )
        db.add(action_item)
    
    db.commit()
    db.refresh(report)
    
    return report


@router.get("/weekly/{week_id}", response_model=WeeklyReportResponse)
async def get_weekly_report(
    week_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get weekly report by ID"""
    report = db.query(WeeklyReport).filter(WeeklyReport.id == week_id).first()
    
    if not report:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Report not found"
        )
    
    return report


@router.get("/weekly")
async def list_weekly_reports(
    skip: int = 0,
    limit: int = 10,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """List weekly reports"""
    reports = db.query(WeeklyReport).order_by(
        WeeklyReport.week_start_date.desc()
    ).offset(skip).limit(limit).all()
    
    return reports


@router.get("/export/pdf/{week_id}")
async def export_pdf_report(
    week_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Export weekly report as PDF"""
    report = db.query(WeeklyReport).filter(WeeklyReport.id == week_id).first()
    
    if not report:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Report not found"
        )
    
    # Generate PDF
    pdf_dir = os.path.join(settings.UPLOAD_DIR, "pdfs")
    os.makedirs(pdf_dir, exist_ok=True)
    
    pdf_filename = f"report_{week_id}_{report.week_start_date.strftime('%Y%m%d')}.pdf"
    pdf_path = os.path.join(pdf_dir, pdf_filename)
    
    generator = PDFGenerator(db)
    generator.generate_pdf(report, pdf_path)
    
    # Update report with PDF path
    report.pdf_path = pdf_path
    db.commit()
    
    # Return file
    return FileResponse(
        pdf_path,
        media_type="application/pdf",
        filename=pdf_filename
    )

