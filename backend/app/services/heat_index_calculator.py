"""
Engagement Heat Index Calculator
"""
from typing import List
from app.models.feedback import Feedback, SentimentAnalysis, SentimentCategory
import logging

logger = logging.getLogger(__name__)


class HeatIndexCalculator:
    """Calculate engagement heat index (0-100)"""
    
    ENGAGEMENT_KEYWORDS = [
        "engaged", "participate", "interactive", "involved", "active",
        "contribute", "collaborate", "teamwork", "discussion", "feedback"
    ]
    
    def calculate(self, feedback_list: List[Feedback]) -> float:
        """
        Calculate heat index based on:
        - Positive sentiment % (40%)
        - Average rating score (30%)
        - Participation volume (20%)
        - Engagement keywords (10%)
        """
        if not feedback_list:
            return 0.0
        
        total_count = len(feedback_list)
        
        # 1. Sentiment Score (40%)
        positive_count = sum(1 for f in feedback_list 
                           if f.sentiment_analysis and 
                           f.sentiment_analysis.sentiment_category == SentimentCategory.POSITIVE)
        sentiment_score = (positive_count / total_count) * 40 if total_count > 0 else 0
        
        # 2. Rating Score (30%)
        ratings = [f.rating_score for f in feedback_list if f.rating_score is not None]
        if ratings:
            avg_rating = sum(ratings) / len(ratings)
            rating_score = (avg_rating / 5.0) * 30
        else:
            rating_score = 15  # Default to middle if no ratings
        
        # 3. Participation Volume Score (20%)
        # Normalize based on expected volume (assuming 50+ is good)
        volume_score = min((total_count / 50.0) * 20, 20) if total_count > 0 else 0
        
        # 4. Engagement Keywords Score (10%)
        engagement_mentions = 0
        for feedback in feedback_list:
            text_lower = feedback.open_text.lower()
            for keyword in self.ENGAGEMENT_KEYWORDS:
                if keyword in text_lower:
                    engagement_mentions += 1
                    break  # Count once per feedback
        
        keyword_score = min((engagement_mentions / total_count) * 10, 10) if total_count > 0 else 0
        
        # Total heat index
        heat_index = sentiment_score + rating_score + volume_score + keyword_score
        
        return min(max(heat_index, 0.0), 100.0)  # Clamp between 0-100




