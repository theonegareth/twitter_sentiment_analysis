# Twitter Sentiment Analysis Pipeline

This repository contains a complete, reproducible pipeline to:

- Scrape and preprocess ~80,000 tweets.
- Clean and deduplicate tweets into a high-quality dataset.
- Run LLM-based sentiment labeling using OpenRouter.
- (Optionally) Aggregate daily sentiment and correlate it with financial indicators (e.g., IHSG, USD/IDR).

The core work is organized under:

- `5th Semester/Data Mining/twitter_sentiment_analysis/`
- `5th Semester/Data Mining/twitter_sentiment_analysis/2_Data_Cleaning/`

This README documents the structure, cleaning logic, and how to run the sentiment labeling pipeline on your final dataset.

---

## 1. Project Structure

Key files and directories (paths are relative to `twitter_sentiment_analysis/`):

- [`2_Data_Cleaning/`](2_Data_Cleaning:1)
  - [`tweet_cleaning.py`](2_Data_Cleaning/tweet_cleaning.py:1)
    - Reusable utilities for tweet text cleaning.
  - [`batch_clean_tweets.py`](2_Data_Cleaning/batch_clean_tweets.py:1)
    - Batch clean multiple raw tweet CSVs and merge them.
  - [`deduplicate_clean_tweets.py`](2_Data_Cleaning/deduplicate_clean_tweets.py:1)
    - Deduplicate merged cleaned tweets.
  - [`gpt5_sentiment_pipeline.py`](2_Data_Cleaning/gpt5_sentiment_pipeline.py:1)
    - LLM (GPT/OpenRouter) based sentiment labeling pipeline.
  - `data/`
    - `tweets_all_clean_dedup_clean.csv`
      - Final cleaned + deduplicated tweets dataset (source for sentiment labeling).
    - (Will be generated)
      - `tweets_gpt5_labeled.csv`
      - `daily_sentiment_gpt5.csv`
- [`Sentiment_analysis/sentiment_analysis.ipynb`](Sentiment_analysis/sentiment_analysis.ipynb:1)
  - Exploratory notebook for sentiment analysis experiments.
- `.env`
  - Located at `twitter_sentiment_analysis/.env`
  - Stores credentials (e.g., `OPENROUTER_API_KEY`) for the LLM API.

Note: Some legacy/experimental files may exist; the files above define the recommended, stable pipeline.

---

## 2. Data Cleaning Logic

All tweet cleaning is centralized in [`tweet_cleaning.py`](2_Data_Cleaning/tweet_cleaning.py:1) to ensure consistency.

Key function:
- `clean_tweet_text()`:
  - Normalizes whitespace and unicode.
  - Optionally lowercases text.
  - Removes:
    - URLs (e.g., `https://...`, `www...`).
    - RT markers (`RT`, `RT @user:`).
  - Handles mentions:
    - Can remove or replace them (configurable).
  - Handles hashtags:
    - Strips `#` but keeps the hashtag word (`#bullish` → `bullish`).
  - Optionally removes emojis (recommended: keep them, as they carry sentiment).
  - Collapses extra spaces and drops empty results.

The typical cleaned dataset contains:
- `id` — original tweet ID.
- `created_at` — timestamp.
- `text` — original tweet.
- `clean_text` — processed text from `clean_tweet_text()`.

---

## 3. From Raw Tweets to Final Clean Dataset

If you are starting from raw `tweets_*.csv` files, use this pipeline.

1) Batch cleaning

[`batch_clean_tweets.py`](2_Data_Cleaning/batch_clean_tweets.py:1) will:
- Load each matching raw CSV.
- Apply `clean_tweet_text()` to create `clean_text`.
- Write per-file `*_clean.csv`.
- Merge all `*_clean.csv` into a single file (e.g., `tweets_all_clean.csv`).

2) Deduplication

[`deduplicate_clean_tweets.py`](2_Data_Cleaning/deduplicate_clean_tweets.py:1) performs:
- Drop duplicate rows by `id` (if present).
- Drop duplicate rows by `clean_text`.
- Save the final canonical dataset.

In this project, the chosen canonical dataset is:

- `2_Data_Cleaning/data/tweets_all_clean_dedup_clean.csv`

This file is:
- Cleaned with consistent rules.
- Deduplicated by both `id` and `clean_text`.
- Used as the single source of truth for sentiment labeling.

---

## 4. LLM-Based Sentiment Labeling

Sentiment labeling is implemented in:
- [`gpt5_sentiment_pipeline.py`](2_Data_Cleaning/gpt5_sentiment_pipeline.py:1)

Features:
- Uses OpenRouter-compatible API (via `OPENROUTER_API_KEY`) or `OPENAI_API_KEY`.
- Targets:
  - Input: `2_Data_Cleaning/data/tweets_all_clean_dedup_clean.csv`
  - Output (checkpoint/final):
    - `2_Data_Cleaning/data/tweets_gpt5_labeled.csv`
- Checkpointing / resume:
  - If interrupted, re-running will:
    - Load existing `tweets_gpt5_labeled.csv`.
    - Skip already labeled rows (based on existing sentiment columns).
    - Continue labeling only missing ones.

The model is instructed to output strict JSON for each tweet:
- Fields (example; adjust in code if needed):
  - `sentiment` (e.g., `positive`, `negative`, `neutral`)
  - `emotion` (optional, e.g., `joy`, `anger`, `fear`, etc.)

---

## 5. How to Run the Sentiment Pipeline

Prerequisites:
- Python 3.10+ (recommended).
- Installed dependencies:
  - `pandas`
  - `python-dotenv`
  - `openai` (or compatible OpenRouter client)
- A valid OpenRouter (or OpenAI) API key.

1) Set up `.env`

Create `twitter_sentiment_analysis/.env` with at least:

```env
OPENROUTER_API_KEY=your_openrouter_api_key_here
```

(Optionally `OPENAI_API_KEY` if you use OpenAI endpoints.)

2) Ensure input file exists

Confirm:

- `2_Data_Cleaning/data/tweets_all_clean_dedup_clean.csv`

exists and contains:

- `id`
- `created_at`
- `clean_text`
(and any other metadata columns you need).

3) Run the labeling script

From the root of your workspace (or adjusted for your environment):

```bash
python "5th Semester/Data Mining/twitter_sentiment_analysis/2_Data_Cleaning/gpt5_sentiment_pipeline.py"
```

Behavior:
- Reads `tweets_all_clean_dedup_clean.csv`.
- Calls the configured LLM for each tweet.
- Periodically writes/updates:
  - `tweets_gpt5_labeled.csv`
- Safe to interrupt:
  - On restart, it resumes from existing labels.

---

## 6. Daily Sentiment Aggregation

`gpt5_sentiment_pipeline.py` includes logic to aggregate into daily metrics once labeling is done.

Conceptual output (`daily_sentiment_gpt5.csv`):
- `date`
- `count_total`
- `count_pos`, `count_neg`, `count_neu`
- `share_pos`, `share_neg`, `share_neu`
- `net_sentiment` (e.g., `share_pos - share_neg`)

This file is intended to be merged later with:
- IHSG daily index data.
- USD/IDR exchange rate data.
- Other financial indicators.

---

## 7. Extending: Market Data & Correlation (Planned)

Planned / recommended next steps (not all implemented in code yet):

1) Collect IHSG and USD/IDR daily data
   - Align the date range with your tweets.

2) Merge with `daily_sentiment_gpt5.csv`
   - Join on `date`.

3) Analyze relationships:
   - Correlation between sentiment and:
     - IHSG returns.
     - USD/IDR changes.
   - Lead-lag analysis:
     - Does sentiment lead market moves by 1–3 days?

4) Visualizations:
   - Plot sentiment vs IHSG.
   - Plot sentiment vs USD/IDR.
   - Highlight periods of extreme sentiment.

These steps are suitable for a report or thesis on the relationship between social media sentiment and market behavior.

---

## 8. Reproducibility Notes

- All core transformations are in Python scripts (not only notebooks) for repeatability.
- Use `tweet_cleaning.py` everywhere for consistent preprocessing.
- Use the final deduplicated file:
  - `tweets_all_clean_dedup_clean.csv`
  as the single source of truth for sentiment labeling.
- The LLM labeling pipeline is:
  - Deterministic in structure (instructions, schema).
  - Checkpointed to handle ~80k tweets reliably.

---

## 9. Disclaimer

- Running LLM-based sentiment labeling over tens of thousands of tweets will consume API credits.
- Ensure you:
  - Understand your billing and rate limits.
  - Test with a small sample first by configuring the sample limit (if exposed in `gpt5_sentiment_pipeline.py`).

---

## 10. Contact / Ownership

This project is part of a 5th Semester Data Mining assignment focusing on:

- Twitter sentiment analysis
- LLM-assisted labeling
- Potential correlation with Indonesian market indicators.

Adapt paths, keys, and configurations as needed if you reuse this pipeline in another environment.