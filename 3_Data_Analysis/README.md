# Twitter Sentiment vs. Market Data Analysis

## Overview
This dataset and notebook analyze the correlation between daily Twitter sentiment related to Indonesian protests in August-September 2025 and financial market indicators: IHSG (Indonesian stock market index) and USD/IDR (US Dollar to Indonesian Rupiah exchange rate).

## Data Sources
- **Sentiment Data**: Scraped from Twitter, classified using GPT-5 into positive, negative, and neutral tweets. Aggregated daily with net sentiment = positive_share - negative_share.
- **IHSG Data**: Daily closing prices from the Indonesian Stock Exchange.
- **USD/IDR Data**: Daily closing exchange rates.

## Time Period
August 1, 2025, to September 29, 2025 (focused on the Indonesian protest event).

## Key Variables
- `date`: YYYY-MM-DD format.
- Sentiment: `total_tweets`, `pos`, `neg`, `neu`, `pos_share`, `neg_share`, `net_sent`.
- Markets: `Close` (price), `ihsg_return` / `usd_return` (daily % change).

## Analysis Summary
- **Correlations**:
  - Net Sentiment vs. IHSG Returns: 0.359 (moderate positive).
  - Net Sentiment vs. USD/IDR Returns: -0.147 (weak negative).
- **Lead-Lag**: Sentiment may predict IHSG returns up to 1-2 days ahead.
- **Limitations**: Small sample (~58 days), potential confounding factors (e.g., global news), sentiment classification biases.

## Files
- `data_analysis.ipynb`: Jupyter notebook with data loading, preprocessing, correlations, and visualizations.
- `data/daily_sentiment_gpt5.csv`: Sentiment data.
- `data/ihsg_daily.csv`: IHSG data.
- `data/usd_idr_daily.csv`: USD/IDR data.

## Dependencies
- Python 3.x
- Libraries: pandas, matplotlib, seaborn, scipy

## Next Steps
- Compute p-values for significance.
- Run Granger causality tests.
- Enhance visualizations for academic journals.
- Expand data for robustness.

## Contact
Prepared by [Your Name]. Pass to collaborator for report writing.