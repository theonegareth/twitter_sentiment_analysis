import pandas as pd
import os
import shutil

# Paths
source_dir = "."
target_ihsg = "../../../HuggingfaceDataset/daily-IHSG/ihsg_daily.csv"
target_usd_raw = "../../../HuggingfaceDataset/daily-usd-idr/usd_idr_daily.csv"
target_usd_clean = "../../../HuggingfaceDataset/daily-usd-idr/usd_idr_daily_cleaned.csv"

# 1. Fix IHSG CSV
print("Processing IHSG CSV...")
ihsg_raw = pd.read_csv(os.path.join(source_dir, "ihsg_daily.csv"), header=[0,1,2])
# The DataFrame has MultiIndex columns. We need to extract the data.
# The column levels: level0 = ['Price', 'Close', 'High', 'Low', 'Open', 'Volume']
# level1 = ['Ticker', '^JKSE', ...]
# level2 = ['Date', 'Unnamed: 1_level_2', ...]
# The actual data rows start at row index 0 (the 'Date' column is under level2? Actually the 'Date' column is under level0='Price', level1='Ticker', level2='Date'
# Let's flatten the columns.
# We'll just take the second row (index 1) as column names? Actually we want Open, High, Low, Close, Volume.
# Let's inspect the structure.
print("Columns:", ihsg_raw.columns.tolist())
print("First few rows:")
print(ihsg_raw.head())

# For simplicity, we can extract the data as a simple DataFrame with columns: Date, Open, High, Low, Close, Volume
# The 'Price' column contains dates? Actually the 'Price' column is the date column.
# Let's rename columns.
ihsg_raw.columns = ['_'.join(col).strip() for col in ihsg_raw.columns.values]
print("Flattened columns:", ihsg_raw.columns.tolist())

# The column 'Price_Ticker_Date' contains dates.
# The column 'Close_^JKSE_Unnamed: 1_level_2' contains Close? Actually that's Close.
# The column 'High_^JKSE_Unnamed: 2_level_2' contains High.
# The column 'Low_^JKSE_Unnamed: 3_level_2' contains Low.
# The column 'Open_^JKSE_Unnamed: 4_level_2' contains Open.
# The column 'Volume_^JKSE_Unnamed: 5_level_2' contains Volume.
# Let's map.
rename_map = {
    'Price_Ticker_Date': 'Date',
    'Close_^JKSE_Unnamed: 1_level_2': 'Close',
    'High_^JKSE_Unnamed: 2_level_2': 'High',
    'Low_^JKSE_Unnamed: 3_level_2': 'Low',
    'Open_^JKSE_Unnamed: 4_level_2': 'Open',
    'Volume_^JKSE_Unnamed: 5_level_2': 'Volume'
}
ihsg_clean = ihsg_raw.rename(columns=rename_map)
# Reorder columns
ihsg_clean = ihsg_clean[['Date', 'Open', 'High', 'Low', 'Close', 'Volume']]
print("Cleaned IHSG head:")
print(ihsg_clean.head())

# Save to target
ihsg_clean.to_csv(target_ihsg, index=False)
print(f"Saved cleaned IHSG to {target_ihsg}")

# 2. USD/IDR raw CSV (already fine)
print("\nProcessing USD/IDR raw CSV...")
usd_raw = pd.read_csv(os.path.join(source_dir, "usd_idr_daily.csv"))
print(f"USD/IDR raw shape: {usd_raw.shape}")
print(usd_raw.head())
# Copy as is
usd_raw.to_csv(target_usd_raw, index=False)
print(f"Copied raw USD/IDR to {target_usd_raw}")

# 3. USD/IDR cleaned CSV (keep only Date, Open, High, Low, Close)
usd_clean = usd_raw[['Date', 'Open', 'High', 'Low', 'Close']].copy()
usd_clean.to_csv(target_usd_clean, index=False)
print(f"Saved cleaned USD/IDR to {target_usd_clean}")

print("\nDone.")