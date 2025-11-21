import pandas as pd

# Load data
df_full = pd.read_csv('data/daily_sentiment_gpt5.csv', parse_dates=['date'])
df_full['date'] = pd.to_datetime(df_full['date'])
df_ihsg = pd.read_csv('data/ihsg_daily.csv', parse_dates=['Date'])
df_ihsg.rename(columns={'Date': 'date'}, inplace=True)
df_ihsg['date'] = pd.to_datetime(df_ihsg['date'])
df_ihsg['ihsg_return'] = df_ihsg['Close'].pct_change() * 100
df_usd = pd.read_csv('data/usd_idr_daily.csv')
df_usd.rename(columns={'Date': 'date'}, inplace=True)
df_usd['date'] = pd.to_datetime(df_usd['date'], utc=True).dt.tz_localize(None)
df_usd['usd_return'] = df_usd['Close'].pct_change() * 100

# Left join to include all sentiment dates
df_merged = pd.merge(df_full, df_ihsg[['date', 'ihsg_return']], on='date', how='left')
df_full = pd.merge(df_merged, df_usd[['date', 'usd_return']], on='date', how='left')

# Forward fill market data
df_full['ihsg_return'] = df_full['ihsg_return'].fillna(method='ffill').fillna(0)
df_full['usd_return'] = df_full['usd_return'].fillna(method='ffill').fillna(0)

# Define periods
before_start = pd.to_datetime('2025-08-01')
before_end = pd.to_datetime('2025-08-24')
during_start = pd.to_datetime('2025-08-25')
during_end = pd.to_datetime('2025-09-07')
after_start = pd.to_datetime('2025-09-08')
after_end = pd.to_datetime('2025-09-29')

# Filter data
df_before = df_full[(df_full['date'] >= before_start) & (df_full['date'] <= before_end)]
df_during = df_full[(df_full['date'] >= during_start) & (df_full['date'] <= during_end)]
df_after = df_full[(df_full['date'] >= after_start) & (df_full['date'] <= after_end)]

# Compute correlations
for period, df in [('Before', df_before), ('During', df_during), ('After', df_after)]:
    if not df.empty:
        corr_ihsg = df['net_sent'].corr(df['ihsg_return'])
        corr_usd = df['net_sent'].corr(df['usd_return'])
        print(f'{period} Protest - IHSG: {corr_ihsg:.3f}, USD/IDR: {corr_usd:.3f}')
    else:
        print(f'{period} Protest - No data')