"""
Lightweight sentiment analysis engine
Uses VADER for low memory footprint (works within 512MB RAM limit)
"""
from typing import Dict, List
import logging
import re

logger = logging.getLogger(__name__)


class SentimentAnalyzer:
    """
    Lightweight sentiment analysis using VADER and rule-based approach.
    Designed to work within Render free tier (512MB RAM).
    """
    
    def __init__(self):
        """Initialize the sentiment analyzer"""
        self._vader = None
        self._initialized = False
    
    def _ensure_initialized(self):
        """Lazy load VADER to save memory"""
        if self._initialized:
            return
        
        try:
            import nltk
            from nltk.sentiment.vader import SentimentIntensityAnalyzer
            
            # Download VADER lexicon if not present
            try:
                nltk.data.find('sentiment/vader_lexicon.zip')
            except LookupError:
                nltk.download('vader_lexicon', quiet=True)
            
            self._vader = SentimentIntensityAnalyzer()
            self._initialized = True
            logger.info("VADER sentiment analyzer loaded successfully")
        except Exception as e:
            logger.warning(f"VADER not available, using rule-based fallback: {e}")
            self._initialized = True  # Mark as initialized even without VADER
    
    def analyze(self, text: str) -> Dict:
        """
        Analyze sentiment of a text
        
        Returns:
            {
                "sentiment": "positive" | "neutral" | "negative",
                "confidence": float,
                "scores": {
                    "positive": float,
                    "neutral": float,
                    "negative": float
                }
            }
        """
        if not text or not text.strip():
            return self._neutral_result()
        
        self._ensure_initialized()
        
        try:
            if self._vader:
                return self._analyze_with_vader(text)
            else:
                return self._analyze_rule_based(text)
        except Exception as e:
            logger.error(f"Error analyzing sentiment: {str(e)}")
            return self._neutral_result()
    
    def _analyze_with_vader(self, text: str) -> Dict:
        """Analyze using VADER"""
        scores = self._vader.polarity_scores(text)
        
        # VADER returns: neg, neu, pos, compound
        compound = scores['compound']
        
        # Determine sentiment based on compound score
        if compound >= 0.05:
            sentiment = "positive"
        elif compound <= -0.05:
            sentiment = "negative"
        else:
            sentiment = "neutral"
        
        # Calculate confidence from compound score
        confidence = min(abs(compound) + 0.5, 1.0)
        
        return {
            "sentiment": sentiment,
            "confidence": round(confidence, 3),
            "scores": {
                "negative": round(scores['neg'], 3),
                "neutral": round(scores['neu'], 3),
                "positive": round(scores['pos'], 3)
            }
        }
    
    def _analyze_rule_based(self, text: str) -> Dict:
        """Simple rule-based sentiment analysis as fallback"""
        text_lower = text.lower()
        
        positive_words = [
            'good', 'great', 'excellent', 'amazing', 'wonderful', 'fantastic',
            'helpful', 'best', 'love', 'happy', 'satisfied', 'awesome', 'perfect',
            'thank', 'appreciate', 'enjoyed', 'informative', 'clear', 'useful',
            'well', 'nice', 'interesting', 'engaging', 'supportive', 'effective'
        ]
        
        negative_words = [
            'bad', 'poor', 'terrible', 'awful', 'horrible', 'worst', 'hate',
            'disappointed', 'frustrated', 'confused', 'boring', 'difficult',
            'unclear', 'unhelpful', 'waste', 'slow', 'hard', 'problem', 'issue',
            'not good', 'not clear', 'not helpful', 'too fast', 'too slow'
        ]
        
        pos_count = sum(1 for word in positive_words if word in text_lower)
        neg_count = sum(1 for word in negative_words if word in text_lower)
        
        total = pos_count + neg_count
        if total == 0:
            return self._neutral_result()
        
        pos_ratio = pos_count / total
        neg_ratio = neg_count / total
        neu_ratio = 1 - abs(pos_ratio - neg_ratio)
        
        if pos_count > neg_count:
            sentiment = "positive"
            confidence = 0.5 + (pos_ratio * 0.5)
        elif neg_count > pos_count:
            sentiment = "negative"
            confidence = 0.5 + (neg_ratio * 0.5)
        else:
            sentiment = "neutral"
            confidence = 0.5
        
        return {
            "sentiment": sentiment,
            "confidence": round(confidence, 3),
            "scores": {
                "negative": round(neg_ratio * 0.4 + 0.2, 3),
                "neutral": round(neu_ratio * 0.4 + 0.2, 3),
                "positive": round(pos_ratio * 0.4 + 0.2, 3)
            }
        }
    
    def _neutral_result(self) -> Dict:
        """Return neutral sentiment result"""
        return {
            "sentiment": "neutral",
            "confidence": 0.5,
            "scores": {
                "negative": 0.33,
                "neutral": 0.34,
                "positive": 0.33
            }
        }
    
    def batch_analyze(self, texts: List[str]) -> List[Dict]:
        """Analyze multiple texts in batch"""
        return [self.analyze(text) for text in texts]
    
    def detect_emotional_tone(self, text: str, sentiment: str) -> str:
        """
        Detect emotional tone from text
        Uses keyword matching and context analysis
        """
        text_lower = text.lower()
        
        # Emotional tone keywords
        tone_keywords = {
            "confusion": ["confused", "unclear", "don't understand", "not sure", "unclear"],
            "stress": ["stress", "pressure", "overwhelmed", "difficult", "hard", "challenging"],
            "motivation": ["motivated", "excited", "enthusiastic", "eager", "looking forward"],
            "satisfaction": ["satisfied", "happy", "pleased", "good", "great", "excellent"],
            "frustration": ["frustrated", "annoyed", "disappointed", "upset", "angry"],
            "appreciation": ["thank", "appreciate", "grateful", "helpful", "supportive"]
        }
        
        # Count keyword matches
        tone_scores = {}
        for tone, keywords in tone_keywords.items():
            score = sum(1 for keyword in keywords if keyword in text_lower)
            if score > 0:
                tone_scores[tone] = score
        
        if not tone_scores:
            # Default based on sentiment
            if sentiment == "positive":
                return "satisfaction"
            elif sentiment == "negative":
                return "frustration"
            else:
                return None
        
        # Return tone with highest score
        return max(tone_scores, key=tone_scores.get)


# Global instance (lazy-loaded)
sentiment_analyzer = SentimentAnalyzer()




