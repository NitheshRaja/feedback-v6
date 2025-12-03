"""
Sentiment analysis engine using transformer models
"""
from typing import Dict, List, Tuple
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)


class SentimentAnalyzer:
    """Sentiment analysis using pre-trained transformer models"""
    
    def __init__(self):
        """Initialize the sentiment analyzer"""
        self.model_name = settings.SENTIMENT_MODEL
        self.device = settings.DEVICE
        self.tokenizer = None
        self.model = None
        self._load_model()
    
    def _load_model(self):
        """Load the pre-trained model and tokenizer"""
        try:
            logger.info(f"Loading sentiment model: {self.model_name}")
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
            self.model = AutoModelForSequenceClassification.from_pretrained(
                self.model_name
            )
            self.model.to(self.device)
            self.model.eval()
            logger.info("Sentiment model loaded successfully")
        except Exception as e:
            logger.error(f"Error loading sentiment model: {str(e)}")
            raise
    
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
        try:
            # Tokenize input
            inputs = self.tokenizer(
                text,
                return_tensors="pt",
                truncation=True,
                max_length=512,
                padding=True
            ).to(self.device)
            
            # Get predictions
            with torch.no_grad():
                outputs = self.model(**inputs)
                logits = outputs.logits
                probabilities = torch.softmax(logits, dim=-1)
            
            # Map to sentiment labels
            # Model outputs: 0=negative, 1=neutral, 2=positive
            probs = probabilities[0].cpu().numpy()
            
            sentiment_map = {0: "negative", 1: "neutral", 2: "positive"}
            predicted_class = int(torch.argmax(probabilities, dim=-1)[0])
            sentiment = sentiment_map.get(predicted_class, "neutral")
            confidence = float(probs[predicted_class])
            
            scores = {
                "negative": float(probs[0]),
                "neutral": float(probs[1]),
                "positive": float(probs[2])
            }
            
            return {
                "sentiment": sentiment,
                "confidence": confidence,
                "scores": scores
            }
        except Exception as e:
            logger.error(f"Error analyzing sentiment: {str(e)}")
            # Return neutral as fallback
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


# Global instance
sentiment_analyzer = SentimentAnalyzer()




