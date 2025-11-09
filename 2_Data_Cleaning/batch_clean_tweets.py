import os
import glob
import pandas as pd

from tweet_cleaning import (
    load_and_clean_file,
    clean_dataframe,
)


"""
Batch cleaner for your Twitter/X datasets.

Features:
1. For every raw tweets__*.csv in the data folder:
   - Load
   - Clean text into 'clean_text'
   - Save as *_clean.csv next to the original file

2. Build a merged file tweets_all_clean.csv:
   - Concatenate all *_clean.csv
   - Useful for training / labeling on a single dataset

Defaults are tuned to:
- Keep hashtag words as tokens (e.g. #JagaJakarta -> jagajakarta)
- Remove mentions (@usernames)
- Keep emojis (they carry sentiment)
- Lowercase output
You can adjust behavior via CLEAN_KWARGS below.
"""


# Path to folder containing your tweet CSV parts
DATA_FOLDER = os.path.join(
    "5th Semester",
    "Data Mining",
    "twitter_sentiment_analysis",
    "2_Data_Cleaning",
    "data",
)

# Raw CSV filename pattern
RAW_PATTERN = "tweets_*.csv"

# Cleaned per-file suffix
CLEAN_SUFFIX = "_clean.csv"

# Output merged file name
MERGED_OUTPUT = "tweets_all_clean.csv"

# Cleaning configuration (passed into tweet_cleaning.clean_tweet_text)
CLEAN_KWARGS = dict(
    keep_hashtag_word=True,   # keep words from hashtags
    keep_mention_token=False, # strip @mentions
    keep_case=False,          # lowercase all text
    remove_emoji=False,       # keep emojis
)


def clean_all_parts(
    data_folder: str = DATA_FOLDER,
    raw_pattern: str = RAW_PATTERN,
    clean_suffix: str = CLEAN_SUFFIX,
) -> list:
    """
    Clean each raw CSV part into its own *_clean.csv.

    Returns:
        List of paths to the cleaned per-file CSVs.
    """
    pattern = os.path.join(data_folder, raw_pattern)
    raw_files = sorted(glob.glob(pattern))

    if not raw_files:
        print(f"[batch_clean_tweets.clean_all_parts] No files matched: {pattern}")
        return []

    print(f"[batch_clean_tweets.clean_all_parts] Found {len(raw_files)} raw files.")

    cleaned_files = []

    for raw_path in raw_files:
        try:
            print(f"[batch_clean_tweets.clean_all_parts] Cleaning: {raw_path}")
            df_clean = load_and_clean_file(
                raw_path,
                text_column="text",
                id_column="id",
                **CLEAN_KWARGS,
            )

            base, _ = os.path.splitext(raw_path)
            clean_path = f"{base}{clean_suffix}"
            df_clean.to_csv(clean_path, index=False, encoding="utf-8-sig")
            cleaned_files.append(clean_path)

            print(
                f"[batch_clean_tweets.clean_all_parts] Wrote {len(df_clean)} rows -> {clean_path}"
            )
        except Exception as e:
            print(
                f"[batch_clean_tweets.clean_all_parts] ERROR processing {raw_path}: {e}"
            )

    if not cleaned_files:
        print(
            "[batch_clean_tweets.clean_all_parts] No cleaned files were produced. Check errors above."
        )

    return cleaned_files


def merge_clean_files(
    data_folder: str = DATA_FOLDER,
    clean_suffix: str = CLEAN_SUFFIX,
    merged_output: str = MERGED_OUTPUT,
) -> str:
    """
    Merge all *_clean.csv files into one combined CSV.

    Returns:
        Path to the merged CSV (if created), else empty string.
    """
    pattern = os.path.join(data_folder, f"*{clean_suffix}")
    clean_files = sorted(glob.glob(pattern))

    if not clean_files:
        print(
            f"[batch_clean_tweets.merge_clean_files] No cleaned files found matching: {pattern}"
        )
        return ""

    print(
        f"[batch_clean_tweets.merge_clean_files] Found {len(clean_files)} cleaned files. Merging..."
    )

    dfs = []
    for path in clean_files:
        try:
            df = pd.read_csv(path)
            dfs.append(df)
            print(
                f"[batch_clean_tweets.merge_clean_files] Loaded {len(df)} rows from {path}"
            )
        except Exception as e:
            print(
                f"[batch_clean_tweets.merge_clean_files] ERROR reading {path}: {e}"
            )

    if not dfs:
        print(
            "[batch_clean_tweets.merge_clean_files] All cleaned files failed to load. No merged file created."
        )
        return ""

    merged_df = pd.concat(dfs, axis=0, ignore_index=True)
    merged_path = os.path.join(data_folder, merged_output)

    # If target file is locked or read-only, write to a temporary name instead
    try:
        merged_df.to_csv(merged_path, index=False, encoding="utf-8-sig")
    except PermissionError:
        fallback_path = os.path.join(data_folder, f"tmp_{merged_output}")
        print(
            f"[batch_clean_tweets.merge_clean_files] Permission denied writing {merged_path}, "
            f"writing to {fallback_path} instead."
        )
        merged_path = fallback_path
        merged_df.to_csv(merged_path, index=False, encoding="utf-8-sig")

    print(
        f"[batch_clean_tweets.merge_clean_files] Wrote merged file with {len(merged_df)} rows -> {merged_path}"
    )

    return merged_path


def run_full_pipeline():
    """
    1) Clean all tweet parts into per-file *_clean.csv.
    2) Merge all *_clean.csv into tweets_all_clean.csv.
    """
    print("[batch_clean_tweets.run_full_pipeline] Starting batch cleaning pipeline...")
    cleaned_files = clean_all_parts()

    if not cleaned_files:
        print(
            "[batch_clean_tweets.run_full_pipeline] No cleaned files; aborting merge."
        )
        return

    merged_path = merge_clean_files()

    if merged_path:
        print(
            f"[batch_clean_tweets.run_full_pipeline] Pipeline complete. Merged dataset at: {merged_path}"
        )
    else:
        print(
            "[batch_clean_tweets.run_full_pipeline] Cleaning done, but merged file was not created."
        )


if __name__ == "__main__":
    """
    Example usage:
        python batch_clean_tweets.py

    Make sure:
    - All your raw tweets__*.csv parts are in:
        5th Semester/Data Mining/twitter_sentiment_analysis/2_Data_Cleaning/data
    - Then run this script from the project root or via VS Code terminal.

    It will:
    - Create per-file: tweets__...__20251020_194748_clean.csv
    - Create merged:   tweets_all_clean.csv
    """
    run_full_pipeline()