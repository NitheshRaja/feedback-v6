"""
Trend analysis service
"""
from typing import List, Dict, Optional
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import func, and_
from app.models.feedback import Feedback, SentimentAnalysis, SentimentCategory, TraineeStage
from app.models.report import TrendData
import logging

logger = logging.getLogger(__name__)


class TrendAnalyzer:
    """Analyze trends and generate comparisons"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def calculate_week_over_week_change(
        self,
        current_week_start: datetime,
        current_week_end: datetime,
        previous_week_start: datetime,
        previous_week_end: datetime
    ) -> Dict:
        """Calculate week-over-week sentiment change"""
        # Current week data
        current_feedback = self.db.query(Feedback).filter(
            and_(
                Feedback.week_start_date >= current_week_start,
                Feedback.week_start_date <= current_week_end
            )
        ).all()
        
        # Previous week data
        previous_feedback = self.db.query(Feedback).filter(
            and_(
                Feedback.week_start_date >= previous_week_start,
                Feedback.week_start_date <= previous_week_end
            )
        ).all()
        
        # Calculate sentiment percentages
        current_sentiment = self._calculate_sentiment_distribution(current_feedback)
        previous_sentiment = self._calculate_sentiment_distribution(previous_feedback)
        
        # Calculate changes
        changes = {}
        for sentiment in ["positive", "neutral", "negative"]:
            current_pct = current_sentiment.get(sentiment, 0)
            previous_pct = previous_sentiment.get(sentiment, 0)
            if previous_pct > 0:
                change = ((current_pct - previous_pct) / previous_pct) * 100
            else:
                change = 0 if current_pct == 0 else 100
            changes[sentiment] = change
        
        # Overall sentiment score change
        current_overall = current_sentiment.get("positive", 0)
        previous_overall = previous_sentiment.get("positive", 0)
        overall_change = current_overall - previous_overall
        
        return {
            "current_week": current_sentiment,
            "previous_week": previous_sentiment,
            "changes": changes,
            "overall_change": overall_change,
            "current_volume": len(current_feedback),
            "previous_volume": len(previous_feedback),
            "volume_change": len(current_feedback) - len(previous_feedback)
        }
    
    def _calculate_sentiment_distribution(self, feedback_list: List[Feedback]) -> Dict:
        """Calculate sentiment distribution from feedback list"""
        total = len(feedback_list)
        if total == 0:
            return {"positive": 0, "neutral": 0, "negative": 0}
        
        positive = sum(1 for f in feedback_list 
                      if f.sentiment_analysis and 
                      f.sentiment_analysis.sentiment_category == SentimentCategory.POSITIVE)
        neutral = sum(1 for f in feedback_list 
                     if f.sentiment_analysis and 
                     f.sentiment_analysis.sentiment_category == SentimentCategory.NEUTRAL)
        negative = sum(1 for f in feedback_list 
                      if f.sentiment_analysis and 
                      f.sentiment_analysis.sentiment_category == SentimentCategory.NEGATIVE)
        
        return {
            "positive": (positive / total) * 100,
            "neutral": (neutral / total) * 100,
            "negative": (negative / total) * 100
        }
    
    def get_category_trends(
        self,
        week_start: datetime,
        week_end: datetime,
        weeks_back: int = 8
    ) -> Dict:
        """Get category-wise trends for specified weeks"""
        trends = {}
        
        for i in range(weeks_back):
            week_start_date = week_start - timedelta(weeks=i)
            week_end_date = week_end - timedelta(weeks=i)
            
            feedback = self.db.query(Feedback).filter(
                and_(
                    Feedback.week_start_date >= week_start_date,
                    Feedback.week_start_date <= week_end_date
                )
            ).all()
            
            # Group by category
            category_sentiment = {}
            for f in feedback:
                for mapping in f.category_mappings:
                    category = mapping.category.value
                    if category not in category_sentiment:
                        category_sentiment[category] = {"positive": 0, "neutral": 0, "negative": 0, "total": 0}
                    
                    if f.sentiment_analysis:
                        sentiment = f.sentiment_analysis.sentiment_category.value
                        category_sentiment[category][sentiment] += 1
                        category_sentiment[category]["total"] += 1
            
            # Calculate percentages
            for category, counts in category_sentiment.items():
                if category not in trends:
                    trends[category] = []
                
                total = counts["total"]
                if total > 0:
                    trends[category].append({
                        "week": week_start_date.isoformat(),
                        "positive": (counts["positive"] / total) * 100,
                        "neutral": (counts["neutral"] / total) * 100,
                        "negative": (counts["negative"] / total) * 100,
                        "volume": total
                    })
        
        return trends
    
    def get_lifecycle_trends(
        self,
        week_start: datetime,
        week_end: datetime
    ) -> Dict:
        """Get sentiment trends by trainee lifecycle stage"""
        feedback = self.db.query(Feedback).filter(
            and_(
                Feedback.week_start_date >= week_start,
                Feedback.week_start_date <= week_end
            )
        ).all()
        
        stage_sentiment = {}
        for f in feedback:
            stage = f.trainee_stage.value if f.trainee_stage else "unknown"
            if stage not in stage_sentiment:
                stage_sentiment[stage] = {"positive": 0, "neutral": 0, "negative": 0, "total": 0}
            
            if f.sentiment_analysis:
                sentiment = f.sentiment_analysis.sentiment_category.value
                stage_sentiment[stage][sentiment] += 1
                stage_sentiment[stage]["total"] += 1
        
        # Calculate percentages
        result = {}
        for stage, counts in stage_sentiment.items():
            total = counts["total"]
            if total > 0:
                result[stage] = {
                    "positive": (counts["positive"] / total) * 100,
                    "neutral": (counts["neutral"] / total) * 100,
                    "negative": (counts["negative"] / total) * 100,
                    "volume": total
                }
        
        return result




