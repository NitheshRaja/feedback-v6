"""
Sentiment analysis and insights endpoints
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import Optional
from app.core.database import get_db
from app.api.v1.endpoints.auth import get_current_user
from app.models.user import User
from app.models.feedback import Feedback
from app.ml.insight_generator import InsightGenerator
from app.services.trend_analyzer import TrendAnalyzer
from app.services.heat_index_calculator import HeatIndexCalculator
from pydantic import BaseModel

router = APIRouter()


class TrendResponse(BaseModel):
    current_week: dict
    previous_week: dict
    changes: dict
    overall_change: float
    current_volume: int
    previous_volume: int
    volume_change: int


class InsightResponse(BaseModel):
    action_items: list
    risk_flags: list
    assessment_stress: Optional[dict]
    executive_summary: str


@router.get("/trends", response_model=TrendResponse)
async def get_trends(
    week_start: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get week-over-week trend analysis"""
    # Parse week_start if it's a string, or use current week
    if week_start:
        try:
            week_start = datetime.fromisoformat(week_start.replace('Z', '+00:00'))
        except:
            try:
                week_start = datetime.strptime(week_start, '%Y-%m-%d')
            except:
                # Default to current week if parsing fails
                today = datetime.now()
                week_start = today - timedelta(days=today.weekday())
    else:
        # Use current week if not provided
        today = datetime.now()
        week_start = today - timedelta(days=today.weekday())
    
    week_end = week_start + timedelta(days=6)
    previous_week_start = week_start - timedelta(days=7)
    previous_week_end = previous_week_start + timedelta(days=6)
    
    analyzer = TrendAnalyzer(db)
    trends = analyzer.calculate_week_over_week_change(
        week_start, week_end, previous_week_start, previous_week_end
    )
    
    return trends


@router.get("/insights")
async def get_insights(
    week_start: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get actionable insights and recommendations"""
    # Parse week_start if it's a string, or use current week
    if week_start:
        try:
            week_start = datetime.fromisoformat(week_start.replace('Z', '+00:00'))
        except:
            try:
                week_start = datetime.strptime(week_start, '%Y-%m-%d')
            except:
                # Default to current week if parsing fails
                today = datetime.now()
                week_start = today - timedelta(days=today.weekday())
    else:
        # Use current week if not provided
        today = datetime.now()
        week_start = today - timedelta(days=today.weekday())
    
    week_end = week_start + timedelta(days=6)
    previous_week_start = week_start - timedelta(days=7)
    
    generator = InsightGenerator(db)
    
    # Generate action items
    action_items = generator.generate_action_items(
        week_start, week_end, previous_week_start
    )
    
    # Generate risk flags
    risk_flags = generator.generate_risk_flags(week_start, week_end)
    
    # Detect assessment stress
    assessment_stress = generator.detect_assessment_stress(week_start, week_end)
    
    # Get feedback for summary
    feedback_list = db.query(Feedback).filter(
        Feedback.week_start_date >= week_start,
        Feedback.week_start_date <= week_end
    ).all()
    
    # Calculate overall sentiment
    total = len(feedback_list)
    positive = sum(1 for f in feedback_list 
                  if f.sentiment_analysis and 
                  f.sentiment_analysis.sentiment_category.value == "positive")
    overall_sentiment = (positive / total * 100) if total > 0 else 0
    
    # Calculate sentiment change
    prev_feedback = db.query(Feedback).filter(
        Feedback.week_start_date >= previous_week_start,
        Feedback.week_start_date < week_start
    ).all()
    prev_total = len(prev_feedback)
    prev_positive = sum(1 for f in prev_feedback 
                       if f.sentiment_analysis and 
                       f.sentiment_analysis.sentiment_category.value == "positive")
    prev_sentiment = (prev_positive / prev_total * 100) if prev_total > 0 else 0
    sentiment_change = overall_sentiment - prev_sentiment if prev_total > 0 else None
    
    # Generate top strengths and concerns from actual data
    strengths_concerns = generator.generate_top_strengths_and_concerns(week_start, week_end)
    top_strengths = strengths_concerns["strengths"]
    top_concerns = strengths_concerns["concerns"]
    
    executive_summary = generator.generate_executive_summary(
        week_start, week_end, overall_sentiment, sentiment_change,
        top_strengths, top_concerns
    )
    
    # Generate appreciation tracker
    appreciation_tracker = generator.generate_appreciation_tracker(week_start, week_end)
    
    # Detect unresolved feedback loops
    unresolved_loops = generator.detect_unresolved_feedback_loops(week_start, week_end)
    
    # Track praise momentum
    praise_momentum = generator.track_praise_momentum(week_start, week_end)
    
    return {
        "action_items": action_items,
        "risk_flags": risk_flags,
        "assessment_stress": assessment_stress,
        "executive_summary": executive_summary,
        "appreciation_tracker": appreciation_tracker,
        "unresolved_loops": unresolved_loops,
        "praise_momentum": praise_momentum
    }


@router.get("/lifecycle")
async def get_lifecycle_trends(
    week_start: datetime,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get trainee lifecycle sentiment trends"""
    week_end = week_start + timedelta(days=6)
    
    analyzer = TrendAnalyzer(db)
    trends = analyzer.get_lifecycle_trends(week_start, week_end)
    
    return trends


@router.get("/category-trends")
async def get_category_trends(
    week_start: Optional[str] = None,
    weeks_back: int = 8,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get category-wise trends for 8 weeks"""
    # Parse week_start if it's a string
    if week_start:
        try:
            week_start = datetime.fromisoformat(week_start.replace('Z', '+00:00'))
        except:
            try:
                week_start = datetime.strptime(week_start, '%Y-%m-%d')
            except:
                today = datetime.now()
                week_start = today - timedelta(days=today.weekday())
    else:
        today = datetime.now()
        week_start = today - timedelta(days=today.weekday())
    
    week_end = week_start + timedelta(days=6)
    
    analyzer = TrendAnalyzer(db)
    trends = analyzer.get_category_trends(week_start, week_end, weeks_back)
    
    return trends


@router.get("/8-week-trends")
async def get_8_week_trends(
    week_start: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get 8-week sentiment trend data"""
    # Parse week_start if it's a string
    if week_start:
        try:
            week_start = datetime.fromisoformat(week_start.replace('Z', '+00:00'))
        except:
            try:
                week_start = datetime.strptime(week_start, '%Y-%m-%d')
            except:
                today = datetime.now()
                week_start = today - timedelta(days=today.weekday())
    else:
        today = datetime.now()
        week_start = today - timedelta(days=today.weekday())
    
    analyzer = TrendAnalyzer(db)
    trends = []
    
    for i in range(8):
        week_start_date = week_start - timedelta(weeks=i)
        week_end_date = week_start_date + timedelta(days=6)
        
        feedback = db.query(Feedback).filter(
            Feedback.week_start_date >= week_start_date,
            Feedback.week_start_date <= week_end_date
        ).all()
        
        if feedback:
            sentiment_dist = analyzer._calculate_sentiment_distribution(feedback)
            trends.append({
                "week": week_start_date.isoformat(),
                "week_label": week_start_date.strftime('%b %d'),
                "positive": sentiment_dist["positive"],
                "neutral": sentiment_dist["neutral"],
                "negative": sentiment_dist["negative"],
                "volume": len(feedback)
            })
    
    # Reverse to show oldest to newest
    trends.reverse()
    
    return {"trends": trends}


@router.get("/category-heatmap")
async def get_category_heatmap(
    week_start: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get category sentiment heatmap data"""
    # Parse week_start if it's a string
    if week_start:
        try:
            week_start = datetime.fromisoformat(week_start.replace('Z', '+00:00'))
        except:
            try:
                week_start = datetime.strptime(week_start, '%Y-%m-%d')
            except:
                today = datetime.now()
                week_start = today - timedelta(days=today.weekday())
    else:
        today = datetime.now()
        week_start = today - timedelta(days=today.weekday())
    
    week_end = week_start + timedelta(days=6)
    
    feedback_list = db.query(Feedback).filter(
        Feedback.week_start_date >= week_start,
        Feedback.week_start_date <= week_end
    ).all()
    
    # Group by category
    category_data = {}
    categories = [
        "trainer_feedback",
        "mentor_support",
        "batch_owner_experience",
        "infrastructure",
        "training_program",
        "engagement_experience"
    ]
    
    for category in categories:
        category_data[category] = {
            "positive": 0,
            "neutral": 0,
            "negative": 0,
            "total": 0
        }
    
    for feedback in feedback_list:
        for mapping in feedback.category_mappings:
            category = mapping.category.value
            if category in category_data:
                if feedback.sentiment_analysis:
                    sentiment = feedback.sentiment_analysis.sentiment_category.value
                    category_data[category][sentiment] += 1
                    category_data[category]["total"] += 1
    
    # Calculate sentiment scores for heatmap (0-100, where 100 is all positive)
    heatmap_data = []
    for category, data in category_data.items():
        if data["total"] > 0:
            positive_pct = (data["positive"] / data["total"]) * 100
            neutral_pct = (data["neutral"] / data["total"]) * 100
            negative_pct = (data["negative"] / data["total"]) * 100
            
            # Heat score: positive weighted more, negative weighted less
            heat_score = positive_pct * 1.0 + neutral_pct * 0.5 - negative_pct * 0.5
            heat_score = max(0, min(100, heat_score))  # Clamp to 0-100
            
            heatmap_data.append({
                "category": category.replace('_', ' ').title(),
                "positive": positive_pct,
                "neutral": neutral_pct,
                "negative": negative_pct,
                "heat_score": heat_score,
                "total": data["total"]
            })
    
    return {"heatmap": heatmap_data}

