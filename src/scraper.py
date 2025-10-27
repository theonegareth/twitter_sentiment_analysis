"""
Twitter Scraper using Twikit

This module handles Twitter data collection using the twikit library.
It scrapes tweets related to Indonesian protests and economic impact.
"""

import json
import logging
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from pathlib import Path

try:
    from twikit import Client
    from twikit.errors import TooManyRequests, TwitterException
except ImportError:
    print("Warning: twikit not installed. Install with: pip install twikit")
    Client = None

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TwitterScraper:
    """
    A class to scrape Twitter data related to Indonesian protests and economy.
    """
    
    def __init__(self, config_path: str = "config.json"):
        """
        Initialize the Twitter scraper.
        
        Args:
            config_path: Path to configuration file
        """
        self.config = self._load_config(config_path)
        self.client = None
        self.tweets_data = []
        
    def _load_config(self, config_path: str) -> Dict:
        """Load configuration from JSON file."""
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            logger.warning(f"Config file {config_path} not found. Using defaults.")
            return self._get_default_config()
    
    def _get_default_config(self) -> Dict:
        """Return default configuration."""
        return {
            "search_keywords": [
                "protes Indonesia ekonomi",
                "demonstrasi Indonesia ekonomi",
                "unjuk rasa Indonesia ekonomi",
                "protest Indonesia economy"
            ],
            "date_range": {
                "start_date": "2024-08-20",
                "end_date": "2024-09-10"
            },
            "max_tweets": 1000,
            "language": "id"
        }
    
    def authenticate(self, username: Optional[str] = None, 
                    email: Optional[str] = None, 
                    password: Optional[str] = None):
        """
        Authenticate with Twitter/X.
        
        Args:
            username: Twitter username
            email: Twitter email
            password: Twitter password
        """
        if Client is None:
            raise ImportError("twikit is not installed")
            
        self.client = Client('en-US')
        
        # Try to load cookies if they exist
        cookies_path = Path("cookies.json")
        if cookies_path.exists():
            logger.info("Loading saved cookies...")
            self.client.load_cookies(str(cookies_path))
        elif username and password:
            logger.info("Logging in to Twitter...")
            self.client.login(
                auth_info_1=username,
                auth_info_2=email if email else username,
                password=password
            )
            # Save cookies for future use
            self.client.save_cookies("cookies.json")
            logger.info("Cookies saved for future use.")
        else:
            raise ValueError("Either provide credentials or have cookies.json file")
    
    def scrape_tweets(self, keyword: str, max_tweets: int = 100) -> List[Dict]:
        """
        Scrape tweets for a specific keyword.
        
        Args:
            keyword: Search keyword
            max_tweets: Maximum number of tweets to scrape
            
        Returns:
            List of tweet dictionaries
        """
        if self.client is None:
            logger.error("Client not authenticated. Call authenticate() first.")
            return []
        
        tweets = []
        logger.info(f"Searching for: {keyword}")
        
        try:
            # Build search query with date range
            query = f"{keyword} lang:{self.config.get('language', 'id')}"
            
            # Search tweets
            search_results = self.client.search_tweet(query, 'Latest')
            
            count = 0
            while count < max_tweets:
                if not search_results:
                    break
                    
                for tweet in search_results:
                    if count >= max_tweets:
                        break
                    
                    tweet_data = {
                        'id': tweet.id,
                        'text': tweet.text,
                        'created_at': str(tweet.created_at),
                        'user': tweet.user.screen_name if tweet.user else 'unknown',
                        'retweet_count': tweet.retweet_count,
                        'favorite_count': tweet.favorite_count,
                        'keyword': keyword
                    }
                    tweets.append(tweet_data)
                    count += 1
                
                # Try to get more tweets
                if count < max_tweets:
                    try:
                        search_results = search_results.next()
                    except:
                        break
                        
        except TooManyRequests as e:
            logger.warning(f"Rate limit reached. Scraped {len(tweets)} tweets.")
        except TwitterException as e:
            logger.error(f"Twitter error: {e}")
        except Exception as e:
            logger.error(f"Error scraping tweets: {e}")
        
        logger.info(f"Scraped {len(tweets)} tweets for keyword: {keyword}")
        return tweets
    
    def scrape_all_keywords(self) -> List[Dict]:
        """
        Scrape tweets for all configured keywords.
        
        Returns:
            List of all tweet dictionaries
        """
        all_tweets = []
        keywords = self.config.get("search_keywords", [])
        max_tweets = self.config.get("max_tweets", 1000)
        tweets_per_keyword = max_tweets // len(keywords) if keywords else 100
        
        for keyword in keywords:
            tweets = self.scrape_tweets(keyword, tweets_per_keyword)
            all_tweets.extend(tweets)
        
        self.tweets_data = all_tweets
        logger.info(f"Total tweets scraped: {len(all_tweets)}")
        return all_tweets
    
    def save_tweets(self, output_path: str = "data/tweets.json"):
        """
        Save scraped tweets to JSON file.
        
        Args:
            output_path: Path to save the tweets
        """
        # Create directory if it doesn't exist
        output_dir = Path(output_path).parent
        output_dir.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(self.tweets_data, f, ensure_ascii=False, indent=2)
        
        logger.info(f"Tweets saved to {output_path}")
    
    def load_tweets(self, input_path: str = "data/tweets.json") -> List[Dict]:
        """
        Load tweets from JSON file.
        
        Args:
            input_path: Path to load tweets from
            
        Returns:
            List of tweet dictionaries
        """
        with open(input_path, 'r', encoding='utf-8') as f:
            self.tweets_data = json.load(f)
        
        logger.info(f"Loaded {len(self.tweets_data)} tweets from {input_path}")
        return self.tweets_data


def main():
    """Main function for testing the scraper."""
    print("Twitter Scraper Module")
    print("=" * 50)
    
    # Initialize scraper
    scraper = TwitterScraper()
    
    print("\nConfiguration:")
    print(f"Keywords: {scraper.config['search_keywords']}")
    print(f"Max tweets: {scraper.config['max_tweets']}")
    print(f"Date range: {scraper.config['date_range']}")
    
    print("\nNote: To use the scraper, you need to:")
    print("1. Call scraper.authenticate(username, email, password)")
    print("2. Call scraper.scrape_all_keywords()")
    print("3. Call scraper.save_tweets()")
    
    print("\nThis module requires Twitter/X credentials to function.")


if __name__ == "__main__":
    main()
