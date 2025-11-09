import os
import pandas as pd

# Deduplicate the merged clean tweets file and write the final dataset.
#
# Usage:
#   1. Ensure you have your merged file from batch_clean_tweets:
#        5th Semester/Data Mining/twitter_sentiment_analysis/2_Data_Cleaning/data/tweets_all_clean_clean_clean.csv
#      (If your merged file has a different name, update MERGED_INPUT below.)
#
#   2. From the project root directory, run (single line):
#        python "5th Semester/Data Mining/twitter_sentiment_analysis/2_Data_Cleaning/deduplicate_clean_tweets.py"
#
#   3. Output:
#        5th Semester/Data Mining/twitter_sentiment_analysis/2_Data_Cleaning/data/tweets_all_clean_dedup.csv
#
#   This file will be used as input to:
#        gpt5_sentiment_pipeline.py


DATA_FOLDER = os.path.join(
    "5th Semester",
    "Data Mining",
    "twitter_sentiment_analysis",
    "2_Data_Cleaning",
    "data",
)

# Adjust this if your merged file name changes
MERGED_INPUT = "tweets_all_clean_clean_clean.csv"
DEDUP_OUTPUT = "tweets_all_clean_dedup.csv"


def main() -> None:
    src = os.path.join(DATA_FOLDER, MERGED_INPUT)
    dst = os.path.join(DATA_FOLDER, DEDUP_OUTPUT)

    if not os.path.exists(src):
        raise FileNotFoundError(
            f"Merged input file not found:\n  {src}\n"
            f"Make sure batch_clean_tweets.py has run and produced this file, "
            f"or update MERGED_INPUT in deduplicate_clean_tweets.py."
        )

    print(f"[deduplicate_clean_tweets] Reading: {src}")
    df = pd.read_csv(src)

    before = len(df)
    print(f"[deduplicate_clean_tweets] Rows before dedupe: {before}")

    # 1) Drop duplicate tweet IDs if present
    if "id" in df.columns:
        df = df.drop_duplicates(subset=["id"])
        after_id = len(df)
        print(
            f"[deduplicate_clean_tweets] After id dedupe: {after_id} "
            f"(dropped {before - after_id})"
        )
    else:
        after_id = before
        print("[deduplicate_clean_tweets] Column 'id' not found; skipping id-based dedupe.")

    # 2) Drop exact duplicate clean_text values if present
    if "clean_text" in df.columns:
        df = df.drop_duplicates(subset=["clean_text"])
        after_text = len(df)
        print(
            f"[deduplicate_clean_tweets] After clean_text dedupe: {after_text} "
            f"(dropped {after_id - after_text})"
        )
    else:
        after_text = after_id
        print(
            "[deduplicate_clean_tweets] Column 'clean_text' not found; "
            "skipping text-based dedupe."
        )

    # Ensure output directory exists
    os.makedirs(DATA_FOLDER, exist_ok=True)

    # Write final deduplicated dataset
    df.to_csv(dst, index=False, encoding="utf-8-sig")

    print(f"[deduplicate_clean_tweets] Wrote final deduped dataset to: {dst}")
    print("[deduplicate_clean_tweets] Done.")


if __name__ == "__main__":
    main()