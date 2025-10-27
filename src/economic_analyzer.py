"""
Economic Impact Analyzer

This module analyzes the economic impact of Indonesian protests
based on Twitter sentiment data.
"""

import json
import logging
from typing import List, Dict, Tuple
from datetime import datetime
from pathlib import Path
from collections import Counter

try:
    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt
    import seaborn as sns
except ImportError:
    print("Warning: pandas/numpy/matplotlib not installed. Install with: pip install pandas numpy matplotlib seaborn")
    pd = None

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class EconomicImpactAnalyzer:
    """
    Analyzes economic impact based on sentiment data from tweets.
    """
    
    def __init__(self):
        """Initialize the economic impact analyzer."""
        self.analyzed_tweets = []
        self.economic_keywords = [
            # Indonesian economic terms
            'ekonomi', 'inflasi', 'harga', 'rupiah', 'saham', 'investasi',
            'perdagangan', 'ekspor', 'impor', 'pajak', 'utang', 'kredit',
            'pekerjaan', 'pengangguran', 'gaji', 'upah', 'bisnis', 'perusahaan',
            'bank', 'bunga', 'ekonomi', 'pasar', 'konsumen', 'daya beli',
            'pertumbuhan', 'resesi', 'stagflasi', 'keuangan', 'fiskal', 'moneter',
            # English economic terms (sometimes used)
            'economy', 'inflation', 'stock', 'market', 'business', 'trade'
        ]
    
    def load_data(self, data_path: str = "data/analyzed_tweets.json"):
        """
        Load analyzed tweet data.
        
        Args:
            data_path: Path to analyzed tweets JSON file
        """
        with open(data_path, 'r', encoding='utf-8') as f:
            self.analyzed_tweets = json.load(f)
        logger.info(f"Loaded {len(self.analyzed_tweets)} analyzed tweets")
    
    def filter_economic_tweets(self) -> List[Dict]:
        """
        Filter tweets that mention economic terms.
        
        Returns:
            List of tweets mentioning economic keywords
        """
        economic_tweets = []
        for tweet in self.analyzed_tweets:
            text_lower = tweet['text'].lower()
            if any(keyword in text_lower for keyword in self.economic_keywords):
                economic_tweets.append(tweet)
        
        logger.info(f"Found {len(economic_tweets)} tweets with economic keywords")
        return economic_tweets
    
    def calculate_sentiment_score(self, tweets: List[Dict]) -> float:
        """
        Calculate overall sentiment score.
        
        Args:
            tweets: List of tweets with sentiment
            
        Returns:
            Sentiment score (-1 to 1, negative to positive)
        """
        if not tweets:
            return 0.0
        
        total_score = 0
        for tweet in tweets:
            sentiment = tweet.get('sentiment', {})
            pos = sentiment.get('positive', 0)
            neg = sentiment.get('negative', 0)
            # Score ranges from -1 (all negative) to 1 (all positive)
            total_score += (pos - neg)
        
        avg_score = total_score / len(tweets)
        return round(avg_score, 3)
    
    def analyze_temporal_trends(self, tweets: List[Dict]) -> Dict:
        """
        Analyze sentiment trends over time.
        
        Args:
            tweets: List of tweets with timestamps
            
        Returns:
            Dictionary with temporal analysis
        """
        if pd is None:
            logger.warning("Pandas not available. Skipping temporal analysis.")
            return {}
        
        # Convert to DataFrame
        df_data = []
        for tweet in tweets:
            try:
                date = pd.to_datetime(tweet['created_at'])
                sentiment = tweet.get('sentiment', {})
                df_data.append({
                    'date': date.date(),
                    'sentiment_score': sentiment.get('positive', 0) - sentiment.get('negative', 0),
                    'label': sentiment.get('label', 'neutral')
                })
            except:
                continue
        
        if not df_data:
            return {}
        
        df = pd.DataFrame(df_data)
        
        # Group by date
        daily_sentiment = df.groupby('date').agg({
            'sentiment_score': 'mean',
            'label': lambda x: x.value_counts().index[0] if len(x) > 0 else 'neutral'
        }).reset_index()
        
        # Calculate trend
        if len(daily_sentiment) > 1:
            trend = 'improving' if daily_sentiment['sentiment_score'].iloc[-1] > daily_sentiment['sentiment_score'].iloc[0] else 'declining'
        else:
            trend = 'stable'
        
        return {
            'daily_sentiment': daily_sentiment.to_dict('records'),
            'trend': trend,
            'avg_sentiment': round(df['sentiment_score'].mean(), 3),
            'min_sentiment': round(df['sentiment_score'].min(), 3),
            'max_sentiment': round(df['sentiment_score'].max(), 3)
        }
    
    def extract_economic_concerns(self, tweets: List[Dict], top_n: int = 10) -> List[Tuple[str, int]]:
        """
        Extract most mentioned economic concerns.
        
        Args:
            tweets: List of tweets
            top_n: Number of top keywords to return
            
        Returns:
            List of (keyword, count) tuples
        """
        keyword_counts = Counter()
        
        for tweet in tweets:
            text_lower = tweet['text'].lower()
            for keyword in self.economic_keywords:
                if keyword in text_lower:
                    keyword_counts[keyword] += 1
        
        return keyword_counts.most_common(top_n)
    
    def analyze_impact(self, data_path: str = None) -> Dict:
        """
        Perform complete economic impact analysis.
        
        Args:
            data_path: Optional path to analyzed tweets
            
        Returns:
            Dictionary with complete analysis results
        """
        if data_path:
            self.load_data(data_path)
        
        if not self.analyzed_tweets:
            logger.error("No data loaded. Call load_data() first.")
            return {}
        
        # Get sentiment distribution
        total_tweets = len(self.analyzed_tweets)
        sentiment_dist = {
            'positive': 0,
            'negative': 0,
            'neutral': 0
        }
        
        for tweet in self.analyzed_tweets:
            label = tweet.get('sentiment', {}).get('label', 'neutral')
            sentiment_dist[label] = sentiment_dist.get(label, 0) + 1
        
        # Filter economic tweets
        economic_tweets = self.filter_economic_tweets()
        
        # Calculate scores
        overall_score = self.calculate_sentiment_score(self.analyzed_tweets)
        economic_score = self.calculate_sentiment_score(economic_tweets)
        
        # Temporal analysis
        temporal_analysis = self.analyze_temporal_trends(economic_tweets)
        
        # Top concerns
        top_concerns = self.extract_economic_concerns(economic_tweets)
        
        # Compile results
        results = {
            'summary': {
                'total_tweets': total_tweets,
                'economic_tweets': len(economic_tweets),
                'economic_tweet_percentage': round(len(economic_tweets) / total_tweets * 100, 1) if total_tweets > 0 else 0,
            },
            'sentiment_distribution': sentiment_dist,
            'sentiment_scores': {
                'overall': overall_score,
                'economic_specific': economic_score,
                'interpretation': self._interpret_score(economic_score)
            },
            'temporal_analysis': temporal_analysis,
            'top_economic_concerns': [
                {'keyword': k, 'mentions': c} for k, c in top_concerns
            ],
            'impact_assessment': self._assess_impact(economic_score, sentiment_dist, len(economic_tweets))
        }
        
        return results
    
    def _interpret_score(self, score: float) -> str:
        """Interpret sentiment score."""
        if score >= 0.3:
            return "Predominantly Positive"
        elif score >= 0.1:
            return "Slightly Positive"
        elif score >= -0.1:
            return "Neutral/Mixed"
        elif score >= -0.3:
            return "Slightly Negative"
        else:
            return "Predominantly Negative"
    
    def _assess_impact(self, score: float, distribution: Dict, economic_tweet_count: int) -> Dict:
        """
        Assess the overall economic impact of protests.
        
        Args:
            score: Sentiment score
            distribution: Sentiment distribution
            economic_tweet_count: Number of economic tweets
            
        Returns:
            Impact assessment dictionary
        """
        # Calculate impact level
        negative_ratio = distribution.get('negative', 0) / sum(distribution.values()) if sum(distribution.values()) > 0 else 0
        
        if score < -0.2 and negative_ratio > 0.5:
            impact_level = "High Negative Impact"
            description = "The protests appear to have significantly negative impact on economic sentiment. High proportion of negative discussions about economy."
        elif score < -0.1 and negative_ratio > 0.4:
            impact_level = "Moderate Negative Impact"
            description = "The protests show moderate negative impact on economic sentiment. Considerable economic concerns expressed."
        elif score < 0.1:
            impact_level = "Slight Negative Impact"
            description = "The protests show slight negative impact on economic sentiment. Some economic concerns present but not overwhelming."
        elif score < 0.2:
            impact_level = "Minimal Impact"
            description = "The protests show minimal impact on economic sentiment. Economic discussions are relatively neutral."
        else:
            impact_level = "Positive or Neutral Impact"
            description = "The protests do not appear to have negative impact on economic sentiment. Discussions are positive or neutral."
        
        return {
            'impact_level': impact_level,
            'description': description,
            'confidence': 'medium' if economic_tweet_count > 50 else 'low',
            'sample_size': economic_tweet_count
        }
    
    def save_results(self, results: Dict, output_path: str = "output/economic_impact_analysis.json"):
        """
        Save analysis results to JSON file.
        
        Args:
            results: Analysis results dictionary
            output_path: Path to save results
        """
        output_dir = Path(output_path).parent
        output_dir.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        
        logger.info(f"Results saved to {output_path}")
    
    def generate_report(self, results: Dict) -> str:
        """
        Generate a human-readable report.
        
        Args:
            results: Analysis results
            
        Returns:
            Formatted report string
        """
        report = []
        report.append("=" * 70)
        report.append("ECONOMIC IMPACT ANALYSIS: INDONESIAN PROTESTS")
        report.append("Late August to Early September 2024")
        report.append("=" * 70)
        report.append("")
        
        # Summary
        summary = results.get('summary', {})
        report.append("SUMMARY")
        report.append("-" * 70)
        report.append(f"Total Tweets Analyzed: {summary.get('total_tweets', 0)}")
        report.append(f"Economic-Related Tweets: {summary.get('economic_tweets', 0)} ({summary.get('economic_tweet_percentage', 0)}%)")
        report.append("")
        
        # Sentiment Distribution
        dist = results.get('sentiment_distribution', {})
        report.append("SENTIMENT DISTRIBUTION")
        report.append("-" * 70)
        report.append(f"Positive: {dist.get('positive', 0)} tweets")
        report.append(f"Negative: {dist.get('negative', 0)} tweets")
        report.append(f"Neutral: {dist.get('neutral', 0)} tweets")
        report.append("")
        
        # Sentiment Scores
        scores = results.get('sentiment_scores', {})
        report.append("SENTIMENT SCORES")
        report.append("-" * 70)
        report.append(f"Overall Sentiment: {scores.get('overall', 0)} ({scores.get('interpretation', 'N/A')})")
        report.append(f"Economic Sentiment: {scores.get('economic_specific', 0)}")
        report.append("")
        
        # Top Concerns
        concerns = results.get('top_economic_concerns', [])
        if concerns:
            report.append("TOP ECONOMIC CONCERNS")
            report.append("-" * 70)
            for i, concern in enumerate(concerns[:10], 1):
                report.append(f"{i}. {concern['keyword']}: {concern['mentions']} mentions")
            report.append("")
        
        # Impact Assessment
        impact = results.get('impact_assessment', {})
        report.append("IMPACT ASSESSMENT")
        report.append("-" * 70)
        report.append(f"Impact Level: {impact.get('impact_level', 'Unknown')}")
        report.append(f"Confidence: {impact.get('confidence', 'unknown').upper()}")
        report.append(f"Sample Size: {impact.get('sample_size', 0)} economic tweets")
        report.append("")
        report.append("Description:")
        report.append(impact.get('description', 'No description available'))
        report.append("")
        
        report.append("=" * 70)
        
        return "\n".join(report)
    
    def visualize_results(self, results: Dict, output_dir: str = "output"):
        """
        Create visualizations of the analysis results.
        
        Args:
            results: Analysis results
            output_dir: Directory to save visualizations
        """
        if plt is None:
            logger.warning("Matplotlib not available. Skipping visualizations.")
            return
        
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        # Set style
        sns.set_style("whitegrid")
        
        # 1. Sentiment Distribution Pie Chart
        dist = results.get('sentiment_distribution', {})
        if dist:
            fig, ax = plt.subplots(figsize=(10, 6))
            colors = ['#2ecc71', '#e74c3c', '#95a5a6']
            ax.pie(dist.values(), labels=dist.keys(), autopct='%1.1f%%', 
                   colors=colors, startangle=90)
            ax.set_title('Sentiment Distribution: Indonesian Protest Economic Impact', 
                        fontsize=14, fontweight='bold')
            plt.savefig(output_path / 'sentiment_distribution.png', dpi=300, bbox_inches='tight')
            plt.close()
            logger.info("Saved sentiment distribution chart")
        
        # 2. Top Economic Concerns Bar Chart
        concerns = results.get('top_economic_concerns', [])
        if concerns:
            fig, ax = plt.subplots(figsize=(12, 8))
            keywords = [c['keyword'] for c in concerns[:10]]
            mentions = [c['mentions'] for c in concerns[:10]]
            
            bars = ax.barh(keywords, mentions, color='#3498db')
            ax.set_xlabel('Number of Mentions', fontsize=12)
            ax.set_title('Top Economic Concerns During Protests', 
                        fontsize=14, fontweight='bold')
            ax.invert_yaxis()
            
            # Add value labels
            for i, bar in enumerate(bars):
                width = bar.get_width()
                ax.text(width, bar.get_y() + bar.get_height()/2, 
                       f' {int(width)}', ha='left', va='center')
            
            plt.tight_layout()
            plt.savefig(output_path / 'top_concerns.png', dpi=300, bbox_inches='tight')
            plt.close()
            logger.info("Saved top concerns chart")


def main():
    """Main function for testing the economic analyzer."""
    print("Economic Impact Analyzer")
    print("=" * 50)
    print("\nThis module analyzes the economic impact of Indonesian protests")
    print("based on Twitter sentiment data.")
    print("\nTo use:")
    print("1. Load analyzed tweets with load_data()")
    print("2. Run analyze_impact() to get results")
    print("3. Use generate_report() to create a readable report")
    print("4. Use visualize_results() to create charts")


if __name__ == "__main__":
    main()
