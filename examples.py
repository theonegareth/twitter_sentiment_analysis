#!/usr/bin/env python3
"""
Example: Quick Start Guide for Indonesian Protest Economic Impact Analysis

This script demonstrates how to use the analysis tools with your own data.
"""

from src.scraper import TwitterScraper
from src.sentiment_analyzer import IndoBERTSentimentAnalyzer
from src.economic_analyzer import EconomicImpactAnalyzer

def example_with_existing_tweets():
    """Example: Analyze existing tweet data."""
    print("\n" + "="*70)
    print("EXAMPLE 1: Analyze Existing Tweet Data")
    print("="*70 + "\n")
    
    # Load and analyze tweets
    analyzer = IndoBERTSentimentAnalyzer()
    
    # Load tweets from file
    import json
    with open('data/tweets.json', 'r', encoding='utf-8') as f:
        tweets = json.load(f)
    
    print(f"Loaded {len(tweets)} tweets")
    
    # Analyze sentiment
    analyzed_tweets = analyzer.analyze_tweets(tweets)
    
    # Show some results
    print(f"\nSample Analysis Results:")
    for i, tweet in enumerate(analyzed_tweets[:3], 1):
        print(f"\n{i}. {tweet['text'][:80]}...")
        print(f"   Sentiment: {tweet['sentiment']['label']} "
              f"(confidence: {tweet['sentiment']['confidence']})")
    
    # Save results
    analyzer.save_analyzed_tweets(analyzed_tweets)
    print(f"\n✓ Analyzed tweets saved to data/analyzed_tweets.json")


def example_economic_analysis():
    """Example: Perform economic impact analysis."""
    print("\n" + "="*70)
    print("EXAMPLE 2: Economic Impact Analysis")
    print("="*70 + "\n")
    
    # Initialize analyzer
    analyzer = EconomicImpactAnalyzer()
    
    # Perform analysis
    results = analyzer.analyze_impact('data/analyzed_tweets.json')
    
    # Display key results
    print("Key Findings:")
    print("-" * 70)
    print(f"Total Tweets: {results['summary']['total_tweets']}")
    print(f"Economic Tweets: {results['summary']['economic_tweets']} "
          f"({results['summary']['economic_tweet_percentage']}%)")
    print(f"\nEconomic Sentiment Score: {results['sentiment_scores']['economic_specific']}")
    print(f"Interpretation: {results['sentiment_scores']['interpretation']}")
    print(f"\nImpact Level: {results['impact_assessment']['impact_level']}")
    
    # Top concerns
    print(f"\nTop 5 Economic Concerns:")
    for i, concern in enumerate(results['top_economic_concerns'][:5], 1):
        print(f"  {i}. {concern['keyword']}: {concern['mentions']} mentions")
    
    # Generate report
    report = analyzer.generate_report(results)
    
    # Save report
    with open('output/quick_start_report.txt', 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"\n✓ Full report saved to output/quick_start_report.txt")


def example_custom_tweets():
    """Example: Analyze custom tweet list."""
    print("\n" + "="*70)
    print("EXAMPLE 3: Analyze Custom Tweets")
    print("="*70 + "\n")
    
    # Create custom tweets
    custom_tweets = [
        {
            "id": "custom1",
            "text": "Ekonomi Indonesia stabil meski ada protes",
            "created_at": "2024-09-01 10:00:00",
            "user": "testuser1",
            "retweet_count": 5,
            "favorite_count": 10,
            "keyword": "custom"
        },
        {
            "id": "custom2",
            "text": "Inflasi naik karena demonstrasi mengganggu supply chain",
            "created_at": "2024-09-02 11:00:00",
            "user": "testuser2",
            "retweet_count": 8,
            "favorite_count": 15,
            "keyword": "custom"
        }
    ]
    
    # Analyze sentiment
    analyzer = IndoBERTSentimentAnalyzer()
    analyzed = analyzer.analyze_tweets(custom_tweets)
    
    print("Analysis Results:")
    for tweet in analyzed:
        print(f"\nTweet: {tweet['text']}")
        print(f"Sentiment: {tweet['sentiment']['label']} "
              f"(Pos: {tweet['sentiment']['positive']}, "
              f"Neg: {tweet['sentiment']['negative']}, "
              f"Neu: {tweet['sentiment']['neutral']})")


def main():
    """Run all examples."""
    print("\n" + "="*70)
    print("TWITTER SENTIMENT ANALYSIS - QUICK START EXAMPLES")
    print("Indonesian Protest Economic Impact")
    print("="*70)
    
    try:
        # Example 1: Existing tweets
        example_with_existing_tweets()
        
        # Example 2: Economic analysis
        example_economic_analysis()
        
        # Example 3: Custom tweets
        example_custom_tweets()
        
        print("\n" + "="*70)
        print("ALL EXAMPLES COMPLETED SUCCESSFULLY")
        print("="*70 + "\n")
        
    except FileNotFoundError as e:
        print(f"\n⚠ Error: {e}")
        print("\nPlease run 'python main.py --skip-scraping' first to generate sample data.")
    except Exception as e:
        print(f"\n⚠ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
