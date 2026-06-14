import pandas as pd
import os

# IHSG
ihsg_path = "../../../HuggingfaceDataset/daily-IHSG/ihsg_daily.csv"
df_ihsg = pd.read_csv(ihsg_path)
ihsg_count = len(df_ihsg)
ihsg_start = df_ihsg['Date'].min()
ihsg_end = df_ihsg['Date'].max()
print(f"IHSG: {ihsg_count} rows, from {ihsg_start} to {ihsg_end}")

# USD/IDR raw
usd_raw_path = "../../../HuggingfaceDataset/daily-usd-idr/usd_idr_daily.csv"
df_usd = pd.read_csv(usd_raw_path)
usd_count = len(df_usd)
usd_start = df_usd['Date'].min()
usd_end = df_usd['Date'].max()
print(f"USD/IDR raw: {usd_count} rows, from {usd_start} to {usd_end}")

# USD/IDR cleaned
usd_clean_path = "../../../HuggingfaceDataset/daily-usd-idr/usd_idr_daily_cleaned.csv"
df_usd_clean = pd.read_csv(usd_clean_path)
usd_clean_count = len(df_usd_clean)
usd_clean_start = df_usd_clean['Date'].min()
usd_clean_end = df_usd_clean['Date'].max()
print(f"USD/IDR cleaned: {usd_clean_count} rows, from {usd_clean_start} to {usd_clean_end}")