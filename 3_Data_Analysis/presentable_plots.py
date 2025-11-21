import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.dates as mdates
import os

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

# Consistent color scheme
colors = {'sentiment': '#1f77b4', 'ihsg': '#d62728', 'usd': '#2ca02c'}

# Create plots directory
os.makedirs('plots', exist_ok=True)

# Load data
df_sent = pd.read_csv('data/daily_sentiment_gpt5.csv', parse_dates=['date'])
df_sent_full = df_sent.copy()  # Keep full sentiment data
df_ihsg = pd.read_csv('data/ihsg_daily.csv', parse_dates=['Date'])
df_ihsg.rename(columns={'Date': 'date'}, inplace=True)
df_usd = pd.read_csv('data/usd_idr_daily.csv', parse_dates=['Date'])
df_usd.rename(columns={'Date': 'date'}, inplace=True)

# Log raw data samples
print("Raw IHSG data sample:")
print(df_ihsg[['date', 'Close']].head())
print("Raw USD/IDR data sample:")
print(df_usd[['date', 'Close']].head())
print("Daily sentiment data sample:")
print(df_sent.head())

# Preprocess
df_sent['date'] = pd.to_datetime(df_sent['date']).dt.strftime('%Y-%m-%d')
df_sent_full['date'] = pd.to_datetime(df_sent_full['date'])
df_ihsg['date'] = pd.to_datetime(df_ihsg['date']).dt.strftime('%Y-%m-%d')
df_usd['date'] = pd.to_datetime(df_usd['date'], utc=True).dt.strftime('%Y-%m-%d')

# Fill weekends in sentiment data with Friday's data
full_date_range = pd.date_range(start='2025-08-01', end='2025-09-29', freq='D')
df_sent_full = df_sent_full.set_index('date').reindex(full_date_range).fillna(method='ffill').reset_index()
df_sent_full.rename(columns={'index': 'date'}, inplace=True)

start = '2025-08-01'
end = '2025-09-29'
df_sent = df_sent[(df_sent['date'] >= start) & (df_sent['date'] <= end)]
df_ihsg = df_ihsg[(df_ihsg['date'] >= start) & (df_ihsg['date'] <= end)]
df_usd = df_usd[(df_usd['date'] >= start) & (df_usd['date'] <= end)]

# Compute returns
df_ihsg['ihsg_return'] = df_ihsg['Close'].pct_change() * 100
df_usd['usd_return'] = df_usd['Close'].pct_change() * 100

# Merge with left join to include all sentiment dates
df_merged = pd.merge(df_sent, df_ihsg[['date', 'ihsg_return', 'Close']], on='date', how='left')
df_merged.rename(columns={'Close': 'ihsg_close'}, inplace=True)
df_full = pd.merge(df_merged, df_usd[['date', 'usd_return', 'Close']], on='date', how='left')
df_full.rename(columns={'Close': 'usd_close'}, inplace=True)
df_full['date'] = pd.to_datetime(df_full['date'])

# Forward fill market data for weekends
df_full['ihsg_return_ff'] = df_full['ihsg_return'].fillna(method='ffill')
df_full['usd_return_ff'] = df_full['usd_return'].fillna(method='ffill')
df_full['ihsg_close_ff'] = df_full['ihsg_close'].fillna(method='ffill')
df_full['usd_close_ff'] = df_full['usd_close'].fillna(method='ffill')

# Add weekday column
df_full['weekday'] = df_full['date'].dt.weekday  # 0=Mon, 6=Sun
df_weekdays = df_full[df_full['weekday'] < 5]
df_weekends = df_full[df_full['weekday'] >= 5]

# Correlations
corr_matrix = df_full[['net_sent', 'ihsg_return', 'usd_return']].corr()
sent_ihsg_corr = corr_matrix.loc['net_sent', 'ihsg_return']
sent_usd_corr = corr_matrix.loc['net_sent', 'usd_return']

# Lead-lag
for lag in [1, 2, 3]:
    df_full[f'net_sent_lag{lag}'] = df_full['net_sent'].shift(lag)
    lag_corr_ihsg = df_full[[f'net_sent_lag{lag}', 'ihsg_return']].dropna().corr().iloc[0, 1]
    lag_corr_usd = df_full[[f'net_sent_lag{lag}', 'usd_return']].dropna().corr().iloc[0, 1]
    print(f'Lag {lag} days - Sentiment vs IHSG: {lag_corr_ihsg:.3f}, vs USD/IDR: {lag_corr_usd:.3f}')

# Rolling averages (after ffill to include weekends)
df_full['net_sent_rolling'] = df_full['net_sent'].rolling(window=7).mean()
df_full['ihsg_return_rolling'] = df_full['ihsg_return_ff'].rolling(window=7).mean()
df_full['usd_return_rolling'] = df_full['usd_return_ff'].rolling(window=7).mean()

# Plot 1: Sentiment vs IHSG
fig, ax1 = plt.subplots(figsize=(16, 8))

ax1.plot(df_full['date'], df_full['net_sent'], color=colors['sentiment'], linewidth=2, label='Net Sentiment (Twitter)')
ax1.set_ylabel('Net Sentiment Score', color=colors['sentiment'], fontsize=14)
ax1.tick_params(axis='y', labelcolor=colors['sentiment'])
ax1.grid(True, alpha=0.3)

ax2 = ax1.twinx()
# Plot dashed line for continuity (weekends/holidays)
ax2.plot(df_full['date'], df_full['ihsg_return_ff'], color=colors['ihsg'], linewidth=2, linestyle='--', alpha=0.7)
# Plot solid line for actual trading days
ax2.plot(df_full['date'], df_full['ihsg_return'], color=colors['ihsg'], linewidth=2, linestyle='-', label='IHSG Daily Return')
ax2.set_ylabel('IHSG Daily Return (%)', color=colors['ihsg'], fontsize=14)
ax2.tick_params(axis='y', labelcolor=colors['ihsg'])

# Add raw IHSG Close as third axis
ax3 = ax2.twinx()
# Plot dashed line for continuity
ax3.plot(df_full['date'], df_full['ihsg_close_ff'], color='gray', linewidth=1, linestyle='--', alpha=0.7)
# Plot solid line for actual trading days
ax3.plot(df_full['date'], df_full['ihsg_close'], color='gray', linewidth=1, linestyle='-', label='IHSG Raw Close')
ax3.set_ylabel('IHSG Close Price', color='gray', fontsize=14)
ax3.tick_params(axis='y', labelcolor='gray')
ax3.spines["right"].set_position(("axes", 1.15))  # Offset the third axis further

ax1.xaxis.set_major_formatter(mdates.DateFormatter('%b %d'))
ax1.xaxis.set_major_locator(mdates.DayLocator(interval=5))
plt.setp(ax1.xaxis.get_majorticklabels(), rotation=45, ha='right')

# Shade demo period grey
demo_start = pd.to_datetime('2025-08-25')
demo_end = pd.to_datetime('2025-09-07')
ax1.axvspan(demo_start, demo_end, color='grey', alpha=0.1)

plt.title('Twitter Sentiment vs IHSG Returns (with Raw Prices)\n(Indonesian Protests Context, Aug-Sep 2025)', fontsize=16, pad=20)
ax1.text(0.02, 0.94, f'Correlation: {sent_ihsg_corr:.3f}', transform=ax1.transAxes,
         verticalalignment='top', fontsize=12, bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
lines3, labels3 = ax3.get_legend_handles_labels()
ax1.legend(lines1 + lines2 + lines3, labels1 + labels2 + labels3, loc='upper right', framealpha=0.9)

plt.tight_layout(pad=3.0)
plt.savefig('plots/sentiment_vs_ihsg.png', dpi=300, bbox_inches='tight')

plt.show()

# Plot 2: Sentiment vs USD/IDR
fig, ax1 = plt.subplots(figsize=(16, 8))

ax1.plot(df_full['date'], df_full['net_sent'], color=colors['sentiment'], linewidth=2, label='Net Sentiment (Twitter)')
ax1.set_ylabel('Net Sentiment Score', color=colors['sentiment'], fontsize=14)
ax1.tick_params(axis='y', labelcolor=colors['sentiment'])
ax1.grid(True, alpha=0.3)

ax2 = ax1.twinx()
# Plot dashed line for continuity
ax2.plot(df_full['date'], df_full['usd_return_ff'], color=colors['usd'], linewidth=2, linestyle='--', alpha=0.7)
# Plot solid line for actual trading days
ax2.plot(df_full['date'], df_full['usd_return'], color=colors['usd'], linewidth=2, linestyle='-', label='USD/IDR Daily Return')
ax2.set_ylabel('USD/IDR Daily Return (%)', color=colors['usd'], fontsize=14)
ax2.tick_params(axis='y', labelcolor=colors['usd'])

# Add raw USD/IDR Close as third axis
ax3 = ax2.twinx()
# Plot dashed line for continuity
ax3.plot(df_full['date'], df_full['usd_close_ff'], color='gray', linewidth=1, linestyle='--', alpha=0.7)
# Plot solid line for actual trading days
ax3.plot(df_full['date'], df_full['usd_close'], color='gray', linewidth=1, linestyle='-', label='USD/IDR Raw Close')
ax3.set_ylabel('USD/IDR Close Price', color='gray', fontsize=14)
ax3.tick_params(axis='y', labelcolor='gray')
ax3.spines["right"].set_position(("axes", 1.1))  # Offset the third axis

ax1.xaxis.set_major_formatter(mdates.DateFormatter('%b %d'))
ax1.xaxis.set_major_locator(mdates.DayLocator(interval=5))
plt.setp(ax1.xaxis.get_majorticklabels(), rotation=45, ha='right')

# Shade demo period grey
demo_start = pd.to_datetime('2025-08-25')
demo_end = pd.to_datetime('2025-09-07')
ax1.axvspan(demo_start, demo_end, color='grey', alpha=0.1)

plt.title('Twitter Sentiment vs USD/IDR Returns (with Raw Prices)\n(Indonesian Protests Context, Aug-Sep 2025)', fontsize=16, pad=20)
ax1.text(0.02, 0.94, f'Correlation: {sent_usd_corr:.3f}', transform=ax1.transAxes,
         verticalalignment='top', fontsize=12, bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
lines3, labels3 = ax3.get_legend_handles_labels()
ax1.legend(lines1 + lines2 + lines3, labels1 + labels2 + labels3, loc='upper right', framealpha=0.9)

plt.tight_layout()
plt.savefig('plots/sentiment_vs_usd.png', dpi=300, bbox_inches='tight')

plt.show()

# Plot 3: Rolling averages IHSG
fig, ax1 = plt.subplots(figsize=(14, 7))
ax1.plot(df_full['date'], df_full['net_sent_rolling'], color=colors['sentiment'], linewidth=2, label='Net Sentiment (7-day avg)')
ax1.set_ylabel('Net Sentiment (Rolling)', color=colors['sentiment'], fontsize=14)
ax1.tick_params(axis='y', labelcolor=colors['sentiment'])
ax1.grid(True, alpha=0.3)

ax2 = ax1.twinx()
ax2.plot(df_full['date'], df_full['ihsg_return_rolling'], color=colors['ihsg'], linewidth=2, label='IHSG Return (7-day avg)')
ax2.set_ylabel('IHSG Return (%) (Rolling)', color=colors['ihsg'], fontsize=14)
ax2.tick_params(axis='y', labelcolor=colors['ihsg'])

ax1.xaxis.set_major_formatter(mdates.DateFormatter('%b %d'))
ax1.xaxis.set_major_locator(mdates.DayLocator(interval=5))
plt.setp(ax1.xaxis.get_majorticklabels(), rotation=45, ha='right')

plt.title('Smoothed Twitter Sentiment vs IHSG Returns\n(7-day Rolling Averages)', fontsize=16, pad=20)

lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left', framealpha=0.9)

plt.tight_layout()
plt.savefig('plots/rolling_sentiment_vs_ihsg.png', dpi=300, bbox_inches='tight')

plt.show()

# Plot 4: Combined subplot
fig, ((ax1, ax2), (ax3, ax4), (ax5, ax6)) = plt.subplots(3, 2, figsize=(20, 24))  # Increased figure size

# Top left: Sentiment vs IHSG
ax1.plot(df_full['date'], df_full['net_sent'], color=colors['sentiment'], linewidth=2)
ax1.set_ylabel('Net Sentiment', color=colors['sentiment'])
ax1.tick_params(axis='y', labelcolor=colors['sentiment'])
ax1.grid(True, alpha=0.3)
ax1_twin = ax1.twinx()
ax1_twin.plot(df_full['date'], df_full['ihsg_return_ff'], color=colors['ihsg'], linewidth=2, linestyle='--', alpha=0.7)
ax1_twin.plot(df_full['date'], df_full['ihsg_return'], color=colors['ihsg'], linewidth=2, linestyle='-')
ax1_twin.set_ylabel('IHSG Return (%)', color=colors['ihsg'])
ax1_twin.tick_params(axis='y', labelcolor=colors['ihsg'])
# Add raw IHSG Close
ax1_twin2 = ax1_twin.twinx()
ax1_twin2.plot(df_full['date'], df_full['ihsg_close_ff'], color='gray', linewidth=1, linestyle='--', alpha=0.7)
ax1_twin2.plot(df_full['date'], df_full['ihsg_close'], color='gray', linewidth=1, linestyle='-')
ax1_twin2.set_ylabel('IHSG Close', color='gray')
ax1_twin2.tick_params(axis='y', labelcolor='gray')
ax1_twin2.spines["right"].set_position(("axes", 1.15)) # Increased offset
demo_start = pd.to_datetime('2025-08-25')
demo_end = pd.to_datetime('2025-09-07')
ax1.axvspan(demo_start, demo_end, color='grey', alpha=0.1)
ax1.set_title(f'Sentiment vs IHSG (Corr: {sent_ihsg_corr:.3f})', pad=20)

# Top right: Sentiment vs USD
ax2.plot(df_full['date'], df_full['net_sent'], color=colors['sentiment'], linewidth=2)
ax2.set_ylabel('Net Sentiment', color=colors['sentiment'])
ax2.tick_params(axis='y', labelcolor=colors['sentiment'])
ax2.grid(True, alpha=0.3)
ax2_twin = ax2.twinx()
ax2_twin.plot(df_full['date'], df_full['usd_return_ff'], color=colors['usd'], linewidth=2, linestyle='--', alpha=0.7)
ax2_twin.plot(df_full['date'], df_full['usd_return'], color=colors['usd'], linewidth=2, linestyle='-')
ax2_twin.set_ylabel('USD/IDR Return (%)', color=colors['usd'])
ax2_twin.tick_params(axis='y', labelcolor=colors['usd'])
# Add raw USD/IDR Close
ax2_twin2 = ax2_twin.twinx()
ax2_twin2.plot(df_full['date'], df_full['usd_close_ff'], color='gray', linewidth=1, linestyle='--', alpha=0.7)
ax2_twin2.plot(df_full['date'], df_full['usd_close'], color='gray', linewidth=1, linestyle='-')
ax2_twin2.set_ylabel('USD/IDR Close', color='gray')
ax2_twin2.tick_params(axis='y', labelcolor='gray')
ax2_twin2.spines["right"].set_position(("axes", 1.15)) # Increased offset
ax2.axvspan(demo_start, demo_end, color='grey', alpha=0.1)
ax2.set_title(f'Sentiment vs USD/IDR (Corr: {sent_usd_corr:.3f})', pad=20)

# Bottom left: Rolling IHSG
ax3.plot(df_full['date'], df_full['net_sent_rolling'], color=colors['sentiment'], linewidth=2)
ax3.set_ylabel('Net Sentiment (Rolling)', color=colors['sentiment'])
ax3.tick_params(axis='y', labelcolor=colors['sentiment'])
ax3.grid(True, alpha=0.3)
ax3_twin = ax3.twinx()
ax3_twin.plot(df_full['date'], df_full['ihsg_return_rolling'], color=colors['ihsg'], linewidth=2)
ax3_twin.set_ylabel('IHSG Return (Rolling)', color=colors['ihsg'])
ax3_twin.tick_params(axis='y', labelcolor=colors['ihsg'])
ax3.axvspan(demo_start, demo_end, color='grey', alpha=0.1)
ax3.set_title('Rolling Averages: Sentiment vs IHSG', pad=20)

# Bottom right: Heatmap
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', ax=ax4, cbar_kws={'shrink': 0.8})
ax4.set_title('Correlation Heatmap', pad=20)

# Bottom row: Full sentiment timeline
ax5.plot(df_sent_full['date'], df_sent_full['net_sent'], color=colors['sentiment'], linewidth=2)
ax5.set_ylabel('Net Sentiment Score', color=colors['sentiment'])
ax5.grid(True, alpha=0.3)
ax5.set_title('All Net Sentiment Scores (Including Weekends)', pad=20)
ax5.axvspan(demo_start, demo_end, color='grey', alpha=0.1)
ax5.xaxis.set_major_formatter(mdates.DateFormatter('%b %d'))
ax5.xaxis.set_major_locator(mdates.DayLocator(interval=7))
plt.setp(ax5.xaxis.get_majorticklabels(), rotation=45, ha='right')

ax6.axis('off')  # Hide the last subplot

# Format dates for all
for ax in [ax1, ax2, ax3, ax5]:
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %d'))
    ax.xaxis.set_major_locator(mdates.DayLocator(interval=7))
    plt.setp(ax.xaxis.get_majorticklabels(), rotation=45, ha='right')

plt.suptitle('Twitter Sentiment Analysis vs Market Indicators\nIndonesian Protests Context (Aug-Sep 2025)', fontsize=20, y=0.98)
plt.tight_layout(rect=[0, 0, 1, 0.96], h_pad=4, w_pad=4) # Increased padding
plt.savefig('plots/combined_analysis.png', dpi=300, bbox_inches='tight')

plt.show()

print("All presentable plots generated and saved to 'plots/' directory.")
