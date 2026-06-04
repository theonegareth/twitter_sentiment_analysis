import pandas as pd
import yfinance as yf
import os
import glob
from datetime import datetime, timedelta

script_dir = os.path.dirname(os.path.abspath(__file__))

# ============================================================
# 1. TRADING DAYS: Aug 1 – Sep 30, 2025
# ============================================================
print("=" * 70)
print("1. TRADING DAYS (Aug 1 – Sep 30, 2025)")
print("=" * 70)

start_date = "2025-08-01"
end_date   = "2025-09-30"

date_range = pd.bdate_range(start=start_date, end=end_date)
all_dates = pd.date_range(start=start_date, end=end_date)

# Indonesian public holidays in Aug–Sep 2025
# Aug 17: Independence Day (Sunday – no extra day off)
# Aug 29: Isra Mi'raj – not in 2025. Let's check actual holidays
# Sep 5: Maulid Nabi Muhammad SAW (Prophet's Birthday) – Friday
# These are based on the 2025 Indonesian national holiday calendar
indonesia_holidays_2025 = [
    "2025-08-17",  # Independence Day (Sunday, but if observed weekday would be a holiday)
    "2025-09-05",  # Maulid Nabi Muhammad SAW (Prophet's Birthday)
]

# Convert holiday strings to weekdays only (market closure on weekday holidays)
holiday_set = set()
for h in indonesia_holidays_2025:
    d = pd.Timestamp(h)
    # Actual market closure for holiday if it falls on a weekday
    if d.dayofweek < 5:
        holiday_set.add(d.date())

# Standard business days (Mon-Fri) minus holidays
business_dates = [d for d in date_range if d.date() not in holiday_set]

print(f"Total calendar days: {len(all_dates)}")
print(f"Standard business days (Mon-Fri): {len(date_range)}")
print(f"Indonesian holidays on weekdays: {len(holiday_set)}")
if holiday_set:
    for h in sorted(holiday_set):
        print(f"  - {h} ({h.strftime('%A')})")
print(f"TRADING DAYS (business days - holidays): {len(business_dates)}")
print()

# ============================================================
# 2. FETCH ACTUAL MARKET DATA (IHSG and USD/IDR)
# ============================================================
print("=" * 70)
print("2. MARKET DATA RETRIEVAL")
print("=" * 70)

ihsg_dates = set()
usdidr_dates = set()

try:
    print("Fetching IHSG data (^JKSE) from Yahoo Finance...")
    ihsg = yf.download("^JKSE", start=start_date, end="2025-10-01", progress=False)
    if not ihsg.empty:
        ihsg_dates = set(ihsg.index.date)
        print(f"  Retrieved: {len(ihsg_dates)} IHSG trading days with data")
    else:
        print("  WARNING: No IHSG data returned")
except Exception as e:
    print(f"  ERROR fetching IHSG data: {e}")

print()

try:
    print("Fetching USD/IDR data (USDIDR=X) from Yahoo Finance...")
    usdidr = yf.download("USDIDR=X", start=start_date, end="2025-10-01", progress=False)
    if not usdidr.empty:
        usdidr_dates = set(usdidr.index.date)
        print(f"  Retrieved: {len(usdidr_dates)} USD/IDR trading days with data")
    else:
        print("  WARNING: No USD/IDR data returned")
except Exception as e:
    print(f"  ERROR fetching USD/IDR data: {e}")

print()

# ============================================================
# 3. EXTRACT TWEET DATES FROM SCRAPED CSV FILES
# ============================================================
print("=" * 70)
print("3. TWEET DATE EXTRACTION")
print("=" * 70)

scraper_dir = os.path.join(script_dir, "TwitterScrapper-main")

# IHSG-related keyword files
ihsg_keyword_files = [
    "tweets_IHSG_since_2025_08_01_until_20_20251021_142338.csv",
    "tweets_IHSG_since_2025_08_25_until_20_20251020_192834.csv",
    "tweets_ihsg_since_2025_08_25_until_20_20251028_192205.csv",
    "tweets_bursa_efek_since_2025_08_25_un_20251020_194634.csv",
    "tweets_bursa_efek_since_2025_08_01_un_20251024_150659.csv",
    "tweets_saham_turun_since_2025_08_25_u_20251020_192847.csv",
    "tweets_saham_naik_since_2025_09_09_un_20251027_001118.csv",
    "tweets_jual_saham_since_2025_08_25_un_20251020_203623.csv",
    "tweets_panic_selling_since_2025_08_25_20251020_195242.csv",
    "tweets_asing_cabut_since_2025_08_01_u_20251027_192757.csv",
    "tweets_foreign_outflow_since_2025_08__20251027_214841.csv",
    "tweets_pasar_keuangan_since_2025_08_0_20251024_145736.csv",
]

# USD/IDR-related keyword files
usdidr_keyword_files = [
    "tweets_nilai_tukar_since_2025_08_25_u_20251020_204801.csv",
    "tweets_kurs_rupiah_since_2025_08_25_u_20251020_203843.csv",
    "tweets_kurs_rupiah_since_2025_08_01_u_20251027_192629.csv",
    "tweets_melemah_since_2025_08_25_until_20251026_223628.csv",
    "tweets_menguat_since_2025_08_25_until_20251024_163121.csv",
]

def extract_dates_from_csvs(file_list, label):
    """Extract unique dates from a list of CSV files."""
    all_dates = set()
    files_found = 0
    files_with_data = 0
    for fname in file_list:
        fpath = os.path.join(scraper_dir, fname)
        if not os.path.exists(fpath):
            continue
        files_found += 1
        try:
            df = pd.read_csv(fpath)
            if 'created_at' not in df.columns:
                continue
            df['created_at'] = pd.to_datetime(df['created_at'], errors='coerce')
            df = df.dropna(subset=['created_at'])
            if df.empty:
                continue
            files_with_data += 1
            # Filter to our date range
            mask = (df['created_at'] >= start_date) & (df['created_at'] < "2025-10-01")
            dates_in_range = set(df.loc[mask, 'created_at'].dt.date)
            all_dates.update(dates_in_range)
        except Exception as e:
            print(f"  Error reading {fname}: {e}")

    print(f"\n{label}:")
    print(f"  CSV files found: {files_found}")
    print(f"  CSV files with data: {files_with_data}")
    print(f"  Unique dates with tweets: {len(all_dates)}")
    return all_dates

ihsg_tweet_dates = extract_dates_from_csvs(ihsg_keyword_files, "IHSG-related keywords")
usdidr_tweet_dates = extract_dates_from_csvs(usdidr_keyword_files, "USD/IDR-related keywords")

print()

# ============================================================
# 4. PAIRED OBSERVATIONS
# ============================================================
print("=" * 70)
print("4. PAIRED OBSERVATIONS (Market + Tweet data on same day)")
print("=" * 70)

# IHSG: days with both market data AND tweet data
ihsg_paired = ihsg_dates & ihsg_tweet_dates
print(f"\nIHSG Paired Observations:")
print(f"  Days with IHSG market data:  {len(ihsg_dates)}")
print(f"  Days with IHSG tweets:       {len(ihsg_tweet_dates)}")
print(f"  PAIRED (both sources):        {len(ihsg_paired)}")

# USD/IDR: days with both market data AND tweet data
usdidr_paired = usdidr_dates & usdidr_tweet_dates
print(f"\nUSD/IDR Paired Observations:")
print(f"  Days with USD/IDR market data: {len(usdidr_dates)}")
print(f"  Days with USD/IDR tweets:      {len(usdidr_tweet_dates)}")
print(f"  PAIRED (both sources):          {len(usdidr_paired)}")

print()
print("=" * 70)
print("FINAL SUMMARY")
print("=" * 70)
print(f"Trading days (Aug 1 – Sep 30, 2025):      {len(business_dates)}")
print(f"Paired observations for IHSG:               {len(ihsg_paired)}")
print(f"Paired observations for USD/IDR:            {len(usdidr_paired)}")
print(f"Total analytical observations (combined):   {len(ihsg_paired | usdidr_paired)}")
print("=" * 70)

# ============================================================
# 5. DETAILED OUTPUT
# ============================================================
print("\n\nDETAIL: IHSG Paired Dates")
print("-" * 40)
for d in sorted(ihsg_paired):
    print(f"  {d} ({d.strftime('%A')})")

print("\nDETAIL: USD/IDR Paired Dates")
print("-" * 40)
for d in sorted(usdidr_paired):
    print(f"  {d} ({d.strftime('%A')})")
