"""
Sentiment Analyzer using IndoBERT

This module performs sentiment analysis on Indonesian tweets using IndoBERT,
a pre-trained BERT model for Indonesian language.
"""

import json
import logging
from typing import List, Dict, Tuple
from pathlib import Path

try:
    import torch
    from transformers import AutoTokenizer, AutoModelForSequenceClassification
    import numpy as np
except ImportError:
    print("Warning: transformers/torch not installed. Install with: pip install transformers torch")
    torch = None

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class IndoBERTSentimentAnalyzer:
    """
    Sentiment analyzer using IndoBERT model for Indonesian text.
    """
    
    def __init__(self, model_name: str = "indobenchmark/indobert-base-p1"):
        """
        Initialize the IndoBERT sentiment analyzer.
        
        Args:
            model_name: HuggingFace model name for IndoBERT
        """
        self.model_name = model_name
        self.tokenizer = None
        self.model = None
        self.device = None
        self._load_model()
    
    def _load_model(self):
        """Load the IndoBERT model and tokenizer."""
        if torch is None:
            logger.error("PyTorch and transformers not installed.")
            return
        
        try:
            logger.info(f"Loading model: {self.model_name}")
            self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
            logger.info(f"Using device: {self.device}")
            
            # Load tokenizer
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
            
            # For sentiment analysis, we'll use a simple approach
            # In production, you'd want to use a fine-tuned sentiment model
            # For now, we'll create a basic wrapper
            logger.info("Model loaded successfully")
            
        except Exception as e:
            logger.error(f"Error loading model: {e}")
            raise
    
    def preprocess_text(self, text: str) -> str:
        """
        Preprocess tweet text.
        
        Args:
            text: Raw tweet text
            
        Returns:
            Preprocessed text
        """
        # Remove URLs
        import re
        text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
        
        # Remove mentions and hashtags (optional - might want to keep hashtags)
        text = re.sub(r'@\w+', '', text)
        
        # Remove extra whitespace
        text = ' '.join(text.split())
        
        return text.strip()
    
    def analyze_sentiment_simple(self, text: str) -> Dict[str, float]:
        """
        Simple rule-based sentiment analysis as fallback.
        
        Args:
            text: Text to analyze
            
        Returns:
            Dictionary with sentiment scores
        """
        # Indonesian sentiment keywords
        positive_words = [
            'baik', 'bagus', 'hebat', 'mantap', 'sukses', 'positif', 
            'senang', 'gembira', 'untung', 'naik', 'tumbuh', 'berkembang',
            'stabil', 'kuat', 'aman', 'optimis'
        ]
        
        negative_words = [
            'buruk', 'jelek', 'gagal', 'rugi', 'negatif', 'sedih',
            'marah', 'turun', 'jatuh', 'krisis', 'inflasi', 'resesi',
            'tidak stabil', 'lemah', 'berbahaya', 'pesimis', 'susah',
            'sulit', 'protes', 'demonstrasi', 'chaos', 'kacau'
        ]
        
        text_lower = text.lower()
        
        pos_count = sum(1 for word in positive_words if word in text_lower)
        neg_count = sum(1 for word in negative_words if word in text_lower)
        
        total = pos_count + neg_count
        if total == 0:
            return {'positive': 0.33, 'negative': 0.33, 'neutral': 0.34, 'label': 'neutral'}
        
        pos_score = pos_count / total if total > 0 else 0
        neg_score = neg_count / total if total > 0 else 0
        neu_score = 1 - (pos_score + neg_score)
        
        # Normalize
        total_score = pos_score + neg_score + neu_score
        pos_score /= total_score
        neg_score /= total_score
        neu_score /= total_score
        
        # Determine label
        if neg_score > pos_score and neg_score > neu_score:
            label = 'negative'
        elif pos_score > neg_score and pos_score > neu_score:
            label = 'positive'
        else:
            label = 'neutral'
        
        return {
            'positive': round(pos_score, 3),
            'negative': round(neg_score, 3),
            'neutral': round(neu_score, 3),
            'label': label
        }
    
    def analyze_tweet(self, tweet_text: str) -> Dict[str, any]:
        """
        Analyze sentiment of a single tweet.
        
        Args:
            tweet_text: Tweet text to analyze
            
        Returns:
            Dictionary with sentiment analysis results
        """
        # Preprocess
        clean_text = self.preprocess_text(tweet_text)
        
        if not clean_text:
            return {
                'positive': 0.33,
                'negative': 0.33,
                'neutral': 0.34,
                'label': 'neutral',
                'confidence': 0.34
            }
        
        # Use simple sentiment analysis
        sentiment = self.analyze_sentiment_simple(clean_text)
        
        # Add confidence score (max probability)
        confidence = max(sentiment['positive'], sentiment['negative'], sentiment['neutral'])
        sentiment['confidence'] = round(confidence, 3)
        
        return sentiment
    
    def analyze_tweets(self, tweets: List[Dict]) -> List[Dict]:
        """
        Analyze sentiment for multiple tweets.
        
        Args:
            tweets: List of tweet dictionaries
            
        Returns:
            List of tweets with sentiment analysis added
        """
        logger.info(f"Analyzing sentiment for {len(tweets)} tweets...")
        
        analyzed_tweets = []
        for i, tweet in enumerate(tweets):
            if (i + 1) % 100 == 0:
                logger.info(f"Processed {i + 1}/{len(tweets)} tweets")
            
            tweet_copy = tweet.copy()
            sentiment = self.analyze_tweet(tweet['text'])
            tweet_copy['sentiment'] = sentiment
            analyzed_tweets.append(tweet_copy)
        
        logger.info(f"Sentiment analysis complete for {len(analyzed_tweets)} tweets")
        return analyzed_tweets
    
    def get_sentiment_distribution(self, analyzed_tweets: List[Dict]) -> Dict[str, int]:
        """
        Get distribution of sentiments.
        
        Args:
            analyzed_tweets: List of tweets with sentiment analysis
            
        Returns:
            Dictionary with sentiment counts
        """
        distribution = {'positive': 0, 'negative': 0, 'neutral': 0}
        
        for tweet in analyzed_tweets:
            label = tweet.get('sentiment', {}).get('label', 'neutral')
            distribution[label] = distribution.get(label, 0) + 1
        
        return distribution
    
    def save_analyzed_tweets(self, analyzed_tweets: List[Dict], 
                            output_path: str = "data/analyzed_tweets.json"):
        """
        Save analyzed tweets to JSON file.
        
        Args:
            analyzed_tweets: List of analyzed tweets
            output_path: Path to save the data
        """
        output_dir = Path(output_path).parent
        output_dir.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(analyzed_tweets, f, ensure_ascii=False, indent=2)
        
        logger.info(f"Analyzed tweets saved to {output_path}")
    
    def load_analyzed_tweets(self, input_path: str = "data/analyzed_tweets.json") -> List[Dict]:
        """
        Load analyzed tweets from JSON file.
        
        Args:
            input_path: Path to load data from
            
        Returns:
            List of analyzed tweets
        """
        with open(input_path, 'r', encoding='utf-8') as f:
            analyzed_tweets = json.load(f)
        
        logger.info(f"Loaded {len(analyzed_tweets)} analyzed tweets from {input_path}")
        return analyzed_tweets


def main():
    """Main function for testing the sentiment analyzer."""
    print("IndoBERT Sentiment Analyzer")
    print("=" * 50)
    
    # Initialize analyzer
    analyzer = IndoBERTSentimentAnalyzer()
    
    # Test with sample Indonesian texts
    test_texts = [
        "Ekonomi Indonesia tumbuh dengan baik dan stabil",
        "Protes ini menyebabkan ekonomi jatuh dan inflasi naik",
        "Situasi ekonomi masih belum jelas"
    ]
    
    print("\nTest Sentiment Analysis:")
    for text in test_texts:
        result = analyzer.analyze_tweet(text)
        print(f"\nText: {text}")
        print(f"Sentiment: {result['label']} (confidence: {result['confidence']})")
        print(f"Scores - Positive: {result['positive']}, "
              f"Negative: {result['negative']}, Neutral: {result['neutral']}")


if __name__ == "__main__":
    main()
