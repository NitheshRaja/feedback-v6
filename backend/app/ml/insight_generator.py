"""
AI-powered insight generation engine
"""
from typing import List, Dict, Optional
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import func, and_
from app.models.feedback import Feedback, SentimentAnalysis, FeedbackCategory, SentimentCategory
from app.models.report import ActionItem, ActionPriority
import logging

logger = logging.getLogger(__name__)


class InsightGenerator:
    """Generate actionable insights, risk flags, and recommendations"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def generate_action_items(
        self,
        week_start: datetime,
        week_end: datetime,
        previous_week_start: Optional[datetime] = None
    ) -> List[Dict]:
        """Generate actionable recommendations"""
        action_items = []
        
        # Get current week feedback
        current_feedback = self.db.query(Feedback).filter(
            and_(
                Feedback.week_start_date >= week_start,
                Feedback.week_start_date <= week_end
            )
        ).all()
        
        # Analyze by category
        category_issues = {}
        for feedback in current_feedback:
            if feedback.sentiment_analysis and feedback.sentiment_analysis.sentiment_category == SentimentCategory.NEGATIVE:
                for mapping in feedback.category_mappings:
                    category = mapping.category.value
                    if category not in category_issues:
                        category_issues[category] = {
                            "count": 0,
                            "keywords": set(),
                            "examples": []
                        }
                    category_issues[category]["count"] += 1
                    if mapping.keywords_matched:
                        category_issues[category]["keywords"].update(mapping.keywords_matched)
                    if len(category_issues[category]["examples"]) < 3:
                        category_issues[category]["examples"].append(feedback.open_text[:200])
        
        # Generate action items based on issue frequency
        for category, data in category_issues.items():
            if data["count"] >= 5:  # Threshold for action item
                priority = ActionPriority.URGENT if data["count"] >= 15 else ActionPriority.HIGH
                
                # Generate description based on keywords
                keywords_str = ", ".join(list(data["keywords"])[:5])
                description = f"Address {data['count']} negative feedback items in {category.replace('_', ' ').title()}. "
                description += f"Common themes: {keywords_str}."
                
                # Assign owner based on category
                owner_map = {
                    "trainer_feedback": "Training Team Lead",
                    "mentor_support": "Mentor Program Manager",
                    "batch_owner_experience": "Batch Owner",
                    "infrastructure": "IT Support Team",
                    "training_program": "Curriculum Team",
                    "engagement_experience": "Engagement Team"
                }
                assigned_to = owner_map.get(category.lower().replace(' ', '_'), "TBD")
                
                action_items.append({
                    "priority": priority.value,
                    "category": category,
                    "title": f"Address {category.replace('_', ' ').title()} Concerns",
                    "description": description,
                    "confidence_score": min(data["count"] / 20.0, 1.0),
                    "assigned_to": assigned_to
                })
        
        # Compare with previous week for trend-based actions
        if previous_week_start:
            prev_week_end = previous_week_start + timedelta(days=7)
            prev_feedback = self.db.query(Feedback).filter(
                and_(
                    Feedback.week_start_date >= previous_week_start,
                    Feedback.week_start_date <= prev_week_end
                )
            ).all()
            
            # Calculate sentiment change
            current_negative = sum(1 for f in current_feedback 
                                 if f.sentiment_analysis and 
                                 f.sentiment_analysis.sentiment_category == SentimentCategory.NEGATIVE)
            prev_negative = sum(1 for f in prev_feedback 
                              if f.sentiment_analysis and 
                              f.sentiment_analysis.sentiment_category == SentimentCategory.NEGATIVE)
            
            if prev_negative > 0:
                change_pct = ((current_negative - prev_negative) / prev_negative) * 100
                if change_pct > 15:  # Significant increase
                    action_items.append({
                        "priority": ActionPriority.URGENT.value,
                        "category": "overall",
                        "title": "Urgent: Significant Sentiment Drop Detected",
                        "description": f"Negative sentiment increased by {change_pct:.1f}% compared to last week. "
                                    f"Immediate investigation required.",
                        "confidence_score": 0.9,
                        "assigned_to": "Leadership Team"
                    })
        
        return action_items
    
    def generate_risk_flags(
        self,
        week_start: datetime,
        week_end: datetime
    ) -> List[Dict]:
        """Generate risk flags and alerts"""
        risk_flags = []
        
        # Get feedback with repeated keywords
        feedback_list = self.db.query(Feedback).filter(
            and_(
                Feedback.week_start_date >= week_start,
                Feedback.week_start_date <= week_end
            )
        ).all()
        
        # Track keyword frequency
        keyword_frequency = {}
        for feedback in feedback_list:
            if feedback.sentiment_analysis and feedback.sentiment_analysis.sentiment_category == SentimentCategory.NEGATIVE:
                for mapping in feedback.category_mappings:
                    if mapping.keywords_matched:
                        for keyword in mapping.keywords_matched:
                            keyword_frequency[keyword] = keyword_frequency.get(keyword, 0) + 1
        
        # Flag repeated keywords
        for keyword, count in keyword_frequency.items():
            if count >= 20:  # Threshold for risk flag
                risk_flags.append({
                    "type": "repeated_keyword",
                    "severity": "high" if count >= 30 else "medium",
                    "message": f"Keyword '{keyword}' mentioned {count} times in negative feedback",
                    "category": "pattern_detection",
                    "recommendation": f"Investigate and address issues related to '{keyword}'"
                })
        
        # Check for unresolved issues (negative sentiment for multiple weeks)
        # This would require querying previous weeks - simplified here
        negative_count = sum(1 for f in feedback_list 
                           if f.sentiment_analysis and 
                           f.sentiment_analysis.sentiment_category == SentimentCategory.NEGATIVE)
        total_count = len(feedback_list)
        
        if total_count > 0:
            negative_pct = (negative_count / total_count) * 100
            if negative_pct > 40:  # High negative percentage
                risk_flags.append({
                    "type": "high_negative_sentiment",
                    "severity": "high",
                    "message": f"High negative sentiment: {negative_pct:.1f}% of feedback is negative",
                    "category": "sentiment_analysis",
                    "recommendation": "Immediate intervention required. Review top concerns and take action."
                })
        
        return risk_flags
    
    def detect_assessment_stress(
        self,
        week_start: datetime,
        week_end: datetime
    ) -> Optional[Dict]:
        """Detect assessment stress patterns"""
        stress_keywords = ["pressure", "difficult", "revision", "exam", "assessment", "stress", "anxious"]
        
        feedback_list = self.db.query(Feedback).filter(
            and_(
                Feedback.week_start_date >= week_start,
                Feedback.week_start_date <= week_end
            )
        ).all()
        
        stress_mentions = 0
        total_feedback = len(feedback_list)
        
        for feedback in feedback_list:
            text_lower = feedback.open_text.lower()
            if any(keyword in text_lower for keyword in stress_keywords):
                stress_mentions += 1
        
        if stress_mentions >= 10 and total_feedback > 0:
            stress_pct = (stress_mentions / total_feedback) * 100
            if stress_pct > 20:  # 20% of feedback mentions stress
                return {
                    "detected": True,
                    "confidence": min(stress_pct / 50.0, 1.0),
                    "message": f"Assessment stress pattern detected. {stress_mentions} mentions of stress-related keywords.",
                    "recommendation": "Consider pre-assessment support workshop or stress management session."
                }
        
        return None
    
    def generate_top_strengths_and_concerns(
        self,
        week_start: datetime,
        week_end: datetime
    ) -> Dict[str, List[Dict]]:
        """Generate top strengths and concerns from actual feedback data with supporting quotes"""
        feedback_list = self.db.query(Feedback).filter(
            and_(
                Feedback.week_start_date >= week_start,
                Feedback.week_start_date <= week_end
            )
        ).all()
        
        # Analyze positive feedback for strengths
        positive_feedback = [f for f in feedback_list 
                           if f.sentiment_analysis and 
                           f.sentiment_analysis.sentiment_category == SentimentCategory.POSITIVE]
        
        # Analyze negative feedback for concerns
        negative_feedback = [f for f in feedback_list 
                           if f.sentiment_analysis and 
                           f.sentiment_analysis.sentiment_category == SentimentCategory.NEGATIVE]
        
        # Count category mentions in positive feedback with quotes
        strength_categories = {}
        for feedback in positive_feedback:
            for mapping in feedback.category_mappings:
                category = mapping.category.value.replace('_', ' ').title()
                if category not in strength_categories:
                    strength_categories[category] = {
                        'count': 0,
                        'quotes': []
                    }
                strength_categories[category]['count'] += 1
                # Collect quotes (max 2 per category)
                if len(strength_categories[category]['quotes']) < 2:
                    quote = feedback.open_text[:200] + "..." if len(feedback.open_text) > 200 else feedback.open_text
                    strength_categories[category]['quotes'].append(quote)
        
        # Count category mentions in negative feedback with quotes
        concern_categories = {}
        for feedback in negative_feedback:
            for mapping in feedback.category_mappings:
                category = mapping.category.value.replace('_', ' ').title()
                if category not in concern_categories:
                    concern_categories[category] = {
                        'count': 0,
                        'quotes': []
                    }
                concern_categories[category]['count'] += 1
                # Collect quotes (max 2 per category)
                if len(concern_categories[category]['quotes']) < 2:
                    quote = feedback.open_text[:200] + "..." if len(feedback.open_text) > 200 else feedback.open_text
                    concern_categories[category]['quotes'].append(quote)
        
        # Get top 3 strengths with quotes
        top_strengths = sorted(
            strength_categories.items(),
            key=lambda x: x[1]['count'],
            reverse=True
        )[:3]
        top_strengths_list = [
            {
                'category': cat,
                'description': f"{cat} received {data['count']} positive mentions",
                'quotes': data['quotes']
            }
            for cat, data in top_strengths
        ]
        
        # Get top 3 concerns with quotes
        top_concerns = sorted(
            concern_categories.items(),
            key=lambda x: x[1]['count'],
            reverse=True
        )[:3]
        top_concerns_list = [
            {
                'category': cat,
                'description': f"{cat} received {data['count']} negative mentions",
                'quotes': data['quotes']
            }
            for cat, data in top_concerns
        ]
        
        # If no data, provide defaults
        if not top_strengths_list:
            top_strengths_list = [{
                'category': 'General',
                'description': 'No positive feedback patterns detected',
                'quotes': []
            }]
        if not top_concerns_list:
            top_concerns_list = [{
                'category': 'General',
                'description': 'No major concerns identified',
                'quotes': []
            }]
        
        return {
            "strengths": top_strengths_list,
            "concerns": top_concerns_list
        }
    
    def generate_executive_summary(
        self,
        week_start: datetime,
        week_end: datetime,
        overall_sentiment: float,
        sentiment_change: Optional[float],
        top_strengths: List[Dict],
        top_concerns: List[Dict]
    ) -> str:
        """Generate human-readable executive summary with supporting quotes"""
        summary = f"Week: {week_start.strftime('%b %d')} - {week_end.strftime('%b %d, %Y')}\n\n"
        summary += f"Overall Sentiment Score: {overall_sentiment:.0f}"
        
        if sentiment_change:
            change_str = f"+{sentiment_change:.1f}%" if sentiment_change > 0 else f"{sentiment_change:.1f}%"
            summary += f" ({change_str} from last week)\n\n"
        else:
            summary += "\n\n"
        
        summary += "Top Strengths:\n"
        for i, strength in enumerate(top_strengths[:3], 1):
            summary += f"{i}. {strength.get('category', 'General')}: {strength.get('description', '')}\n"
            if strength.get('quotes') and len(strength['quotes']) > 0:
                summary += f"   Quote: \"{strength['quotes'][0][:100]}...\"\n"
        
        summary += "\nTop Concerns:\n"
        for i, concern in enumerate(top_concerns[:3], 1):
            summary += f"{i}. {concern.get('category', 'General')}: {concern.get('description', '')}\n"
            if concern.get('quotes') and len(concern['quotes']) > 0:
                summary += f"   Quote: \"{concern['quotes'][0][:100]}...\"\n"
        
        return summary
    
    def generate_appreciation_tracker(
        self,
        week_start: datetime,
        week_end: datetime
    ) -> Dict:
        """Generate appreciation tracker with positive feedback highlights and trainer/mentor recognition"""
        feedback_list = self.db.query(Feedback).filter(
            and_(
                Feedback.week_start_date >= week_start,
                Feedback.week_start_date <= week_end
            )
        ).all()
        
        # Filter positive feedback
        positive_feedback = [f for f in feedback_list 
                           if f.sentiment_analysis and 
                           f.sentiment_analysis.sentiment_category == SentimentCategory.POSITIVE]
        
        # Extract appreciation keywords
        appreciation_keywords = [
            "thank", "appreciate", "great", "excellent", "helpful", "supportive",
            "amazing", "wonderful", "fantastic", "outstanding", "brilliant"
        ]
        
        trainer_mentions = []
        mentor_mentions = []
        general_appreciation = []
        
        for feedback in positive_feedback:
            text_lower = feedback.open_text.lower()
            
            # Check for appreciation keywords
            has_appreciation = any(keyword in text_lower for keyword in appreciation_keywords)
            
            if has_appreciation:
                # Check for trainer mentions
                trainer_keywords = ["trainer", "instructor", "teacher", "faculty"]
                if any(keyword in text_lower for keyword in trainer_keywords):
                    trainer_mentions.append({
                        "text": feedback.open_text[:200] + "..." if len(feedback.open_text) > 200 else feedback.open_text,
                        "location": feedback.location,
                        "batch": feedback.training_batch
                    })
                
                # Check for mentor mentions
                mentor_keywords = ["mentor", "guide", "coach"]
                if any(keyword in text_lower for keyword in mentor_keywords):
                    mentor_mentions.append({
                        "text": feedback.open_text[:200] + "..." if len(feedback.open_text) > 200 else feedback.open_text,
                        "location": feedback.location,
                        "batch": feedback.training_batch
                    })
                
                # General appreciation
                if len(general_appreciation) < 5:
                    general_appreciation.append({
                        "text": feedback.open_text[:200] + "..." if len(feedback.open_text) > 200 else feedback.open_text,
                        "location": feedback.location,
                        "batch": feedback.training_batch
                    })
        
        return {
            "trainer_recognition": trainer_mentions[:5],  # Top 5
            "mentor_recognition": mentor_mentions[:5],  # Top 5
            "general_appreciation": general_appreciation[:5],  # Top 5
            "total_positive_feedback": len(positive_feedback)
        }
    
    def detect_unresolved_feedback_loops(
        self,
        week_start: datetime,
        week_end: datetime,
        weeks_to_check: int = 3
    ) -> List[Dict]:
        """Detect unresolved feedback loops (negative sentiment for 3+ consecutive weeks)"""
        unresolved_loops = []
        
        # Check each week going back
        for week_offset in range(weeks_to_check):
            check_week_start = week_start - timedelta(weeks=week_offset)
            check_week_end = check_week_start + timedelta(days=6)
            
            feedback_list = self.db.query(Feedback).filter(
                and_(
                    Feedback.week_start_date >= check_week_start,
                    Feedback.week_start_date <= check_week_end
                )
            ).all()
            
            if not feedback_list:
                continue
            
            # Calculate negative sentiment percentage
            negative_count = sum(1 for f in feedback_list 
                               if f.sentiment_analysis and 
                               f.sentiment_analysis.sentiment_category == SentimentCategory.NEGATIVE)
            total = len(feedback_list)
            negative_pct = (negative_count / total * 100) if total > 0 else 0
            
            # If negative sentiment > 40% for this week, track it
            if negative_pct > 40:
                # Group by category to find recurring issues
                category_issues = {}
                for feedback in feedback_list:
                    if feedback.sentiment_analysis and feedback.sentiment_analysis.sentiment_category == SentimentCategory.NEGATIVE:
                        for mapping in feedback.category_mappings:
                            category = mapping.category.value
                            if category not in category_issues:
                                category_issues[category] = 0
                            category_issues[category] += 1
                
                # Find most common issue category
                if category_issues:
                    top_category = max(category_issues.items(), key=lambda x: x[1])
                    unresolved_loops.append({
                        "week": check_week_start.isoformat(),
                        "negative_percentage": negative_pct,
                        "top_category": top_category[0],
                        "category_count": top_category[1],
                        "total_feedback": total
                    })
        
        # If we have 3+ weeks with high negative sentiment, flag it
        if len(unresolved_loops) >= 3:
            return [{
                "detected": True,
                "weeks_affected": len(unresolved_loops),
                "message": f"Unresolved feedback loop detected: {len(unresolved_loops)} consecutive weeks with high negative sentiment (>40%)",
                "details": unresolved_loops,
                "recommendation": "Immediate intervention required. Review recurring issues and implement corrective actions."
            }]
        
        return []
    
    def track_praise_momentum(
        self,
        week_start: datetime,
        week_end: datetime,
        weeks_back: int = 4
    ) -> Dict:
        """Track praise momentum - increasing positive feedback trends"""
        momentum_data = []
        
        for week_offset in range(weeks_back):
            check_week_start = week_start - timedelta(weeks=week_offset)
            check_week_end = check_week_start + timedelta(days=6)
            
            feedback_list = self.db.query(Feedback).filter(
                and_(
                    Feedback.week_start_date >= check_week_start,
                    Feedback.week_start_date <= check_week_end
                )
            ).all()
            
            if not feedback_list:
                continue
            
            # Count positive feedback
            positive_count = sum(1 for f in feedback_list 
                               if f.sentiment_analysis and 
                               f.sentiment_analysis.sentiment_category == SentimentCategory.POSITIVE)
            total = len(feedback_list)
            positive_pct = (positive_count / total * 100) if total > 0 else 0
            
            # Track trainer/mentor mentions
            trainer_mentions = 0
            mentor_mentions = 0
            for feedback in feedback_list:
                if feedback.sentiment_analysis and feedback.sentiment_analysis.sentiment_category == SentimentCategory.POSITIVE:
                    text_lower = feedback.open_text.lower()
                    if "trainer" in text_lower or "instructor" in text_lower:
                        trainer_mentions += 1
                    if "mentor" in text_lower or "guide" in text_lower:
                        mentor_mentions += 1
            
            momentum_data.append({
                "week": check_week_start.isoformat(),
                "positive_percentage": positive_pct,
                "positive_count": positive_count,
                "total_feedback": total,
                "trainer_mentions": trainer_mentions,
                "mentor_mentions": mentor_mentions
            })
        
        # Calculate trend
        if len(momentum_data) >= 2:
            recent_positive = momentum_data[0]["positive_percentage"]
            previous_positive = momentum_data[1]["positive_percentage"] if len(momentum_data) > 1 else 0
            trend = "increasing" if recent_positive > previous_positive else "decreasing"
            change = recent_positive - previous_positive
        else:
            trend = "stable"
            change = 0
        
        return {
            "trend": trend,
            "change": change,
            "current_positive_pct": momentum_data[0]["positive_percentage"] if momentum_data else 0,
            "weeks_data": momentum_data,
            "trainer_recognition_trend": "increasing" if momentum_data and momentum_data[0]["trainer_mentions"] > (momentum_data[1]["trainer_mentions"] if len(momentum_data) > 1 else 0) else "stable",
            "mentor_recognition_trend": "increasing" if momentum_data and momentum_data[0]["mentor_mentions"] > (momentum_data[1]["mentor_mentions"] if len(momentum_data) > 1 else 0) else "stable"
        }

