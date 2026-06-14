import pandas as pd
import numpy as np
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
repo = os.path.join(os.path.dirname(script_dir), 'twitter_sentiment_analysis', '3_Data_Analysis', 'data')

start = '2025-08-01'
end = '2025-09-30'

# Load GPT-5
gpt5 = pd.read_csv(os.path.join(script_dir, 'gpt5_sentiment_raw.csv'), parse_dates=['date'])
gpt5_daily = gpt5[['date','net_sent']].copy()
gpt5_daily.rename(columns={'net_sent': 'net_sentiment_ratio'}, inplace=True)

# Load IHSG
ihsg = pd.read_csv(os.path.join(repo, 'ihsg_daily.csv'), parse_dates=['Date'])
ihsg.rename(columns={'Date':'date'}, inplace=True)
ihsg_win = ihsg[(ihsg['date']>=start)&(ihsg['date']<=end)][['date','Close']].sort_values('date').copy()
ihsg_win['IHSG_return'] = ihsg_win['Close'].pct_change() * 100
print(f"IHSG trading days: {len(ihsg_win)}, with returns: {ihsg_win['IHSG_return'].notna().sum()}")

# Load USD/IDR — dates have timezone (+01:00), extract date only
usdidr = pd.read_csv(os.path.join(repo, 'usd_idr_daily.csv'))
usdidr['date'] = pd.to_datetime(usdidr['Date'].str.split(' ').str[0])
usdidr_win = usdidr[(usdidr['date']>=start)&(usdidr['date']<=end)][['date','Close']].sort_values('date').copy()
usdidr_win['USDIDR_return'] = usdidr_win['Close'].pct_change() * 100
print(f"USD/IDR trading days: {len(usdidr_win)}, with returns: {usdidr_win['USDIDR_return'].notna().sum()}")

# Merge
m1 = gpt5_daily.merge(ihsg_win[['date','IHSG_return']], on='date', how='inner')
print(f"GPT5 + IHSG merge: {len(m1)} rows")
m2 = m1.merge(usdidr_win[['date','USDIDR_return']], on='date', how='inner')
print(f"+ USD/IDR merge: {len(m2)} rows")
merged = m2.dropna(subset=['IHSG_return','USDIDR_return']).sort_values('date').reset_index(drop=True)
print(f"After dropna: {len(merged)} rows")
print(f"Merged paired observations (with returns): {len(merged)}")

# Save
out = os.path.join(script_dir, 'gpt5_merged.csv')
merged.to_csv(out, index=False)
print(f"Saved: {out}")
print(merged.to_string(index=False))
