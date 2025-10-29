# """
# Main script for Indonesian Protest Economic Impact Analysis

# This script orchestrates the complete analysis pipeline:
# 1. Twitter data scraping (optional - can use existing data)
# 2. Sentiment analysis using IndoBERT
# 3. Economic impact analysis
# 4. Report generation
# """

# import argparse
# import logging
# import sys
# from pathlib import Path

# from src.scraper import TwitterScraper
# from src.sentiment_analyzer import IndoBERTSentimentAnalyzer
# from src.economic_analyzer import EconomicImpactAnalyzer
# from src.utils import ensure_directory

# # Set up logging
# logging.basicConfig(
#     level=logging.INFO,
#     format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
# )
# logger = logging.getLogger(__name__)


# def parse_arguments():
#     """Parse command line arguments."""
#     parser = argparse.ArgumentParser(
#         description='Analyze Indonesian protest economic impact using Twitter sentiment'
#     )
    
#     parser.add_argument(
#         '--skip-scraping',
#         action='store_true',
#         help='Skip Twitter scraping (use existing data)'
#     )
    
#     parser.add_argument(
#         '--tweets-file',
#         type=str,
#         default='data/tweets.json',
#         help='Path to tweets JSON file'
#     )
    
#     parser.add_argument(
#         '--analyzed-file',
#         type=str,
#         default='data/analyzed_tweets.json',
#         help='Path to analyzed tweets JSON file'
#     )
    
#     parser.add_argument(
#         '--output-dir',
#         type=str,
#         default='output',
#         help='Output directory for results'
#     )
    
#     parser.add_argument(
#         '--config',
#         type=str,
#         default='config.json',
#         help='Path to configuration file'
#     )
    
#     parser.add_argument(
#         '--visualize',
#         action='store_true',
#         help='Generate visualization charts'
#     )
    
#     return parser.parse_args()


# def scrape_tweets(config_path: str, output_path: str) -> bool:
#     """
#     Scrape tweets from Twitter.
    
#     Args:
#         config_path: Path to config file
#         output_path: Path to save tweets
        
#     Returns:
#         True if successful, False otherwise
#     """
#     logger.info("Starting Twitter scraping...")
    
#     try:
#         scraper = TwitterScraper(config_path)
        
#         # Note: Authentication requires credentials
#         # This is a placeholder - users need to provide credentials
#         print("\n" + "="*70)
#         print("TWITTER SCRAPING REQUIRES AUTHENTICATION")
#         print("="*70)
#         print("To scrape tweets, you need to:")
#         print("1. Have a Twitter/X account")
#         print("2. Provide credentials via scraper.authenticate()")
#         print("3. Or have a cookies.json file from a previous session")
#         print("\nFor this demo, we'll skip scraping and create sample data.")
#         print("="*70 + "\n")
        
#         return False
        
#     except Exception as e:
#         logger.error(f"Error during scraping: {e}")
#         return False


# def create_sample_data(output_path: str):
#     """
#     Create sample tweet data for demonstration.
    
#     Args:
#         output_path: Path to save sample data
#     """
#     logger.info("Creating sample tweet data for demonstration...")
    
#     sample_tweets = [
#         {
#             "id": "1",
#             "text": "Protes di Indonesia menyebabkan ekonomi tidak stabil. Inflasi naik dan harga sembako meningkat.",
#             "created_at": "2024-08-25 10:00:00",
#             "user": "user1",
#             "retweet_count": 15,
#             "favorite_count": 30,
#             "keyword": "protes Indonesia ekonomi"
#         },
#         {
#             "id": "2",
#             "text": "Demonstrasi besar-besaran membuat pasar saham jatuh drastis. Investor khawatir.",
#             "created_at": "2024-08-26 14:30:00",
#             "user": "user2",
#             "retweet_count": 45,
#             "favorite_count": 67,
#             "keyword": "demonstrasi Indonesia ekonomi"
#         },
#         {
#             "id": "3",
#             "text": "Situasi ekonomi Indonesia masih belum jelas pasca protes. Perlu stabilitas politik.",
#             "created_at": "2024-08-27 09:15:00",
#             "user": "user3",
#             "retweet_count": 23,
#             "favorite_count": 41,
#             "keyword": "protes Indonesia ekonomi"
#         },
#         {
#             "id": "4",
#             "text": "Pemerintah berusaha menjaga stabilitas ekonomi di tengah unjuk rasa. Bank sentral ambil langkah.",
#             "created_at": "2024-08-28 16:45:00",
#             "user": "user4",
#             "retweet_count": 34,
#             "favorite_count": 56,
#             "keyword": "unjuk rasa Indonesia ekonomi"
#         },
#         {
#             "id": "5",
#             "text": "Protes membuat ekonomi tertekan. Rupiah melemah terhadap dolar AS.",
#             "created_at": "2024-08-29 11:20:00",
#             "user": "user5",
#             "retweet_count": 28,
#             "favorite_count": 52,
#             "keyword": "protes Indonesia ekonomi"
#         },
#         {
#             "id": "6",
#             "text": "Dampak demonstrasi terhadap ekonomi mulai terasa. Perdagangan terganggu di beberapa kota.",
#             "created_at": "2024-08-30 13:00:00",
#             "user": "user6",
#             "retweet_count": 19,
#             "favorite_count": 38,
#             "keyword": "demonstrasi Indonesia ekonomi"
#         },
#         {
#             "id": "7",
#             "text": "Investor asing mulai wait and see. Ekonomi Indonesia perlu pemulihan cepat.",
#             "created_at": "2024-08-31 10:30:00",
#             "user": "user7",
#             "retweet_count": 41,
#             "favorite_count": 73,
#             "keyword": "protes Indonesia ekonomi"
#         },
#         {
#             "id": "8",
#             "text": "Sektor pariwisata terdampak akibat protes. Hotel dan restoran sepi pengunjung.",
#             "created_at": "2024-09-01 15:15:00",
#             "user": "user8",
#             "retweet_count": 22,
#             "favorite_count": 45,
#             "keyword": "protes Indonesia ekonomi"
#         },
#         {
#             "id": "9",
#             "text": "Bisnis UMKM kesulitan beroperasi saat demonstrasi berlangsung. Omzet turun signifikan.",
#             "created_at": "2024-09-02 12:00:00",
#             "user": "user9",
#             "retweet_count": 31,
#             "favorite_count": 58,
#             "keyword": "demonstrasi Indonesia ekonomi"
#         },
#         {
#             "id": "10",
#             "text": "Ekonomi diharapkan pulih setelah protes mereda. Pemerintah siap dengan stimulus.",
#             "created_at": "2024-09-03 14:45:00",
#             "user": "user10",
#             "retweet_count": 37,
#             "favorite_count": 69,
#             "keyword": "protes Indonesia ekonomi"
#         }
#     ]
    
#     import json
#     ensure_directory(Path(output_path).parent)
    
#     with open(output_path, 'w', encoding='utf-8') as f:
#         json.dump(sample_tweets, f, ensure_ascii=False, indent=2)
    
#     logger.info(f"Sample data created: {len(sample_tweets)} tweets saved to {output_path}")


# def analyze_sentiment(tweets_file: str, output_file: str) -> bool:
#     """
#     Perform sentiment analysis on tweets.
    
#     Args:
#         tweets_file: Path to tweets JSON file
#         output_file: Path to save analyzed tweets
        
#     Returns:
#         True if successful, False otherwise
#     """
#     logger.info("Starting sentiment analysis...")
    
#     try:
#         # Load tweets
#         import json
#         with open(tweets_file, 'r', encoding='utf-8') as f:
#             tweets = json.load(f)
        
#         logger.info(f"Loaded {len(tweets)} tweets")
        
#         # Initialize analyzer
#         analyzer = IndoBERTSentimentAnalyzer()
        
#         # Analyze tweets
#         analyzed_tweets = analyzer.analyze_tweets(tweets)
        
#         # Show distribution
#         distribution = analyzer.get_sentiment_distribution(analyzed_tweets)
#         logger.info(f"Sentiment distribution: {distribution}")
        
#         # Save results
#         analyzer.save_analyzed_tweets(analyzed_tweets, output_file)
        
#         return True
        
#     except Exception as e:
#         logger.error(f"Error during sentiment analysis: {e}")
#         return False


# def analyze_economic_impact(analyzed_file: str, output_dir: str, visualize: bool = False) -> bool:
#     """
#     Analyze economic impact.
    
#     Args:
#         analyzed_file: Path to analyzed tweets file
#         output_dir: Directory to save results
#         visualize: Whether to generate visualizations
        
#     Returns:
#         True if successful, False otherwise
#     """
#     logger.info("Starting economic impact analysis...")
    
#     try:
#         # Initialize analyzer
#         analyzer = EconomicImpactAnalyzer()
        
#         # Perform analysis
#         results = analyzer.analyze_impact(analyzed_file)
        
#         # Save results
#         results_file = f"{output_dir}/economic_impact_analysis.json"
#         analyzer.save_results(results, results_file)
        
#         # Generate report
#         report = analyzer.generate_report(results)
#         report_file = f"{output_dir}/economic_impact_report.txt"
#         ensure_directory(output_dir)
        
#         with open(report_file, 'w', encoding='utf-8') as f:
#             f.write(report)
        
#         logger.info(f"Report saved to {report_file}")
        
#         # Print report to console
#         print("\n" + report)
        
#         # Generate visualizations if requested
#         if visualize:
#             logger.info("Generating visualizations...")
#             analyzer.visualize_results(results, output_dir)
        
#         return True
        
#     except Exception as e:
#         logger.error(f"Error during economic impact analysis: {e}")
#         return False


# def main():
#     """Main execution function."""
#     print("="*70)
#     print("INDONESIAN PROTEST ECONOMIC IMPACT ANALYSIS")
#     print("Twitter Sentiment Analysis using IndoBERT")
#     print("="*70)
#     print()
    
#     args = parse_arguments()
    
#     # Ensure output directory exists
#     ensure_directory(args.output_dir)
#     ensure_directory(Path(args.tweets_file).parent)
    
#     # Step 1: Scraping (or use existing data)
#     if not args.skip_scraping:
#         success = scrape_tweets(args.config, args.tweets_file)
#         if not success:
#             logger.info("Scraping not available. Using or creating sample data.")
#             if not Path(args.tweets_file).exists():
#                 create_sample_data(args.tweets_file)
#     else:
#         logger.info("Skipping scraping step (using existing data)")
#         if not Path(args.tweets_file).exists():
#             logger.info("No existing data found. Creating sample data.")
#             create_sample_data(args.tweets_file)
    
#     # Step 2: Sentiment Analysis
#     if Path(args.tweets_file).exists():
#         success = analyze_sentiment(args.tweets_file, args.analyzed_file)
#         if not success:
#             logger.error("Sentiment analysis failed")
#             sys.exit(1)
#     else:
#         logger.error(f"Tweets file not found: {args.tweets_file}")
#         sys.exit(1)
    
#     # Step 3: Economic Impact Analysis
#     if Path(args.analyzed_file).exists():
#         success = analyze_economic_impact(args.analyzed_file, args.output_dir, args.visualize)
#         if not success:
#             logger.error("Economic impact analysis failed")
#             sys.exit(1)
#     else:
#         logger.error(f"Analyzed tweets file not found: {args.analyzed_file}")
#         sys.exit(1)
    
#     print("\n" + "="*70)
#     print("ANALYSIS COMPLETE")
#     print("="*70)
#     print(f"\nResults saved to: {args.output_dir}/")
#     print(f"- economic_impact_analysis.json")
#     print(f"- economic_impact_report.txt")
#     if args.visualize:
#         print(f"- sentiment_distribution.png")
#         print(f"- top_concerns.png")
#     print()


# if __name__ == "__main__":
#     main()
