import os
import re
import unicodedata
from typing import Iterable, List, Optional

import pandas as pd


"""
Reusable cleaning utilities for Twitter/X data, designed for:
- Large volumes (~80k+ tweets)
- Indonesian + English content
- Downstream sentiment analysis / classification (labels added later)

Usage (example from a notebook):

    from tweet_cleaning import load_and_clean_folder

    df_clean = load_and_clean_folder(
        folder_path="5th Semester/Data Mining/twitter_sentiment_analysis/2_Data_Cleaning/data",
        glob_pattern="tweets__*.csv",
        text_column="text",
        id_column="id",
    )

    # Inspect
    df_clean.head()
"""


URL_PATTERN = re.compile(r"https?://\S+")
MENTION_PATTERN = re.compile(r"@\w+")
HASHTAG_PATTERN = re.compile(r"#(\w+)")
MULTISPACE_PATTERN = re.compile(r"\s+")
EMOJI_PATTERN = re.compile(
    "["
    "\U0001F600-\U0001F64F"  # emoticons
    "\U0001F300-\U0001F5FF"  # symbols & pictographs
    "\U0001F680-\U0001F6FF"  # transport & map symbols
    "\U0001F1E0-\U0001F1FF"  # flags
    "\U00002700-\U000027BF"  # dingbats
    "\U0001F900-\U0001F9FF"  # supplemental symbols and pictographs
    "]+",
    flags=re.UNICODE,
)


def normalize_text(text: str) -> str:
    """
    Basic normalization:
    - Ensure string
    - Normalize unicode
    - Strip leading/trailing spaces
    """
    if not isinstance(text, str):
        text = "" if pd.isna(text) else str(text)
    text = unicodedata.normalize("NFKC", text)
    return text.strip()


def clean_tweet_text(
    text: str,
    *,
    keep_hashtag_word: bool = True,
    keep_mention_token: bool = False,
    keep_case: bool = False,
    remove_emoji: bool = False,
) -> str:
    """
    Clean a single tweet for sentiment analysis.

    Steps:
    - Normalize to string and unicode-safe
    - Remove URLs
    - Remove or normalize mentions
    - Optionally keep hashtag words (e.g. "#JagaJakarta" -> "Jagajakarta" or "JagaJakarta")
      for task-specific signal; here default keeps the word without '#'
    - Remove emoji (optional; default keep, since emoji carry sentiment)
    - Remove RT markers
    - Remove excessive punctuation and extra whitespace

    Parameters:
        text: Raw tweet text.
        keep_hashtag_word: If True, replace "#word" with "word".
        keep_mention_token: If True, replace "@user" with "@user" token;
                            If False, remove mentions.
        keep_case: If False, lowercase everything (recommended for ML).
        remove_emoji: If True, strip emojis; else keep them.

    Returns:
        Cleaned text string.
    """
    t = normalize_text(text)

    # Remove URLs
    t = URL_PATTERN.sub(" ", t)

    # Handle mentions
    if keep_mention_token:
        # Replace "@username" with generic @user to keep structure w/o identity
        t = MENTION_PATTERN.sub(" @user ", t)
    else:
        t = MENTION_PATTERN.sub(" ", t)

    # Handle hashtags
    def _hashtag_repl(match: re.Match) -> str:
        word = match.group(1)
        return f" {word} " if keep_hashtag_word else " "

    t = HASHTAG_PATTERN.sub(_hashtag_repl, t)

    # Remove "RT" retweet markers at start
    t = re.sub(r"^\s*RT\s+", " ", t)

    # Optionally remove emojis
    if remove_emoji:
        t = EMOJI_PATTERN.sub(" ", t)

    # Remove leftover non-printable chars
    t = "".join(ch for ch in t if ch.isprintable() or ch.isspace())

    # Collapse whitespace
    t = MULTISPACE_PATTERN.sub(" ", t).strip()

    # Lowercase if desired
    if not keep_case:
        t = t.lower()

    return t


def clean_dataframe(
    df: pd.DataFrame,
    text_column: str = "text",
    id_column: Optional[str] = "id",
    drop_na_text: bool = True,
    **clean_kwargs,
) -> pd.DataFrame:
    """
    Apply tweet cleaning to a DataFrame.

    - Expects a column with raw tweet text.
    - Adds a 'clean_text' column.
    - Optionally drops rows where clean_text is empty.

    Parameters:
        df: Input DataFrame.
        text_column: Name of the column containing raw tweet text.
        id_column: Optional id column name; if provided and present, kept for reference.
        drop_na_text: Drop rows where clean_text is empty after cleaning.
        **clean_kwargs: Passed to clean_tweet_text().

    Returns:
        New DataFrame with:
            - id_column (if exists)
            - original text column
            - 'clean_text'
            - remaining metadata columns preserved.
    """
    if text_column not in df.columns:
        raise ValueError(f"text_column '{text_column}' not found. Available: {list(df.columns)}")

    df = df.copy()

    # Apply cleaning
    df["clean_text"] = df[text_column].apply(lambda x: clean_tweet_text(x, **clean_kwargs))

    if drop_na_text:
        before = len(df)
        df = df[df["clean_text"].str.strip() != ""]
        df = df[~df["clean_text"].isna()]
        df = df.reset_index(drop=True)
        after = len(df)
        print(f"[tweet_cleaning.clean_dataframe()] Dropped {before - after} empty/invalid rows.")

    return df


def load_and_clean_file(
    file_path: str,
    text_column: str = "text",
    id_column: Optional[str] = "id",
    encoding: str = "utf-8",
    **clean_kwargs,
) -> pd.DataFrame:
    """
    Load a single CSV of tweets and return cleaned DataFrame.

    Parameters:
        file_path: CSV path.
        text_column: Raw text column name.
        id_column: Optional id column name.
        encoding: File encoding.
        **clean_kwargs: Passed to clean_dataframe() / clean_tweet_text().

    Returns:
        Cleaned DataFrame.
    """
    print(f"[tweet_cleaning.load_and_clean_file()] Loading {file_path}...")
    df = pd.read_csv(file_path, encoding=encoding)
    return clean_dataframe(df, text_column=text_column, id_column=id_column, **clean_kwargs)


def load_and_clean_folder(
    folder_path: str,
    glob_pattern: str = "*.csv",
    text_column: str = "text",
    id_column: Optional[str] = "id",
    encoding: str = "utf-8",
    concat_axis: int = 0,
    **clean_kwargs,
) -> pd.DataFrame:
    """
    Load multiple CSV tweet files from a folder, clean them, and concatenate.

    Parameters:
        folder_path: Directory containing CSVs.
        glob_pattern: Filename pattern (e.g. 'tweets__*.csv').
        text_column: Raw text column name.
        id_column: Optional id column name.
        encoding: File encoding to try.
        concat_axis: Axis for concatenation (default rows).
        **clean_kwargs: Passed to clean_dataframe() / clean_tweet_text().

    Returns:
        Single concatenated cleaned DataFrame.
    """
    import glob

    pattern = os.path.join(folder_path, glob_pattern)
    files: List[str] = sorted(glob.glob(pattern))

    if not files:
        raise FileNotFoundError(f"No files matched pattern: {pattern}")

    print(f"[tweet_cleaning.load_and_clean_folder()] Found {len(files)} files.")
    dfs: List[pd.DataFrame] = []

    for path in files:
        try:
            df_clean = load_and_clean_file(
                path,
                text_column=text_column,
                id_column=id_column,
                encoding=encoding,
                **clean_kwargs,
            )
            dfs.append(df_clean)
        except Exception as e:
            print(f"[tweet_cleaning.load_and_clean_folder()] Skipping {path} due to error: {e}")

    if not dfs:
        raise RuntimeError("All files failed to load/clean. Check errors above.")

    combined = pd.concat(dfs, axis=concat_axis, ignore_index=True)
    print(f"[tweet_cleaning.load_and_clean_folder()] Combined shape: {combined.shape}")
    return combined


if __name__ == "__main__":
    """
    Minimal CLI-style usage for quick testing on a single file.
    Adjust the path and column names as needed, then run:

        python tweet_cleaning.py

    This will create:
        tweets_clean_sample.csv  (first 100 cleaned rows)
    """
    sample_file = r"5th Semester\Data Mining\twitter_sentiment_analysis\2_Data_Cleaning\data\tweets__JagaJakarta_since_2025_08_25__20251020_194748.csv"

    if os.path.exists(sample_file):
        df_clean_sample = load_and_clean_file(
            sample_file,
            text_column="text",
            id_column="id",
            keep_hashtag_word=True,
            keep_mention_token=False,
            keep_case=False,
            remove_emoji=False,
        )
        out_path = os.path.join(
            os.path.dirname(sample_file),
            "tweets_clean_sample.csv",
        )
        df_clean_sample.head(100).to_csv(out_path, index=False, encoding="utf-8-sig")
        print(f"[tweet_cleaning.__main__] Wrote sample cleaned data to: {out_path}")
    else:
        print(
            "[tweet_cleaning.__main__] Sample file not found. "
            "Import this module in your notebook and call load_and_clean_folder() instead."
        )