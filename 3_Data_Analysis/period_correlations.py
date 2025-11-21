import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Load data
df_full = pd.read_csv('data/daily_sentiment_gpt5.csv', parse_dates=['date'])
df_full['date'] = pd.to_datetime(df_full['date'])
df_ihsg = pd.read_csv('data/ihsg_daily.csv', parse_dates=['Date'])
df_ihsg.rename(columns={'Date': 'date'}, inplace=True)
df_ihsg['date'] = pd.to_datetime(df_ihsg['date'])
df_ihsg['ihsg_return'] = df_ihsg['Close'].pct_change() * 100
df_usd = pd.read_csv('data/usd_idr_daily.csv', parse_dates=['Date'])
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
correlations = {}
for period, df in [('Before', df_before), ('During', df_during), ('After', df_after)]:
    if not df.empty:
        corr_ihsg = df['net_sent'].corr(df['ihsg_return'])
        corr_usd = df['net_sent'].corr(df['usd_return'])
        correlations[period] = {'IHSG': corr_ihsg, 'USD/IDR': corr_usd}
        print(f'{period} Protest - IHSG: {corr_ihsg:.3f}, USD/IDR: {corr_usd:.3f}')
    else:
        print(f'{period} Protest - No data')

# Create bar plot
periods = list(correlations.keys())
ihsg_corrs = [correlations[p]['IHSG'] for p in periods]

# Set professional styling
sns.set_style('whitegrid')
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['font.size'] = 12
plt.rcParams['axes.labelsize'] = 14
plt.rcParams['axes.titlesize'] = 16
plt.rcParams['xtick.labelsize'] = 12
plt.rcParams['ytick.labelsize'] = 12
plt.rcParams['legend.fontsize'] = 12
plt.rcParams['figure.titlesize'] = 18

# Create plots directory
os.makedirs('plots', exist_ok=True)

fig, ax = plt.subplots(figsize=(10, 6))
bars = ax.bar(periods, ihsg_corrs, color='#1f77b4', alpha=0.7)
ax.set_ylabel('Correlation Coefficient')
ax.set_title('Twitter Sentiment vs IHSG Returns Correlation by Protest Period')
ax.set_ylim(-0.1, 0.5)
ax.grid(True, alpha=0.3)

# Add value labels on bars
for bar, corr in zip(bars, ihsg_corrs):
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2., height + 0.01,
            f'{corr:.3f}', ha='center', va='bottom', fontsize=12)

plt.tight_layout()
plt.savefig('plots/period_correlations_ihsg.png', dpi=300, bbox_inches='tight')
plt.show()

print("Period correlations bar plot saved as 'plots/period_correlations_ihsg.png'")