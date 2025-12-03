"""
Category mapping engine for feedback classification
"""
from typing import List, Dict, Tuple
from app.models.feedback import FeedbackCategory
import re
import logging

logger = logging.getLogger(__name__)


class CategoryMapper:
    """Map feedback to relevant categories using keyword matching and NLP"""
    
    def __init__(self):
        """Initialize category keywords"""
        self.category_keywords = {
            FeedbackCategory.TRAINER: [
                "trainer", "instructor", "teacher", "teaching", "explanation",
                "clarity", "delivery", "presentation", "session", "lecture",
                "explain", "understand", "clear", "confusing", "helpful trainer"
            ],
            FeedbackCategory.MENTOR: [
                "mentor", "mentoring", "guidance", "support", "availability",
                "responsive", "help", "assistance", "clarify", "doubt",
                "question", "answer", "mentor support"
            ],
            FeedbackCategory.BATCH_OWNER: [
                "batch owner", "batch", "owner", "process", "procedure",
                "coordination", "schedule", "timing", "organization",
                "management", "batch management"
            ],
            FeedbackCategory.INFRASTRUCTURE: [
                "software", "hardware", "laptop", "computer", "system",
                "internet", "network", "access", "login", "password",
                "application", "tool", "platform", "server", "connection",
                "wi-fi", "wifi", "device", "equipment", "infrastructure"
            ],
            FeedbackCategory.TRAINING_PROGRAM: [
                "curriculum", "syllabus", "course", "content", "material",
                "pacing", "speed", "fast", "slow", "assessment", "exam",
                "test", "evaluation", "assignment", "project", "module",
                "topic", "subject", "program", "training program"
            ],
            FeedbackCategory.ENGAGEMENT: [
                "engagement", "environment", "atmosphere", "culture",
                "communication", "interaction", "participation", "activity",
                "onboarding", "welcome", "team", "colleague", "peer",
                "collaboration", "workshop", "session", "event"
            ]
        }
    
    def map_categories(self, text: str, provided_tags: str = None) -> List[Dict]:
        """
        Map feedback text to categories
        
        Returns:
            List of {
                "category": FeedbackCategory,
                "relevance_score": float,
                "keywords_matched": List[str]
            }
        """
        text_lower = text.lower()
        category_scores = {}
        
        # If tags are provided, use them with high confidence
        if provided_tags:
            tag_list = [tag.strip().lower() for tag in provided_tags.split(",")]
            for tag in tag_list:
                for category, keywords in self.category_keywords.items():
                    if any(keyword in tag for keyword in keywords):
                        if category not in category_scores:
                            category_scores[category] = {
                                "score": 0.0,
                                "keywords": []
                            }
                        category_scores[category]["score"] += 0.3
                        category_scores[category]["keywords"].append(tag)
        
        # Keyword matching in text
        for category, keywords in self.category_keywords.items():
            matched_keywords = []
            score = 0.0
            
            for keyword in keywords:
                # Use word boundaries for exact matches
                pattern = r'\b' + re.escape(keyword) + r'\b'
                matches = re.findall(pattern, text_lower, re.IGNORECASE)
                if matches:
                    matched_keywords.extend(matches)
                    # Score based on keyword importance (longer keywords = more specific)
                    score += len(keyword) * 0.01
            
            if matched_keywords:
                if category not in category_scores:
                    category_scores[category] = {
                        "score": 0.0,
                        "keywords": []
                    }
                category_scores[category]["score"] += min(score, 0.7)  # Cap at 0.7
                category_scores[category]["keywords"].extend(matched_keywords)
        
        # Normalize scores and filter by threshold
        results = []
        for category, data in category_scores.items():
            relevance_score = min(data["score"], 1.0)  # Cap at 1.0
            if relevance_score >= 0.2:  # Threshold for inclusion
                results.append({
                    "category": category,
                    "relevance_score": relevance_score,
                    "keywords_matched": list(set(data["keywords"]))  # Remove duplicates
                })
        
        # Sort by relevance score
        results.sort(key=lambda x: x["relevance_score"], reverse=True)
        
        # If no categories matched, return all with low scores (for comprehensive analysis)
        if not results:
            for category in FeedbackCategory:
                results.append({
                    "category": category,
                    "relevance_score": 0.1,
                    "keywords_matched": []
                })
        
        return results
    
    def get_primary_category(self, text: str, provided_tags: str = None) -> FeedbackCategory:
        """Get the primary (most relevant) category"""
        mappings = self.map_categories(text, provided_tags)
        if mappings:
            return mappings[0]["category"]
        return FeedbackCategory.ENGAGEMENT  # Default


# Global instance
category_mapper = CategoryMapper()




