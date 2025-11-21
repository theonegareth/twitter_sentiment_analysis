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
colors = {'sentiment': '#1f77b4'}

# Create plots directory
os.makedirs('plots', exist_ok=True)

# Load data
df_sent = pd.read_csv('data/daily_sentiment_gpt5.csv', parse_dates=['date'])

# Preprocess
df_sent['date'] = pd.to_datetime(df_sent['date'])

# Plot net sentiment over time
fig, ax = plt.subplots(figsize=(16, 8))

ax.plot(df_sent['date'], df_sent['net_sent'], color=colors['sentiment'], linewidth=2, label='Net Sentiment (Twitter)')
ax.set_ylabel('Net Sentiment Score', color=colors['sentiment'], fontsize=14)
ax.tick_params(axis='y', labelcolor=colors['sentiment'])
ax.grid(True, alpha=0.3)

# Shade demo period grey
demo_start = pd.to_datetime('2025-08-25')
demo_end = pd.to_datetime('2025-09-07')
ax.axvspan(demo_start, demo_end, color='grey', alpha=0.1)

ax.set_title('Net Sentiment Over Time\n(Indonesian Protests Context, Aug-Sep 2025)', fontsize=16, pad=20)

ax.legend(loc='upper left', framealpha=0.9)

ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %d'))
ax.xaxis.set_major_locator(mdates.DayLocator(interval=5))
plt.setp(ax.xaxis.get_majorticklabels(), rotation=45, ha='right')

plt.tight_layout()
plt.savefig('plots/net_sentiment.png', dpi=300, bbox_inches='tight')

plt.show()

print("Net sentiment plot saved as 'plots/net_sentiment.png'")