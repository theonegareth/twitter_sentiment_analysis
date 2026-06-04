import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.patches as mpatches
from matplotlib.gridspec import GridSpec
import seaborn as sns
import yfinance as yf
from scipy import stats
from datetime import datetime, timedelta
import os
import warnings
warnings.filterwarnings('ignore')

script_dir = os.path.dirname(os.path.abspath(__file__))
charts_dir = os.path.join(script_dir, 'charts')
os.makedirs(charts_dir, exist_ok=True)

START_DATE = "2025-08-01"
END_DATE = "2025-09-30"

# ============================================================
# THEME SETUP
# ============================================================
plt.rcParams.update({
    'figure.facecolor': 'white',
    'axes.facecolor': '#f8f9fa',
    'axes.grid': True,
    'grid.alpha': 0.3,
    'font.family': 'sans-serif',
    'font.size': 11,
    'axes.titlesize': 14,
    'axes.labelsize': 12,
    'savefig.dpi': 200,
    'savefig.bbox': 'tight',
})

sns.set_palette("husl")

# ============================================================
# 1. LOAD DATA
# ============================================================
print("Loading data...")

# Sentiment data
ihsg_sent = pd.read_csv(os.path.join(script_dir, 'daily_sentiment_IHSG.csv'), parse_dates=['date'])
usdidr_sent = pd.read_csv(os.path.join(script_dir, 'daily_sentiment_USDIDR.csv'), parse_dates=['date'])

# Market data
ihsg_raw = yf.download("^JKSE", start=START_DATE, end="2025-10-01", progress=False, auto_adjust=True)
usdidr_raw = yf.download("USDIDR=X", start=START_DATE, end="2025-10-01", progress=False, auto_adjust=True)

if isinstance(ihsg_raw.columns, pd.MultiIndex):
    ihsg_raw.columns = ihsg_raw.columns.get_level_values(0)
if isinstance(usdidr_raw.columns, pd.MultiIndex):
    usdidr_raw.columns = usdidr_raw.columns.get_level_values(0)

def safe_savefig(fig, name):
    path = os.path.join(charts_dir, name)
    fig.savefig(path, dpi=200, bbox_inches='tight', facecolor='white')
    print(f"  Saved: {path}")
    plt.close(fig)

# ============================================================
# 2. KEY EVENT DATES
# ============================================================
events = [
    ("Aug 25: Protest Begins\nDPR demonstration starts", "2025-08-25"),
    ("Aug 28: Affan Kurniawan\nOjol driver killed", "2025-08-28"),
    ("Aug 29: Financial Panic\nIHSG plunges, USD/IDR weakens", "2025-08-29"),
    ("Aug 30: Politicians Targeted\nHomes of Sahroni, Uya Kuya", "2025-08-30"),
    ("Sep 1-2: Demands Consolidated\n17+8 People's Demands", "2025-09-01"),
    ("Sep 5: Maulid Nabi\nPublic Holiday", "2025-09-05"),
]

# ============================================================
# FIGURE 1: SCATTER PLOTS — Net Sentiment vs Market Returns
# ============================================================
print("\nCreating Figure 1: Scatter plots...")

fig, axes = plt.subplots(1, 2, figsize=(14, 6))

# IHSG scatter
ax1 = axes[0]
merged_ihsg = ihsg_sent.dropna(subset=['net_sentiment_ratio', 'IHSG_return'])
x1 = merged_ihsg['net_sentiment_ratio']
y1 = merged_ihsg['IHSG_return']
r1, p1 = stats.pearsonr(x1, y1)
ci1_l, ci1_u = np.tanh(np.arctanh(r1) - stats.norm.ppf(0.975)/np.sqrt(len(x1)-3)), np.tanh(np.arctanh(r1) + stats.norm.ppf(0.975)/np.sqrt(len(x1)-3))

# Scatter
sc1 = ax1.scatter(x1, y1, c=merged_ihsg['tweet_count'], cmap='OrRd', s=80, edgecolors='white', linewidth=0.5, alpha=0.85)
# Regression line
z = np.polyfit(x1, y1, 1)
p_line = np.poly1d(z)
x_line = np.linspace(x1.min()-0.02, x1.max()+0.02, 100)
ax1.plot(x_line, p_line(x_line), '--', color='#2c3e50', linewidth=2)
# CI band
x_span = np.linspace(x1.min()-0.02, x1.max()+0.02, 100)
n = len(x1)
x_mean = x1.mean()
se_line = np.sqrt(np.sum((y1 - p_line(x1))**2)/(n-2)) * np.sqrt(1/n + (x_span - x_mean)**2/np.sum((x1 - x_mean)**2))
ax1.fill_between(x_span, p_line(x_span) - 1.96*se_line, p_line(x_span) + 1.96*se_line, alpha=0.12, color='#2c3e50')
cbar = plt.colorbar(sc1, ax=ax1)
cbar.set_label('Tweet Count', fontsize=10)
ax1.set_xlabel('Net Sentiment Ratio', fontweight='bold')
ax1.set_ylabel('IHSG Daily Return (%)', fontweight='bold')
ax1.set_title(f'IHSG: r = {r1:+.3f}, p = {p1:.3f}\n95% CI [{ci1_l:+.3f}, {ci1_u:+.3f}], n = {n}', fontsize=11)
ax1.axhline(0, color='gray', linewidth=0.5, linestyle=':')
ax1.axvline(0, color='gray', linewidth=0.5, linestyle=':')

# USD/IDR scatter
ax2 = axes[1]
merged_usd = usdidr_sent.dropna(subset=['net_sentiment_ratio', 'USDIDR_return'])
x2 = merged_usd['net_sentiment_ratio']
y2 = merged_usd['USDIDR_return']
r2, p2 = stats.pearsonr(x2, y2)
ci2_l, ci2_u = np.tanh(np.arctanh(r2) - stats.norm.ppf(0.975)/np.sqrt(len(x2)-3)), np.tanh(np.arctanh(r2) + stats.norm.ppf(0.975)/np.sqrt(len(x2)-3))

sc2 = ax2.scatter(x2, y2, c=merged_usd['tweet_count'], cmap='Blues', s=80, edgecolors='white', linewidth=0.5, alpha=0.85)
z = np.polyfit(x2, y2, 1)
p_line = np.poly1d(z)
x_line = np.linspace(x2.min()-0.02, x2.max()+0.02, 100)
ax2.plot(x_line, p_line(x_line), '--', color='#2c3e50', linewidth=2)
x_mean2 = x2.mean()
se_line2 = np.sqrt(np.sum((y2 - p_line(x2))**2)/(n-2)) * np.sqrt(1/n + (x_line - x_mean2)**2/np.sum((x2 - x_mean2)**2))
ax2.fill_between(x_line, p_line(x_line) - 1.96*se_line2, p_line(x_line) + 1.96*se_line2, alpha=0.12, color='#2c3e50')
cbar2 = plt.colorbar(sc2, ax=ax2)
cbar2.set_label('Tweet Count', fontsize=10)
ax2.set_xlabel('Net Sentiment Ratio', fontweight='bold')
ax2.set_ylabel('USD/IDR Daily Return (%)', fontweight='bold')
ax2.set_title(f'USD/IDR: r = {r2:+.3f}, p = {p2:.3f}\n95% CI [{ci2_l:+.3f}, {ci2_u:+.3f}], n = {n}', fontsize=11)
ax2.axhline(0, color='gray', linewidth=0.5, linestyle=':')
ax2.axvline(0, color='gray', linewidth=0.5, linestyle=':')

plt.suptitle('Net Sentiment vs. Same-Day Market Returns (VADER)', fontsize=15, fontweight='bold', y=1.02)
plt.tight_layout()
safe_savefig(fig, '01_scatter_net_sentiment_vs_returns.png')

# ============================================================
# FIGURE 2: TIME SERIES — IHSG + Sentiment Timeline
# ============================================================
print("Creating Figure 2: IHSG time series with sentiment...")

fig = plt.figure(figsize=(16, 10))
gs = GridSpec(4, 1, figure=fig, height_ratios=[2, 1, 1, 1], hspace=0.15)

# Panel A: IHSG Price
ax_price = fig.add_subplot(gs[0])
ax_price.plot(ihsg_raw.index, ihsg_raw['Close'], color='#1a1a2e', linewidth=1.8, label='IHSG Close')

# Shade periods
for start_d, end_d, color, label in [
    ('2025-08-01', '2025-08-24', '#27ae60', 'Before Demo'),
    ('2025-08-25', '2025-09-08', '#e74c3c', 'Demo Period'),
    ('2025-09-09', '2025-09-30', '#3498db', 'After Demo'),
]:
    ax_price.axvspan(pd.Timestamp(start_d), pd.Timestamp(end_d), alpha=0.08, color=color, label=label)

# Annotate key events
for text, d in events:
    t = pd.Timestamp(d)
    if t in ihsg_raw.index:
        v = ihsg_raw.loc[t, 'Close']
        ax_price.annotate(text.split('\n')[0], xy=(t, v), fontsize=7,
                          xytext=(5, 15), textcoords='offset points',
                          arrowprops=dict(arrowstyle='->', color='#e74c3c', lw=1),
                          bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.85, edgecolor='#ccc'),
                          fontweight='bold', color='#e74c3c')

ax_price.set_ylabel('IHSG (Close)', fontweight='bold')
ax_price.set_title('IHSG Composite Index (^JKSE) — Aug 1 to Sep 30, 2025', fontsize=13, fontweight='bold')
ax_price.legend(loc='upper right', fontsize=8, ncol=4)
ax_price.xaxis.set_major_formatter(mdates.DateFormatter('%b %d'))
ax_price.xaxis.set_major_locator(mdates.WeekdayLocator(interval=1))

# Panel B: IHSG Daily Returns
ax_ret = fig.add_subplot(gs[1], sharex=ax_price)
colors_ret = ['#e74c3c' if r < 0 else '#27ae60' for r in ihsg_sent['IHSG_return'].fillna(0)]
ax_ret.bar(ihsg_sent['date'], ihsg_sent['IHSG_return'], color=colors_ret, width=0.7, alpha=0.7)
ax_ret.axhline(0, color='black', linewidth=0.5)
ax_ret.set_ylabel('Return (%)', fontweight='bold')

# Panel C: IHSG Net Sentiment
ax_sent = fig.add_subplot(gs[2], sharex=ax_price)
ax_sent.bar(ihsg_sent['date'], ihsg_sent['net_sentiment_ratio'], color='#e67e22', width=0.7, alpha=0.7)
ax_sent.set_ylabel('Net Sentiment', fontweight='bold')
ax_sent.set_title('Daily Net Sentiment (IHSG-Related Keywords)', fontsize=10, fontweight='bold')

# Panel D: Tweet Volume
ax_vol = fig.add_subplot(gs[3], sharex=ax_price)
ax_vol.fill_between(ihsg_sent['date'], ihsg_sent['tweet_count'], alpha=0.5, color='#9b59b6')
ax_vol.plot(ihsg_sent['date'], ihsg_sent['tweet_count'], color='#8e44ad', linewidth=0.5)
ax_vol.set_ylabel('Tweet Count', fontweight='bold')
ax_vol.set_xlabel('Date', fontweight='bold')
ax_vol.set_title('Daily Tweet Volume (IHSG-Related Keywords)', fontsize=10, fontweight='bold')

plt.tight_layout()
safe_savefig(fig, '02_ihsg_timeline_with_sentiment.png')

# ============================================================
# FIGURE 3: TIME SERIES — USD/IDR + Sentiment Timeline
# ============================================================
print("Creating Figure 3: USD/IDR time series with sentiment...")

fig = plt.figure(figsize=(16, 10))
gs = GridSpec(4, 1, figure=fig, height_ratios=[2, 1, 1, 1], hspace=0.15)

# Panel A: USD/IDR Price
ax_price2 = fig.add_subplot(gs[0])
ax_price2.plot(usdidr_raw.index, usdidr_raw['Close'], color='#c0392b', linewidth=1.8, label='USD/IDR Close')

for start_d, end_d, color, label in [
    ('2025-08-01', '2025-08-24', '#27ae60', 'Before Demo'),
    ('2025-08-25', '2025-09-08', '#e74c3c', 'Demo Period'),
    ('2025-09-09', '2025-09-30', '#3498db', 'After Demo'),
]:
    ax_price2.axvspan(pd.Timestamp(start_d), pd.Timestamp(end_d), alpha=0.08, color=color, label=label)

for text, d in events:
    t = pd.Timestamp(d)
    if t in usdidr_raw.index:
        v = usdidr_raw.loc[t, 'Close']
        ax_price2.annotate(text.split('\n')[0], xy=(t, v), fontsize=7,
                          xytext=(5, 15), textcoords='offset points',
                          arrowprops=dict(arrowstyle='->', color='#e74c3c', lw=1),
                          bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.85, edgecolor='#ccc'),
                          fontweight='bold', color='#e74c3c')

ax_price2.set_ylabel('USD/IDR (Close)', fontweight='bold')
ax_price2.set_title('USD/IDR Exchange Rate — Aug 1 to Sep 30, 2025', fontsize=13, fontweight='bold')
ax_price2.legend(loc='upper left', fontsize=8, ncol=4)
ax_price2.xaxis.set_major_formatter(mdates.DateFormatter('%b %d'))
ax_price2.xaxis.set_major_locator(mdates.WeekdayLocator(interval=1))

# Panel B: USD/IDR Returns
ax_ret2 = fig.add_subplot(gs[1], sharex=ax_price2)
colors_ret2 = ['#e74c3c' if r < 0 else '#27ae60' for r in usdidr_sent['USDIDR_return'].fillna(0)]
ax_ret2.bar(usdidr_sent['date'], usdidr_sent['USDIDR_return'], color=colors_ret2, width=0.7, alpha=0.7)
ax_ret2.axhline(0, color='black', linewidth=0.5)
ax_ret2.set_ylabel('Return (%)', fontweight='bold')

# Panel C: USD/IDR Net Sentiment
ax_sent2 = fig.add_subplot(gs[2], sharex=ax_price2)
ax_sent2.bar(usdidr_sent['date'], usdidr_sent['net_sentiment_ratio'], color='#2980b9', width=0.7, alpha=0.7)
ax_sent2.set_ylabel('Net Sentiment', fontweight='bold')
ax_sent2.set_title('Daily Net Sentiment (USD/IDR-Related Keywords)', fontsize=10, fontweight='bold')

# Panel D: USD/IDR Tweet Volume
ax_vol2 = fig.add_subplot(gs[3], sharex=ax_price2)
ax_vol2.fill_between(usdidr_sent['date'], usdidr_sent['tweet_count'], alpha=0.5, color='#16a085')
ax_vol2.plot(usdidr_sent['date'], usdidr_sent['tweet_count'], color='#1abc9c', linewidth=0.5)
ax_vol2.set_ylabel('Tweet Count', fontweight='bold')
ax_vol2.set_xlabel('Date', fontweight='bold')
ax_vol2.set_title('Daily Tweet Volume (USD/IDR-Related Keywords)', fontsize=10, fontweight='bold')

plt.tight_layout()
safe_savefig(fig, '03_usdidr_timeline_with_sentiment.png')

# ============================================================
# FIGURE 4: PERIOD COMPARISON BAR CHART
# ============================================================
print("Creating Figure 4: Period comparison...")

periods = {
    'Before Demo\n(Aug 1–24)': ('2025-08-01', '2025-08-24'),
    'Demo\n(Aug 25 – Sep 8)': ('2025-08-25', '2025-09-08'),
    'After Demo\n(Sep 9–30)': ('2025-09-09', '2025-09-30'),
}

period_data = []
for pname, (ps, pe) in periods.items():
    ps_d = pd.Timestamp(ps)
    pe_d = pd.Timestamp(pe)

    # IHSG
    si = ihsg_sent[(ihsg_sent['date'] >= ps_d) & (ihsg_sent['date'] <= pe_d)].dropna(subset=['net_sentiment_ratio', 'IHSG_return'])
    su = usdidr_sent[(usdidr_sent['date'] >= ps_d) & (usdidr_sent['date'] <= pe_d)].dropna(subset=['net_sentiment_ratio', 'USDIDR_return'])

    ri, pi = stats.pearsonr(si['net_sentiment_ratio'], si['IHSG_return']) if len(si) >= 3 else (np.nan, np.nan)
    ru, pu = stats.pearsonr(su['net_sentiment_ratio'], su['USDIDR_return']) if len(su) >= 3 else (np.nan, np.nan)

    period_data.append({
        'Period': pname.replace('\n', ' '),
        'period_label': pname,
        'IHSG r': ri, 'IHSG p': pi,
        'USD/IDR r': ru, 'USD/IDR p': pu,
        'IHSG n': len(si), 'USD/IDR n': len(su),
    })

fig, ax = plt.subplots(figsize=(10, 6))
x = np.arange(len(period_data))
width = 0.35

bars1 = ax.bar(x - width/2, [d['IHSG r'] for d in period_data], width, label='IHSG', color='#e74c3c', alpha=0.85)
bars2 = ax.bar(x + width/2, [d['USD/IDR r'] for d in period_data], width, label='USD/IDR', color='#3498db', alpha=0.85)

# Add value labels
for bar in bars1:
    h = bar.get_height()
    if not np.isnan(h):
        ax.text(bar.get_x() + bar.get_width()/2., h + 0.02 if h >= 0 else h - 0.08,
                f'{h:+.3f}', ha='center', va='bottom' if h >= 0 else 'top', fontsize=9, fontweight='bold')

for bar in bars2:
    h = bar.get_height()
    if not np.isnan(h):
        ax.text(bar.get_x() + bar.get_width()/2., h + 0.02 if h >= 0 else h - 0.08,
                f'{h:+.3f}', ha='center', va='bottom' if h >= 0 else 'top', fontsize=9, fontweight='bold')

# Add n annotations
for i, d in enumerate(period_data):
    ax.text(i - width/2, -0.55, f'n={d["IHSG n"]}', ha='center', fontsize=8, color='#666')
    ax.text(i + width/2, -0.55, f'n={d["USD/IDR n"]}', ha='center', fontsize=8, color='#666')

ax.set_xticks(x)
ax.set_xticklabels([d['period_label'] for d in period_data], fontsize=10)
ax.set_ylabel('Pearson r', fontweight='bold')
ax.set_title('Net Sentiment vs. Market Returns: Correlation by Period', fontsize=14, fontweight='bold')
ax.axhline(0, color='black', linewidth=0.5)
ax.legend(fontsize=10)
ax.set_ylim(-0.8, 1.0)

# Add significance asterisks
for i, d in enumerate(period_data):
    for j, (r, p) in enumerate([(d['IHSG r'], d['IHSG p']), (d['USD/IDR r'], d['USD/IDR p'])]):
        if not np.isnan(p):
            sig = '***' if p < 0.001 else ('**' if p < 0.01 else ('*' if p < 0.05 else ''))
            if sig:
                xpos = i - width/2 + j*width
                ax.text(xpos, 0.92, sig, ha='center', fontsize=12, fontweight='bold', color='#e74c3c')

plt.tight_layout()
safe_savefig(fig, '04_period_correlation_comparison.png')

# ============================================================
# FIGURE 5: CORRELATION HEATMAP (All sentiment metrics)
# ============================================================
print("Creating Figure 5: Correlation heatmap...")

metrics_ihsg = ['net_sentiment_ratio', 'mean_compound', 'net_sentiment_compound', 'IHSG_return']
metrics_usd = ['net_sentiment_ratio', 'mean_compound', 'net_sentiment_compound', 'USDIDR_return']

fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# IHSG heatmap
corr_ihsg = ihsg_sent[metrics_ihsg].rename(columns={
    'net_sentiment_ratio': 'Net Sentiment\nRatio',
    'mean_compound': 'Mean\nCompound',
    'net_sentiment_compound': 'Net Sentiment\nCompound',
    'IHSG_return': 'IHSG\nReturn',
}).corr()

mask = np.triu(np.ones_like(corr_ihsg, dtype=bool), k=1)
sns.heatmap(corr_ihsg, annot=True, fmt='+.3f', cmap='RdBu_r', center=0,
            mask=mask, square=True, linewidths=0.5, ax=axes[0],
            vmin=-1, vmax=1, cbar_kws={'shrink': 0.8})
axes[0].set_title('IHSG Sentiment Metrics', fontsize=12, fontweight='bold', pad=15)

# USD/IDR heatmap
corr_usd = usdidr_sent[metrics_usd].rename(columns={
    'net_sentiment_ratio': 'Net Sentiment\nRatio',
    'mean_compound': 'Mean\nCompound',
    'net_sentiment_compound': 'Net Sentiment\nCompound',
    'USDIDR_return': 'USD/IDR\nReturn',
}).corr()

sns.heatmap(corr_usd, annot=True, fmt='+.3f', cmap='RdBu_r', center=0,
            mask=mask, square=True, linewidths=0.5, ax=axes[1],
            vmin=-1, vmax=1, cbar_kws={'shrink': 0.8})
axes[1].set_title('USD/IDR Sentiment Metrics', fontsize=12, fontweight='bold', pad=15)

plt.suptitle('Correlation Matrix: Sentiment Metrics vs. Market Returns', fontsize=14, fontweight='bold', y=1.02)
plt.tight_layout()
safe_savefig(fig, '05_correlation_heatmap.png')

# ============================================================
# FIGURE 6: EVENT TIMELINE — Annotated IHSG Chart
# ============================================================
print("Creating Figure 6: Event timeline...")

fig, ax = plt.subplots(figsize=(16, 7))

ax.plot(ihsg_raw.index, ihsg_raw['Close'], color='#2c3e50', linewidth=2.2, zorder=2)

# Shade periods
ax.axvspan(pd.Timestamp('2025-08-01'), pd.Timestamp('2025-08-24'), alpha=0.05, color='#27ae60')
ax.axvspan(pd.Timestamp('2025-08-25'), pd.Timestamp('2025-09-08'), alpha=0.12, color='#e74c3c')
ax.axvspan(pd.Timestamp('2025-09-09'), pd.Timestamp('2025-09-30'), alpha=0.05, color='#3498db')

# Vertical event lines with detailed labels
event_details = {
    '2025-08-25': ('Aug 25', "Protest Begins\nat DPR Building"),
    '2025-08-28': ('Aug 28', "Affan Kurniawan\nkilled by police vehicle"),
    '2025-08-29': ('Aug 29', "IHSG Plunges\nForeign outflow"),
    '2025-08-30': ('Aug 30', "Politicians' homes\ntargeted by protesters"),
    '2025-09-01': ('Sep 1–2', "17+8 Demands\nconsolidated"),
}

y_min, y_max = ihsg_raw['Close'].min(), ihsg_raw['Close'].max()
y_range = y_max - y_min
positions = [0.92, 0.75, 0.55, 0.40, 0.25]  # staggered

for i, (date_str, (short_label, detail)) in enumerate(event_details.items()):
    dt = pd.Timestamp(date_str)
    if dt in ihsg_raw.index:
        val = ihsg_raw.loc[dt, 'Close']
        ypos = y_min + y_range * positions[i]
        ax.axvline(dt, color='#e74c3c', linewidth=1, linestyle='--', alpha=0.5)
        ax.annotate(f'{short_label}: {detail}', xy=(dt, val),
                   xytext=(dt + pd.Timedelta(days=1), ypos),
                   fontsize=8, fontweight='bold',
                   bbox=dict(boxstyle='round,pad=0.4', facecolor='white', alpha=0.9, edgecolor='#e74c3c', linewidth=0.8),
                   arrowprops=dict(arrowstyle='->', color='#e74c3c', lw=1.2, connectionstyle='arc3,rad=0.1'))

ax.set_ylabel('IHSG Index', fontweight='bold')
ax.set_title('Event Study Timeline: IHSG During the August–September 2025 DPR Protests', fontsize=14, fontweight='bold')
ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %d'))
ax.xaxis.set_major_locator(mdates.DayLocator(interval=3))
ax.tick_params(axis='x', rotation=45)

# Legend
legend_elements = [
    mpatches.Patch(facecolor='#27ae60', alpha=0.15, label='Before Demo'),
    mpatches.Patch(facecolor='#e74c3c', alpha=0.2, label='Demo Period'),
    mpatches.Patch(facecolor='#3498db', alpha=0.15, label='After Demo'),
]
ax.legend(handles=legend_elements, loc='lower left', fontsize=9)

plt.tight_layout()
safe_savefig(fig, '06_event_timeline.png')

# ============================================================
# FIGURE 7: DUAL-AXIS IHSG + USD/IDR comparison
# ============================================================
print("Creating Figure 7: Dual market comparison...")

fig, ax1 = plt.subplots(figsize=(16, 6))

# IHSG on left axis
ax1.plot(ihsg_raw.index, ihsg_raw['Close'], color='#2c3e50', linewidth=2, label='IHSG')
ax1.set_ylabel('IHSG Index', fontweight='bold', color='#2c3e50')
ax1.tick_params(axis='y', labelcolor='#2c3e50')

# USD/IDR on right axis
ax2 = ax1.twinx()
ax2.plot(usdidr_raw.index, usdidr_raw['Close'], color='#e74c3c', linewidth=2, label='USD/IDR')
ax2.set_ylabel('USD/IDR Rate', fontweight='bold', color='#e74c3c')
ax2.tick_params(axis='y', labelcolor='#e74c3c')

# Period shading
ax1.axvspan(pd.Timestamp('2025-08-01'), pd.Timestamp('2025-08-24'), alpha=0.06, color='#27ae60')
ax1.axvspan(pd.Timestamp('2025-08-25'), pd.Timestamp('2025-09-08'), alpha=0.12, color='#e74c3c')
ax1.axvspan(pd.Timestamp('2025-09-09'), pd.Timestamp('2025-09-30'), alpha=0.06, color='#3498db')

# Key event
ax1.axvline(pd.Timestamp('2025-08-29'), color='#e74c3c', linewidth=1.2, linestyle='--', alpha=0.7)
ax1.annotate('Aug 29: IHSG Plunge\n& Rupiah Weakness', xy=(pd.Timestamp('2025-08-29'), ihsg_raw.loc['2025-08-29', 'Close']),
            xytext=(pd.Timestamp('2025-08-31'), ihsg_raw['Close'].max() * 0.97),
            fontsize=9, fontweight='bold', color='#e74c3c',
            bbox=dict(boxstyle='round', facecolor='white', alpha=0.9, edgecolor='#e74c3c'),
            arrowprops=dict(arrowstyle='->', color='#e74c3c'))

ax1.set_title('IHSG and USD/IDR: Divergent Paths During Political Crisis', fontsize=14, fontweight='bold')
ax1.xaxis.set_major_formatter(mdates.DateFormatter('%b %d'))
ax1.xaxis.set_major_locator(mdates.DayLocator(interval=3))
ax1.tick_params(axis='x', rotation=45)

lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, loc='lower left', fontsize=9)

plt.tight_layout()
safe_savefig(fig, '07_dual_market_comparison.png')

# ============================================================
# FIGURE 8: TWEET VOLUME DISTRIBUTION (Boxplot by period)
# ============================================================
print("Creating Figure 8: Tweet volume by period...")

fig, axes = plt.subplots(1, 2, figsize=(12, 5))

def classify_period(d):
    d = pd.Timestamp(d)
    if d < pd.Timestamp('2025-08-25'):
        return 'Before Demo'
    elif d <= pd.Timestamp('2025-09-08'):
        return 'Demo'
    else:
        return 'After Demo'

ihsg_sent['period'] = ihsg_sent['date'].apply(classify_period)
usdidr_sent['period'] = usdidr_sent['date'].apply(classify_period)

palette_i = ['#27ae60', '#e74c3c', '#3498db']
sns.boxplot(data=ihsg_sent, x='period', y='tweet_count', palette=palette_i, order=['Before Demo', 'Demo', 'After Demo'], ax=axes[0])
sns.stripplot(data=ihsg_sent, x='period', y='tweet_count', color='black', alpha=0.3, size=3, order=['Before Demo', 'Demo', 'After Demo'], ax=axes[0])
axes[0].set_ylabel('Tweet Count per Day', fontweight='bold')
axes[0].set_xlabel('')
axes[0].set_title('IHSG-Related Keywords', fontsize=12, fontweight='bold')

sns.boxplot(data=usdidr_sent, x='period', y='tweet_count', palette=palette_i, order=['Before Demo', 'Demo', 'After Demo'], ax=axes[1])
sns.stripplot(data=usdidr_sent, x='period', y='tweet_count', color='black', alpha=0.3, size=3, order=['Before Demo', 'Demo', 'After Demo'], ax=axes[1])
axes[1].set_ylabel('Tweet Count per Day', fontweight='bold')
axes[1].set_xlabel('')
axes[1].set_title('USD/IDR-Related Keywords', fontsize=12, fontweight='bold')

plt.suptitle('Daily Tweet Volume Distribution by Period', fontsize=14, fontweight='bold', y=1.02)
plt.tight_layout()
safe_savefig(fig, '08_tweet_volume_by_period.png')

# ============================================================
# FIGURE 9: NET SENTIMENT BOXPLOT BY PERIOD
# ============================================================
print("Creating Figure 9: Sentiment distribution by period...")

fig, axes = plt.subplots(1, 2, figsize=(12, 5))

sns.boxplot(data=ihsg_sent, x='period', y='net_sentiment_ratio', palette=palette_i, order=['Before Demo', 'Demo', 'After Demo'], ax=axes[0])
sns.stripplot(data=ihsg_sent, x='period', y='net_sentiment_ratio', color='black', alpha=0.3, size=3, order=['Before Demo', 'Demo', 'After Demo'], ax=axes[0])
axes[0].set_ylabel('Net Sentiment Ratio', fontweight='bold')
axes[0].set_xlabel('')
axes[0].axhline(0, color='gray', linestyle=':', linewidth=0.8)
axes[0].set_title('IHSG Sentiment', fontsize=12, fontweight='bold')

sns.boxplot(data=usdidr_sent, x='period', y='net_sentiment_ratio', palette=palette_i, order=['Before Demo', 'Demo', 'After Demo'], ax=axes[1])
sns.stripplot(data=usdidr_sent, x='period', y='net_sentiment_ratio', color='black', alpha=0.3, size=3, order=['Before Demo', 'Demo', 'After Demo'], ax=axes[1])
axes[1].set_ylabel('Net Sentiment Ratio', fontweight='bold')
axes[1].set_xlabel('')
axes[1].axhline(0, color='gray', linestyle=':', linewidth=0.8)
axes[1].set_title('USD/IDR Sentiment', fontsize=12, fontweight='bold')

plt.suptitle('Net Sentiment Distribution by Period (VADER)', fontsize=14, fontweight='bold', y=1.02)
plt.tight_layout()
safe_savefig(fig, '09_sentiment_distribution_by_period.png')

print("\nAll 9 charts generated successfully.")
print(f"Output directory: {charts_dir}")
