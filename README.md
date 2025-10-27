# Twitter Sentiment Analysis: Indonesian Protest Economic Impact

This project analyzes Twitter sentiment regarding Indonesian protests that occurred in late August to early September, and examines their effect on the economy.

## Overview

The analysis uses:
- **Twikit** for Twitter data scraping
- **IndoBERT** for Indonesian language sentiment analysis
- Natural Language Processing techniques to understand economic sentiment

## Features

- Twitter data collection focused on Indonesian protest keywords
- Sentiment analysis using IndoBERT (pre-trained Indonesian BERT model)
- Economic sentiment tracking and analysis
- Time-series visualization of sentiment trends
- Economic impact assessment based on sentiment patterns

## Installation

```bash
# Clone the repository
git clone https://github.com/theonegareth/twitter_sentiment_analysis.git
cd twitter_sentiment_analysis

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Configuration

Create a `config.json` file with your search parameters:

```json
{
  "search_keywords": [
    "protes Indonesia ekonomi",
    "demonstrasi Indonesia ekonomi",
    "unjuk rasa Indonesia ekonomi"
  ],
  "date_range": {
    "start_date": "2024-08-20",
    "end_date": "2024-09-10"
  },
  "max_tweets": 1000
}
```

## Usage

### Basic Usage

```bash
# Run the complete analysis pipeline
python main.py

# Run specific components
python src/scraper.py          # Data collection only
python src/sentiment_analyzer.py  # Sentiment analysis only
python src/economic_analyzer.py   # Economic impact analysis only
```

### Example Code

```python
from src.sentiment_analyzer import IndoBERTSentimentAnalyzer
from src.economic_analyzer import EconomicImpactAnalyzer

# Analyze sentiment
analyzer = IndoBERTSentimentAnalyzer()
sentiments = analyzer.analyze_tweets("data/tweets.json")

# Analyze economic impact
economic_analyzer = EconomicImpactAnalyzer()
impact = economic_analyzer.analyze_impact(sentiments)
print(f"Economic Sentiment Score: {impact['sentiment_score']}")
```

## Project Structure

```
twitter_sentiment_analysis/
├── src/
│   ├── __init__.py
│   ├── scraper.py              # Twitter scraping with twikit
│   ├── sentiment_analyzer.py   # IndoBERT sentiment analysis
│   ├── economic_analyzer.py    # Economic impact analysis
│   └── utils.py                # Helper functions
├── main.py                     # Main execution script
├── requirements.txt            # Project dependencies
├── config.json.example         # Example configuration
└── README.md                   # This file
```

## Key Components

### 1. Twitter Scraper (`scraper.py`)
- Uses twikit to collect tweets
- Filters tweets related to Indonesian protests and economy
- Handles rate limiting and error recovery
- Exports data in JSON format

### 2. Sentiment Analyzer (`sentiment_analyzer.py`)
- Implements IndoBERT for Indonesian language understanding
- Classifies sentiment as positive, negative, or neutral
- Provides confidence scores for each classification
- Handles batch processing for efficiency

### 3. Economic Impact Analyzer (`economic_analyzer.py`)
- Analyzes sentiment trends over time
- Identifies key economic concerns from tweets
- Correlates protest activity with economic sentiment
- Generates impact reports and visualizations

## Analysis Approach

1. **Data Collection**: Scrape tweets containing keywords related to Indonesian protests and economy during the specified time period
2. **Preprocessing**: Clean and prepare tweet text for analysis
3. **Sentiment Analysis**: Use IndoBERT to classify sentiment of each tweet
4. **Temporal Analysis**: Track sentiment changes over time
5. **Economic Impact**: Identify economic themes and measure sentiment shifts
6. **Reporting**: Generate insights about protest impact on economic sentiment

## Results Interpretation

The analysis provides:
- **Sentiment Distribution**: Breakdown of positive, negative, and neutral tweets
- **Trend Analysis**: How sentiment changed throughout the protest period
- **Economic Keywords**: Most frequent economic concerns mentioned
- **Impact Score**: Overall assessment of protest impact on economic sentiment

## Dependencies

- `twikit`: Twitter scraping
- `transformers`: For IndoBERT model
- `torch`: Deep learning backend
- `pandas`: Data manipulation
- `numpy`: Numerical operations
- `matplotlib`, `seaborn`: Visualization
- `python-dotenv`: Configuration management

## Notes

- **Twitter API Access**: Twikit may require Twitter/X credentials
- **Model Download**: IndoBERT model will be downloaded on first run (~500MB)
- **Processing Time**: Analysis time depends on tweet volume and hardware
- **Language**: Optimized for Indonesian language tweets

## Ethical Considerations

- This tool is for research and analysis purposes only
- Respects Twitter's terms of service and rate limits
- Does not store personal information
- Aggregates sentiment data to protect individual privacy

## License

See LICENSE file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Contact

For questions or issues, please open an issue on GitHub.