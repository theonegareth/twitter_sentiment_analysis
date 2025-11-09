import os
import time
from typing import List, Dict, Any, Optional

import pandas as pd
from openai import OpenAI

# Auto-load .env so OPENROUTER_API_KEY from the correct project root is visible
try:
    from dotenv import load_dotenv
    # This script lives in .../twitter_sentiment_analysis/2_Data_Cleaning/
    # The .env is in .../twitter_sentiment_analysis/.env (one level up, not two).
    ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
    env_path = os.path.join(ROOT_DIR, ".env")
    if os.path.exists(env_path):
        load_dotenv(env_path)
        print(f"[gpt5_sentiment_pipeline] Loaded .env from {env_path}")
    else:
        print(f"[gpt5_sentiment_pipeline] .env not found at {env_path}, relying on system env vars.")
except ImportError:
    print("[gpt5_sentiment_pipeline] python-dotenv not installed; ensure env vars are set manually.")


"""
End-to-end GPT-5 sentiment pipeline for your cleaned tweets.

What this script does:

1) Load final deduplicated tweets:
   - Input: tweets_all_clean_dedup.csv
   - Location:
     5th Semester/Data Mining/twitter_sentiment_analysis/2_Data_Cleaning/data

2) Call GPT-5 to assign sentiment (and optional emotion) per tweet:
   - Uses clean_text as input
   - Adds:
       sentiment_gpt5 in {Positive, Negative, Neutral}
       emotion_gpt5   in {love, anger, sadness, fear, happy, neutral} (optional)

3) Save labeled tweets:
   - Output: tweets_gpt5_labeled.csv

4) Aggregate to daily sentiment:
   - Output: daily_sentiment_gpt5.csv
   - Columns include:
       date, total_tweets, pos, neg, neu, net_sent, pos_share, neg_share

After that, you can:
- Join daily_sentiment_gpt5.csv with IHSG & USD/IDR market_data.csv in a notebook
- Compute correlations and lead/lag relationships.


REQUIREMENTS / SETUP:

- Install:
    pip install openai pandas

- Set your API key securely (DO NOT hardcode it here):
    On Windows PowerShell:
        $env:OPENAI_API_KEY = "sk-..."
    On cmd.exe:
        set OPENAI_API_KEY=sk-...
    Or use a .env / environment manager.

- Then run from project root:
    python "5th Semester/Data Mining/twitter_sentiment_analysis/2_Data_Cleaning/gpt5_sentiment_pipeline.py"

NOTE:
- This script is designed for batch labeling with rate limiting and progress logs.
- By default, it processes all rows. You can start with SAMPLE_LIMIT to test.
"""


# ---------- CONFIGURATION ----------

# This script lives in:  .../twitter_sentiment_analysis/2_Data_Cleaning/
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# All data files are under the local "data" folder next to this script.
INPUT_CSV = os.path.join("data", "tweets_all_clean_dedup_clean.csv")
LABELED_CSV = os.path.join("data", "tweets_gpt5_labeled.csv")
DAILY_SENTIMENT_CSV = os.path.join("data", "daily_sentiment_gpt5.csv")

# Model name for OpenRouter (change if you use another model)
# For your case: openrouter/polaris-alpha
GPT5_MODEL = "openrouter/polaris-alpha"

# Safety: set a limit for testing; set to None to run full dataset
SAMPLE_LIMIT: Optional[int] = None  # e.g., 500 for dry-run; None for all

# Throttling between API calls (seconds)
REQUEST_SLEEP = 0  # adjust to respect rate limits / avoid overload

# -----------------------------------


def init_client() -> OpenAI:
    """
    Initialize client to send all requests via OpenRouter or direct OpenAI.

    Priority:
    1) If OPENROUTER_API_KEY is set -> use OpenRouter at https://openrouter.ai/api/v1
    2) Else if OPENAI_API_KEY is set  -> use OpenAI default endpoint

    This avoids relying on external dotenv loading; it reads the real
    environment variables seen by the Python process.
    """
    openrouter_key = os.getenv("OPENROUTER_API_KEY")
    openai_key = os.getenv("OPENAI_API_KEY")

    if openrouter_key:
        base_url = "https://openrouter.ai/api/v1"
        client = OpenAI(
            api_key=openrouter_key,
            base_url=base_url,
            default_headers={
                # Optional but recommended by OpenRouter for identification:
                "HTTP-Referer": "https://github.com/jakarta-sentiment-corr",
                "X-Title": "jakarta-sentiment-correlation-project",
            },
        )
        print("[init_client] Using OpenRouter with OPENROUTER_API_KEY.")
        return client

    if openai_key:
        # Fallback: direct OpenAI if user prefers/has only this configured
        client = OpenAI(api_key=openai_key)
        print("[init_client] Using direct OpenAI with OPENAI_API_KEY.")
        return client

    raise RuntimeError(
        "No API key configured. Set either OPENROUTER_API_KEY (preferred) or OPENAI_API_KEY "
        "in your environment or .env before running."
    )


def call_gpt5_sentiment(client: OpenAI, text: str) -> Dict[str, Any]:
    """
    Call GPT-5 to get sentiment and emotion for a single tweet.

    The model is instructed to ONLY return a strict JSON object:
        {
          "sentiment": "Positive/Negative/Neutral",
          "emotion": "love/anger/sadness/fear/happy/neutral"
        }

    Returns:
        dict with keys: sentiment, emotion
        or fallback {"sentiment": "Unknown", "emotion": "Unknown"} on any issue.
    """
    if not isinstance(text, str):
        text = "" if pd.isna(text) else str(text)

    text = text.strip()
    if not text:
        return {"sentiment": "Unknown", "emotion": "Unknown"}

    system_or_dev_prompt = (
        "You are an expert sentiment analysis assistant for Indonesian and English tweets "
        "about Jakarta and related topics. "
        "Classify the overall sentiment of the tweet as exactly one of: "
        "\"Positive\", \"Negative\", or \"Neutral\". "
        "Additionally, classify the dominant emotion as exactly one of: "
        "\"love\", \"anger\", \"sadness\", \"fear\", \"happy\", or \"neutral\". "
        "Return ONLY a single valid JSON object in this exact format:\n"
        '{"sentiment": "Positive/Negative/Neutral", '
        '"emotion": "love/anger/sadness/fear/happy/neutral"}\n'
        "No explanations, no extra keys, no text outside JSON."
    )

    try:
        # Using Responses API style for GPT-5 (adjust if your environment differs)
        resp = client.responses.create(
            model=GPT5_MODEL,
            input=[
                {"role": "developer", "content": system_or_dev_prompt},
                {"role": "user", "content": text},
            ],
            reasoning={"effort": "minimal"},
            text={"verbosity": "low"},
        )

        raw = resp.output_text.strip()

        # Validate as JSON manually (without assuming perfect behavior)
        import json

        try:
            data = json.loads(raw)
        except json.JSONDecodeError:
            # Try to recover if extra text is present (very defensive)
            # Find first '{' and last '}' and attempt substring parse
            start = raw.find("{")
            end = raw.rfind("}")
            if start != -1 and end != -1 and end > start:
                try:
                    data = json.loads(raw[start : end + 1])
                except Exception:
                    return {"sentiment": "Unknown", "emotion": "Unknown"}
            else:
                return {"sentiment": "Unknown", "emotion": "Unknown"}

        # Basic schema check
        sentiment = str(data.get("sentiment", "Unknown"))
        emotion = str(data.get("emotion", "Unknown"))

        if sentiment not in ("Positive", "Negative", "Neutral"):
            sentiment = "Unknown"
        if emotion not in ("love", "anger", "sadness", "fear", "happy", "neutral"):
            emotion = "Unknown"

        return {"sentiment": sentiment, "emotion": emotion}

    except Exception as e:
        print(f"[call_gpt5_sentiment] Error: {e}")
        return {"sentiment": "Unknown", "emotion": "Unknown"}


def label_tweets_with_gpt5(
    input_path: str,
    output_path: str,
    client: OpenAI,
    sample_limit: Optional[int] = SAMPLE_LIMIT,
    resume_if_exists: bool = True,
) -> pd.DataFrame:
    """
    Label tweets in input_path with GPT-5 sentiment.

    - Reads tweets_all_clean_dedup.csv
    - Adds sentiment_gpt5, emotion_gpt5
    - Writes tweets_gpt5_labeled.csv
    - Supports resume: if output exists, skips rows that already have sentiment_gpt5.

    Returns:
        Final labeled DataFrame.
    """
    print(f"[label_tweets_with_gpt5] Loading: {input_path}")
    df = pd.read_csv(input_path)

    # Optional sub-sample for testing/cost-control
    if sample_limit is not None and sample_limit > 0:
        df = df.iloc[:sample_limit].copy()
        print(f"[label_tweets_with_gpt5] Using sample_limit={sample_limit}, rows={len(df)}")

    # Prepare/resume
    if resume_if_exists and os.path.exists(output_path):
        print(f"[label_tweets_with_gpt5] Resuming from existing labeled file: {output_path}")
        df_labeled = pd.read_csv(output_path)

        # Ensure merge key
        if "id" in df.columns and "id" in df_labeled.columns:
            # Use id as key
            df = df.merge(
                df_labeled[["id", "sentiment_gpt5", "emotion_gpt5"]],
                on="id",
                how="left",
                suffixes=("", "_old"),
            )
        else:
            # Fallback to index-based alignment
            df["sentiment_gpt5"] = df_labeled.get("sentiment_gpt5")
            df["emotion_gpt5"] = df_labeled.get("emotion_gpt5")
    else:
        # Fresh run
        if "sentiment_gpt5" not in df.columns:
            df["sentiment_gpt5"] = pd.NA
        if "emotion_gpt5" not in df.columns:
            df["emotion_gpt5"] = pd.NA

    total = len(df)
    to_process = df["sentiment_gpt5"].isna() | (df["sentiment_gpt5"] == "")

    print(f"[label_tweets_with_gpt5] Total rows: {total}")
    print(f"[label_tweets_with_gpt5] Rows needing GPT-5 calls: {to_process.sum()}")

    processed = 0
    for idx in df[to_process].index:
        text = df.at[idx, "clean_text"] if "clean_text" in df.columns else df.at[idx, "text"]

        res = call_gpt5_sentiment(client, str(text))
        df.at[idx, "sentiment_gpt5"] = res.get("sentiment", "Unknown")
        df.at[idx, "emotion_gpt5"] = res.get("emotion", "Unknown")

        processed += 1
        if processed % 50 == 0 or processed == 1:
            print(
                f"[label_tweets_with_gpt5] Processed {processed}/{to_process.sum()} "
                f"({processed/to_process.sum():.1%})"
            )
            # Save checkpoint
            df.to_csv(output_path, index=False, encoding="utf-8-sig")

        time.sleep(REQUEST_SLEEP)

    # Final save
    df.to_csv(output_path, index=False, encoding="utf-8-sig")
    print(f"[label_tweets_with_gpt5] Completed. Labeled file written to: {output_path}")

    # Basic distribution summary
    if "sentiment_gpt5" in df.columns:
        print("[label_tweets_with_gpt5] Sentiment distribution:")
        print(df["sentiment_gpt5"].value_counts(dropna=False))

    return df


def aggregate_daily_sentiment(
    labeled_df: pd.DataFrame,
    output_path: str,
    created_at_col: str = "created_at",
    sentiment_col: str = "sentiment_gpt5",
) -> pd.DataFrame:
    """
    Aggregate per-tweet GPT-5 labels into daily sentiment metrics.

    Output columns:
        date
        total_tweets
        pos, neg, neu
        pos_share, neg_share
        net_sent  = (pos - neg) / total_tweets

    Returns:
        daily sentiment DataFrame.
    """
    if created_at_col not in labeled_df.columns:
        raise ValueError(f"Column '{created_at_col}' not found in labeled_df.")

    if sentiment_col not in labeled_df.columns:
        raise ValueError(f"Column '{sentiment_col}' not found in labeled_df.")

    df = labeled_df.copy()

    # Parse created_at to datetime (robust)
    df[created_at_col] = pd.to_datetime(df[created_at_col], errors="coerce")
    df = df.dropna(subset=[created_at_col])

    df["date"] = df[created_at_col].dt.date

    # Normalize sentiment labels
    s = df[sentiment_col].fillna("Unknown").astype(str)

    df["is_pos"] = (s == "Positive").astype(int)
    df["is_neg"] = (s == "Negative").astype(int)
    df["is_neu"] = (s == "Neutral").astype(int)

    grouped = df.groupby("date").agg(
        total_tweets=("id", "count") if "id" in df.columns else (sentiment_col, "count"),
        pos=("is_pos", "sum"),
        neg=("is_neg", "sum"),
        neu=("is_neu", "sum"),
    ).reset_index()

    # Shares and net sentiment
    grouped["pos_share"] = grouped["pos"] / grouped["total_tweets"]
    grouped["neg_share"] = grouped["neg"] / grouped["total_tweets"]
    grouped["net_sent"] = (grouped["pos"] - grouped["neg"]) / grouped["total_tweets"]

    # Sort by date for time-series coherence
    grouped = grouped.sort_values("date").reset_index(drop=True)

    grouped.to_csv(output_path, index=False, encoding="utf-8-sig")
    print(f"[aggregate_daily_sentiment] Daily sentiment written to: {output_path}")
    print("[aggregate_daily_sentiment] Head:")
    print(grouped.head())

    return grouped


def run_pipeline():
    """
    Run the full GPT-5 sentiment pipeline:

    1) Load tweets_all_clean_dedup_clean.csv
    2) Label with GPT-5 (checkpoint-safe)
    3) Aggregate to daily_sentiment_gpt5.csv
    """
    # Build paths strictly as BASE_DIR + relative file config (no extra nesting)
    input_path = os.path.join(BASE_DIR, INPUT_CSV)
    labeled_path = os.path.join(BASE_DIR, LABELED_CSV)
    daily_path = os.path.join(BASE_DIR, DAILY_SENTIMENT_CSV)

    if not os.path.exists(input_path):
        raise FileNotFoundError(
            f"Input file not found: {input_path}\n"
            f"Make sure you've run the batch cleaning & dedup steps first."
        )

    client = init_client()

    # Step 1-2: Label tweets
    df_labeled = label_tweets_with_gpt5(
        input_path=input_path,
        output_path=labeled_path,
        client=client,
        sample_limit=SAMPLE_LIMIT,
        resume_if_exists=True,
    )

    # Step 3: Aggregate daily sentiment
    aggregate_daily_sentiment(
        labeled_df=df_labeled,
        output_path=daily_path,
        created_at_col="created_at",
        sentiment_col="sentiment_gpt5",
    )

    print("[run_pipeline] Pipeline finished successfully.")
    print(f"  Labeled tweets: {labeled_path}")
    print(f"  Daily sentiment: {daily_path}")


if __name__ == "__main__":
    run_pipeline()