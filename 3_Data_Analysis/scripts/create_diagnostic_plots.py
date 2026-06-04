import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from matplotlib.gridspec import GridSpec
import seaborn as sns
from scipy import stats
from scipy.stats import shapiro, kstest, normaltest, probplot
import os
import warnings
warnings.filterwarnings('ignore')

script_dir = os.path.dirname(os.path.abspath(__file__))
diagnostics_dir = os.path.join(script_dir, 'charts', 'diagnostics')
os.makedirs(diagnostics_dir, exist_ok=True)

plt.rcParams.update({
    'figure.facecolor': 'white',
    'axes.facecolor': '#fafafa',
    'axes.grid': True,
    'grid.alpha': 0.25,
    'font.family': 'sans-serif',
    'font.size': 10,
    'axes.titlesize': 12,
    'axes.labelsize': 11,
    'savefig.dpi': 200,
    'savefig.bbox': 'tight',
})

COLOR_IHSG = '#e74c3c'
COLOR_USD  = '#2980b9'
COLOR_SENT = '#e67e22'

def safe_save(fig, name):
    path = os.path.join(diagnostics_dir, name)
    fig.savefig(path, dpi=200, bbox_inches='tight', facecolor='white')
    print(f"  Saved: {path}")
    plt.close(fig)

# ============================================================
# LOAD DATA
# ============================================================
print("Loading data...")

ihsg = pd.read_csv(os.path.join(script_dir, 'daily_sentiment_IHSG.csv'), parse_dates=['date'])
usdidr = pd.read_csv(os.path.join(script_dir, 'daily_sentiment_USDIDR.csv'), parse_dates=['date'])

def classify_period(d):
    d = pd.Timestamp(d)
    if d < pd.Timestamp('2025-08-25'):
        return 'Before Demo'
    elif d <= pd.Timestamp('2025-09-08'):
        return 'Demo'
    else:
        return 'After Demo'

ihsg['period'] = ihsg['date'].apply(classify_period)
usdidr['period'] = usdidr['date'].apply(classify_period)

# Combine for pairwise
combined = ihsg[['date', 'net_sentiment_ratio', 'IHSG_return', 'period']].rename(
    columns={'net_sentiment_ratio': 'NSR_IHSG'}
)
combined['NSR_USDIDR'] = usdidr['net_sentiment_ratio'].values
combined['USDIDR_return'] = usdidr['USDIDR_return'].values

# ============================================================
# NORMALITY TESTS (Shapiro-Wilk, D'Agostino-Pearson, KS)
# ============================================================
print("\nRunning normality tests...")

norm_results = []
for name, series in [
    ('IHSG Net Sentiment (NSR)', combined['NSR_IHSG'].dropna()),
    ('USD/IDR Net Sentiment (NSR)', combined['NSR_USDIDR'].dropna()),
    ('IHSG Return (%)', combined['IHSG_return'].dropna()),
    ('USD/IDR Return (%)', combined['USDIDR_return'].dropna()),
]:
    s = series.values
    sh_stat, sh_p = shapiro(s)
    dap_stat, dap_p = normaltest(s)
    ks_stat, ks_p = kstest((s - s.mean()) / s.std(), 'norm')
    skew = stats.skew(s)
    kurt = stats.kurtosis(s)

    norm_results.append({
        'Variable': name,
        'n': len(s),
        'Mean': round(s.mean(), 4),
        'SD': round(s.std(), 4),
        'Skewness': round(skew, 4),
        'Kurtosis': round(kurt, 4),
        'Shapiro-Wilk W': round(sh_stat, 4),
        'Shapiro-Wilk p': round(sh_p, 6),
        "D'Agostino K2": round(dap_stat, 4),
        "D'Agostino p": round(dap_p, 6),
        'KS Statistic': round(ks_stat, 4),
        'KS p': round(ks_p, 6),
        'Normal (alpha=0.05)?': 'YES' if sh_p > 0.05 else 'NO',
    })

norm_df = pd.DataFrame(norm_results)
print("\nNormality Test Results:")
print(norm_df.to_string(index=False))

# ============================================================
# FIGURE D1: MASTER DIAGNOSTIC DASHBOARD — 3 vars, 4 diagnostic rows
# ============================================================
print("\nCreating Figure D1: Master diagnostic dashboard...")

fig = plt.figure(figsize=(20, 14))
gs = GridSpec(4, 4, figure=fig, hspace=0.35, wspace=0.3)

var_specs = [
    ('IHSG Net\nSentiment (NSR)', combined['NSR_IHSG'].dropna(), COLOR_SENT),
    ('USD/IDR Net\nSentiment (NSR)', combined['NSR_USDIDR'].dropna(), COLOR_SENT),
    ('IHSG Daily\nReturn (%)', combined['IHSG_return'].dropna(), COLOR_IHSG),
    ('USD/IDR Daily\nReturn (%)', combined['USDIDR_return'].dropna(), COLOR_USD),
]

for col_idx, (label, data, color) in enumerate(var_specs):
    vals = data.values
    n = len(vals)
    sh_stat, sh_p = shapiro(vals)

    # Row 0: Histogram + KDE + Normal overlay
    ax_hist = fig.add_subplot(gs[0, col_idx])
    ax_hist.hist(vals, bins='auto', density=True, alpha=0.6, color=color, edgecolor='white', linewidth=0.5)
    from scipy.stats import gaussian_kde
    kde = gaussian_kde(vals)
    x_kde = np.linspace(vals.min(), vals.max(), 200)
    ax_hist.plot(x_kde, kde(x_kde), color='#2c3e50', linewidth=1.8, label='KDE')
    x_norm = np.linspace(vals.min() - 0.5*vals.std(), vals.max() + 0.5*vals.std(), 200)
    ax_hist.plot(x_norm, stats.norm.pdf(x_norm, vals.mean(), vals.std()),
                 '--', color='#95a5a6', linewidth=1.2, label='Normal')
    ax_hist.set_title(f'{label}\nShapiro-Wilk W={sh_stat:.3f}, p={sh_p:.3f}', fontsize=9)
    ax_hist.legend(fontsize=7, loc='upper right')
    ax_hist.set_ylabel('Density', fontsize=8)

    # Row 1: Boxplot
    ax_box = fig.add_subplot(gs[1, col_idx])
    bp = ax_box.boxplot(vals, vert=True, patch_artist=True, widths=0.5,
                         boxprops=dict(facecolor=color, alpha=0.6, edgecolor='#2c3e50'),
                         whiskerprops=dict(color='#2c3e50'),
                         capprops=dict(color='#2c3e50'),
                         medianprops=dict(color='#2c3e50', linewidth=2),
                         flierprops=dict(marker='o', markerfacecolor=color, markersize=4, alpha=0.6))
    ax_box.set_xticklabels([label.replace('\n', ' ')])
    ax_box.set_ylabel('Value', fontsize=8)
    # Add individual points
    jitter = np.random.normal(0, 0.04, size=n)
    ax_box.scatter(np.ones(n) + jitter, vals, alpha=0.3, s=15, color='black', zorder=3)

    # Row 2: Q-Q Plot
    ax_qq = fig.add_subplot(gs[2, col_idx])
    (osm, osr), (slope, intercept, r_qq) = probplot(vals, dist="norm", plot=None)
    ax_qq.scatter(osm, osr, alpha=0.5, s=20, color=color, edgecolors='white', linewidth=0.3)
    ax_qq.plot(osm, slope * osm + intercept, '--', color='#2c3e50', linewidth=1.5)
    ax_qq.set_title(f'Q-Q Plot (R²={r_qq**2:.3f})', fontsize=9)
    ax_qq.set_xlabel('Theoretical Quantiles', fontsize=8)
    ax_qq.set_ylabel('Sample Quantiles', fontsize=8)

    # Row 3: Violin plot
    ax_violin = fig.add_subplot(gs[3, col_idx])
    parts = ax_violin.violinplot(vals, vert=True, showmedians=True, showextrema=True)
    for pc in parts['bodies']:
        pc.set_facecolor(color)
        pc.set_alpha(0.6)
    for partname in ('cbars', 'cmins', 'cmaxes', 'cmedians'):
        if partname in parts:
            parts[partname].set_color('#2c3e50')
            parts[partname].set_linewidth(1)
    ax_violin.set_xticklabels([label.replace('\n', ' ')])
    ax_violin.set_ylabel('Value', fontsize=8)
    jitter = np.random.normal(0, 0.04, size=n)
    ax_violin.scatter(np.ones(n) + jitter, vals, alpha=0.3, s=15, color='black', zorder=3)

    # Add skew/kurt annotation
    sk = stats.skew(vals)
    ku = stats.kurtosis(vals)
    ax_violin.annotate(f'Skew: {sk:+.3f}\nKurt: {ku:+.3f}',
                       xy=(0.02, 0.95), xycoords='axes fraction',
                       fontsize=7, va='top',
                       bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))

plt.suptitle('Diagnostic Dashboard: Net Sentiment & Market Returns', fontsize=16, fontweight='bold', y=0.995)
safe_save(fig, 'D01_master_diagnostic_dashboard.png')

# ============================================================
# FIGURE D2: HISTOGRAMS WITH FULL DETAIL — all 4 vars, large format
# ============================================================
print("Creating Figure D2: Detailed histograms...")

fig, axes = plt.subplots(2, 2, figsize=(14, 10))

hist_specs = [
    (axes[0, 0], 'IHSG Net Sentiment (NSR)', combined['NSR_IHSG'].dropna(), COLOR_SENT),
    (axes[0, 1], 'USD/IDR Net Sentiment (NSR)', combined['NSR_USDIDR'].dropna(), COLOR_SENT),
    (axes[1, 0], 'IHSG Daily Return (%)', combined['IHSG_return'].dropna(), COLOR_IHSG),
    (axes[1, 1], 'USD/IDR Daily Return (%)', combined['USDIDR_return'].dropna(), COLOR_USD),
]

for ax, title, data, color in hist_specs:
    vals = data.values
    n_val = len(vals)

    # Histogram
    n_bins = max(6, int(np.sqrt(n_val)))
    ax.hist(vals, bins=n_bins, density=True, alpha=0.6, color=color, edgecolor='white', linewidth=0.8)

    # KDE
    kde = gaussian_kde(vals)
    x_kde = np.linspace(vals.min(), vals.max(), 300)
    ax.plot(x_kde, kde(x_kde), color='#2c3e50', linewidth=2, label='KDE')

    # Normal overlay
    x_norm = np.linspace(vals.min() - 0.8*vals.std(), vals.max() + 0.8*vals.std(), 300)
    ax.plot(x_norm, stats.norm.pdf(x_norm, vals.mean(), vals.std()),
            '--', color='#95a5a6', linewidth=1.5, label='Normal fit')

    # Vertical lines for mean and median
    ax.axvline(vals.mean(), color='#e74c3c', linestyle='-', linewidth=1, alpha=0.8, label=f'Mean={vals.mean():.4f}')
    ax.axvline(np.median(vals), color='#3498db', linestyle='-', linewidth=1, alpha=0.8, label=f'Median={np.median(vals):.4f}')

    # Rug plot
    ax.plot(vals, np.zeros_like(vals) - 0.02*kde(x_kde).max(), '|', color='black', alpha=0.3, markersize=8)

    # Statistics box
    sk = stats.skew(vals)
    ku = stats.kurtosis(vals)
    sh_stat, sh_p = shapiro(vals)
    ks_stat, ks_p = kstest((vals - vals.mean()) / vals.std(), 'norm')

    stats_text = (
        f"n = {n_val}\n"
        f"Mean = {vals.mean():.4f}\n"
        f"SD = {vals.std():.4f}\n"
        f"Skewness = {sk:+.4f}\n"
        f"Kurtosis = {ku:+.4f}\n"
        f"Shapiro-Wilk p = {sh_p:.4f}\n"
        f"KS p = {ks_p:.4f}"
    )
    ax.text(0.97, 0.97, stats_text, transform=ax.transAxes, fontsize=8,
            va='top', ha='right',
            bbox=dict(boxstyle='round,pad=0.5', facecolor='white', alpha=0.9, edgecolor='#ccc'),
            family='monospace')

    ax.set_title(title, fontsize=12, fontweight='bold')
    ax.set_xlabel('Value', fontweight='bold')
    ax.set_ylabel('Density', fontweight='bold')
    ax.legend(fontsize=7, loc='upper left')

plt.suptitle('Distribution Analysis: Histograms with KDE and Normal Overlay', fontsize=14, fontweight='bold', y=1.01)
plt.tight_layout()
safe_save(fig, 'D02_histograms_detailed.png')

# ============================================================
# FIGURE D3: BOXPLOTS BY PERIOD — all 4 vars
# ============================================================
print("Creating Figure D3: Boxplots by period...")

fig, axes = plt.subplots(2, 2, figsize=(14, 10))
palette_period = ['#27ae60', '#e74c3c', '#3498db']
period_order = ['Before Demo', 'Demo', 'After Demo']

box_specs = [
    (axes[0, 0], ihsg, 'net_sentiment_ratio', 'IHSG Net Sentiment (NSR)', COLOR_SENT),
    (axes[0, 1], usdidr, 'net_sentiment_ratio', 'USD/IDR Net Sentiment (NSR)', COLOR_SENT),
    (axes[1, 0], ihsg, 'IHSG_return', 'IHSG Daily Return (%)', COLOR_IHSG),
    (axes[1, 1], usdidr, 'USDIDR_return', 'USD/IDR Daily Return (%)', COLOR_USD),
]

for ax, df, col, title, color in box_specs:
    data_list = [df[df['period'] == p][col].dropna().values for p in period_order]
    bp = ax.boxplot(data_list, patch_artist=True, widths=0.5,
                     boxprops=dict(facecolor=color, alpha=0.5, edgecolor='#2c3e50'),
                     whiskerprops=dict(color='#2c3e50'),
                     capprops=dict(color='#2c3e50'),
                     medianprops=dict(color='#2c3e50', linewidth=2),
                     flierprops=dict(marker='o', markerfacecolor=color, markersize=4, alpha=0.6))

    # Overlay stripplot
    for i, (vals, p) in enumerate(zip(data_list, period_order)):
        n = len(vals)
        if n > 0:
            jitter = np.random.normal(0, 0.06, size=n)
            ax.scatter(np.ones(n) * (i+1) + jitter, vals, alpha=0.35, s=20, color='black', zorder=3)

    ax.set_xticklabels(period_order, fontsize=9)
    ax.set_title(title, fontsize=11, fontweight='bold')
    ax.set_ylabel('Value', fontweight='bold')
    ax.axhline(0, color='gray', linestyle=':', linewidth=0.5)

    # Annotate n
    for i, vals in enumerate(data_list):
        if len(vals) > 0:
            ax.annotate(f'n={len(vals)}', xy=(i+1, ax.get_ylim()[0]),
                       ha='center', va='top', fontsize=8, color='#666')

    # ANOVA or Kruskal-Wallis between periods (if enough data)
    valid_groups = [g for g in data_list if len(g) >= 3]
    if len(valid_groups) >= 2:
        if all(len(g) >= 3 for g in valid_groups):
            try:
                from scipy.stats import kruskal
                h_stat, h_p = kruskal(*valid_groups)
                ax.set_title(f'{title}\nKruskal-Wallis H={h_stat:.2f}, p={h_p:.4f}', fontsize=10)
            except:
                pass

plt.suptitle('Distribution Comparison by Period', fontsize=14, fontweight='bold', y=1.01)
plt.tight_layout()
safe_save(fig, 'D03_boxplots_by_period.png')

# ============================================================
# FIGURE D4: VIOLIN PLOTS BY PERIOD — all 4 vars
# ============================================================
print("Creating Figure D4: Violin plots by period...")

fig, axes = plt.subplots(2, 2, figsize=(14, 10))

for ax, df, col, title, color in box_specs:
    data_list = [df[df['period'] == p][col].dropna().values for p in period_order]
    positions = [1, 2, 3]
    valid_pos = []
    valid_data = []
    for pos, vals in zip(positions, data_list):
        if len(vals) > 0:
            valid_pos.append(pos)
            valid_data.append(vals)

    if valid_data:
        parts = ax.violinplot(valid_data, positions=valid_pos, showmedians=True, showextrema=True)
        for pc in parts['bodies']:
            pc.set_facecolor(color)
            pc.set_alpha(0.5)
        for partname in ('cbars', 'cmins', 'cmaxes', 'cmedians'):
            if partname in parts:
                parts[partname].set_color('#2c3e50')

        for pos, vals in zip(valid_pos, valid_data):
            n = len(vals)
            jitter = np.random.normal(0, 0.04, size=n)
            ax.scatter(np.ones(n)*pos + jitter, vals, alpha=0.3, s=15, color='black', zorder=3)
            sk = stats.skew(vals)
            ax.annotate(f'n={n}\nskew={sk:+.2f}', xy=(pos-0.35, ax.get_ylim()[1]*0.9),
                       fontsize=7, ha='left',
                       bbox=dict(boxstyle='round,pad=0.2', facecolor='white', alpha=0.8))

    ax.set_xticks(positions)
    ax.set_xticklabels(period_order, fontsize=9)
    ax.set_title(title, fontsize=11, fontweight='bold')
    ax.set_ylabel('Value', fontweight='bold')
    ax.axhline(0, color='gray', linestyle=':', linewidth=0.5)

plt.suptitle('Violin Plots: Full Distribution Shape by Period', fontsize=14, fontweight='bold', y=1.01)
plt.tight_layout()
safe_save(fig, 'D04_violin_plots_by_period.png')

# ============================================================
# FIGURE D5: Q-Q PLOTS PER VARIABLE × PERIOD (12 panels)
# ============================================================
print("Creating Figure D5: Q-Q plots by period...")

fig, axes = plt.subplots(4, 3, figsize=(16, 16))

qq_specs = []
for var_name, df, col, color in [
    ('IHSG Net Sentiment', ihsg, 'net_sentiment_ratio', COLOR_SENT),
    ('USD/IDR Net Sentiment', usdidr, 'net_sentiment_ratio', COLOR_SENT),
    ('IHSG Return', ihsg, 'IHSG_return', COLOR_IHSG),
    ('USD/IDR Return', usdidr, 'USDIDR_return', COLOR_USD),
]:
    for p in period_order:
        vals = df[df['period'] == p][col].dropna().values
        qq_specs.append((var_name, p, vals, color))

for idx, (var_name, period, vals, color) in enumerate(qq_specs):
    row = idx // 3
    col_idx = idx % 3
    ax = axes[row, col_idx]

    if len(vals) < 3:
        ax.text(0.5, 0.5, f'n={len(vals)}\nInsufficient', ha='center', va='center',
                transform=ax.transAxes, fontsize=10, color='gray')
        ax.set_title(f'{var_name}\n{period}', fontsize=8)
        continue

    (osm, osr), (slope, intercept, r_qq) = probplot(vals, dist="norm", plot=None)
    ax.scatter(osm, osr, alpha=0.5, s=25, color=color, edgecolors='white', linewidth=0.3)
    ax.plot(osm, slope * osm + intercept, '--', color='#2c3e50', linewidth=1.5)

    # Shaded confidence band for Q-Q
    n_val = len(vals)
    se = np.sqrt(slope**2 / (2*n_val))
    ax.fill_between(osm, osr - 1.96*se, osr + 1.96*se, alpha=0.08, color=color)

    sh_stat, sh_p = shapiro(vals)
    ax.set_title(f'{var_name} — {period}\nn={n_val}, W={sh_stat:.3f}, p={sh_p:.3f}', fontsize=8)
    ax.set_xlabel('Theoretical', fontsize=7)
    ax.set_ylabel('Sample', fontsize=7)
    ax.tick_params(labelsize=7)

plt.suptitle('Q-Q Plots: Normality Assessment by Variable and Period', fontsize=14, fontweight='bold', y=0.998)
plt.tight_layout()
safe_save(fig, 'D05_qq_plots_by_period.png')

# ============================================================
# FIGURE D6: PAIRWISE SCATTERPLOT MATRIX (4×4 with KDE on diagonal)
# ============================================================
print("Creating Figure D6: Pairwise scatter matrix...")

pair_vars = combined[['NSR_IHSG', 'NSR_USDIDR', 'IHSG_return', 'USDIDR_return']].dropna()
pair_labels = [
    'IHSG Net\nSentiment',
    'USD/IDR Net\nSentiment',
    'IHSG\nReturn (%)',
    'USD/IDR\nReturn (%)',
]

colors_by_period = combined.loc[pair_vars.index, 'period'].map({
    'Before Demo': '#27ae60',
    'Demo': '#e74c3c',
    'After Demo': '#3498db',
}).values

g = sns.PairGrid(pair_vars, diag_sharey=False)
g.map_lower(sns.scatterplot, alpha=0.5, s=40, c=colors_by_period, edgecolor='white', linewidth=0.3)
g.map_upper(sns.kdeplot, cmap='OrRd', fill=True, alpha=0.3, levels=5, thresh=0.05)
g.map_diag(sns.histplot, kde=True, alpha=0.6, edgecolor='white', linewidth=0.5)

# Add Pearson r annotations in upper triangle
for i in range(4):
    for j in range(i+1, 4):
        ax = g.axes[i, j]
        x = pair_vars.iloc[:, j].values
        y = pair_vars.iloc[:, i].values
        mask = ~(np.isnan(x) | np.isnan(y))
        if mask.sum() >= 3:
            r, p = stats.pearsonr(x[mask], y[mask])
            ax.text(0.5, 0.92, f'r={r:+.3f}\np={p:.3f}', transform=ax.transAxes,
                   ha='center', va='top', fontsize=7, fontweight='bold',
                   bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.85, edgecolor='#ccc'))

# Set labels
for i in range(4):
    for j in range(4):
        if i == 3:
            g.axes[i, j].set_xlabel(pair_labels[j], fontsize=7, fontweight='bold')
        else:
            g.axes[i, j].set_xlabel('')
        if j == 0:
            g.axes[i, j].set_ylabel(pair_labels[i], fontsize=7, fontweight='bold')
        else:
            g.axes[i, j].set_ylabel('')

# Legend for periods
from matplotlib.patches import Patch
legend_elements = [
    Patch(facecolor='#27ae60', alpha=0.6, label='Before Demo'),
    Patch(facecolor='#e74c3c', alpha=0.6, label='Demo'),
    Patch(facecolor='#3498db', alpha=0.6, label='After Demo'),
]
g.figure.legend(handles=legend_elements, loc='lower right', fontsize=8, title='Period', title_fontsize=9)

g.figure.suptitle('Pairwise Diagnostic Matrix: Sentiment & Market Returns', fontsize=14, fontweight='bold', y=1.00)
g.figure.set_size_inches(14, 14)
safe_save(g.figure, 'D06_pairwise_scatter_matrix.png')

# ============================================================
# FIGURE D7: SENTIMENT × RETURN SCATTER BY PERIOD (colored)
# ============================================================
print("Creating Figure D7: Scatter by period...")

fig, axes = plt.subplots(1, 2, figsize=(14, 6))

scatter_pairs = [
    (axes[0], combined, 'NSR_IHSG', 'IHSG_return', 'IHSG', [0.0, 0.25, -2, 2]),
    (axes[1], combined, 'NSR_USDIDR', 'USDIDR_return', 'USD/IDR', [-0.25, 0.3, -1, 1]),
]

for ax, df, xcol, ycol, label, (xlim_low, xlim_high, ylim_low, ylim_high) in scatter_pairs:
    for period, color in zip(period_order, palette_period):
        sub = df[df['period'] == period].dropna(subset=[xcol, ycol])
        if len(sub) > 0:
            ax.scatter(sub[xcol], sub[ycol], c=color, label=f"{period} (n={len(sub)})",
                      s=60, edgecolors='white', linewidth=0.5, alpha=0.75)

    # Regression lines per period
    for period, color in zip(period_order, palette_period):
        sub = df[df['period'] == period].dropna(subset=[xcol, ycol])
        if len(sub) >= 3:
            z = np.polyfit(sub[xcol], sub[ycol], 1)
            p_line = np.poly1d(z)
            x_range = np.linspace(sub[xcol].min(), sub[xcol].max(), 50)
            ax.plot(x_range, p_line(x_range), '--', color=color, linewidth=1.5, alpha=0.7)

    # Overall regression
    all_data = df.dropna(subset=[xcol, ycol])
    if len(all_data) >= 3:
        r_all, p_all = stats.pearsonr(all_data[xcol], all_data[ycol])
        z = np.polyfit(all_data[xcol], all_data[ycol], 1)
        p_line = np.poly1d(z)
        x_range = np.linspace(all_data[xcol].min(), all_data[xcol].max(), 100)
        ax.plot(x_range, p_line(x_range), '-', color='black', linewidth=2, alpha=0.8,
                label=f'Overall r={r_all:+.3f}, p={p_all:.3f}')

    ax.set_xlabel('Net Sentiment Ratio', fontweight='bold')
    ax.set_ylabel(f'{label} Return (%)', fontweight='bold')
    ax.set_title(f'{label} Sentiment vs. Return', fontsize=12, fontweight='bold')
    ax.axhline(0, color='gray', linewidth=0.5, linestyle=':')
    ax.axvline(0, color='gray', linewidth=0.5, linestyle=':')
    ax.set_xlim(xlim_low, xlim_high)
    ax.set_ylim(ylim_low, ylim_high)
    ax.legend(fontsize=7, loc='best')

plt.suptitle('Net Sentiment vs. Market Returns: Stratified by Event Period', fontsize=13, fontweight='bold', y=1.02)
plt.tight_layout()
safe_save(fig, 'D07_scatter_by_period.png')

# ============================================================
# FIGURE D8: ECDF (Empirical Cumulative Distribution Function)
# ============================================================
print("Creating Figure D8: ECDF plots...")

fig, axes = plt.subplots(2, 2, figsize=(14, 10))

for ax, df, col, title, color in box_specs:
    vals = df[col].dropna().values
    sorted_vals = np.sort(vals)
    y = np.arange(1, len(sorted_vals) + 1) / len(sorted_vals)

    ax.step(sorted_vals, y, where='post', color=color, linewidth=2, label='ECDF')

    # Normal CDF overlay
    x_norm = np.linspace(vals.min() - 0.5*vals.std(), vals.max() + 0.5*vals.std(), 300)
    ax.plot(x_norm, stats.norm.cdf(x_norm, vals.mean(), vals.std()),
            '--', color='#2c3e50', linewidth=1.5, label='Normal CDF')

    # KS statistic
    ks_stat, ks_p = kstest((vals - vals.mean()) / vals.std(), 'norm')
    ax.set_title(f'{title}\nKS D={ks_stat:.4f}, p={ks_p:.4f}', fontsize=10, fontweight='bold')
    ax.set_xlabel('Value', fontweight='bold')
    ax.set_ylabel('Cumulative Probability', fontweight='bold')
    ax.legend(fontsize=8)
    ax.grid(True, alpha=0.3)

plt.suptitle('Empirical CDF vs. Theoretical Normal CDF', fontsize=14, fontweight='bold', y=1.01)
plt.tight_layout()
safe_save(fig, 'D08_ecdf_comparison.png')

# ============================================================
# FIGURE D9: RESIDUAL DIAGNOSTICS (from linear regression)
# ============================================================
print("Creating Figure D9: Residual diagnostics...")

fig = plt.figure(figsize=(16, 12))
gs = GridSpec(3, 2, figure=fig, hspace=0.35, wspace=0.3)

for idx, (xcol, ycol, label_x, label_y, color) in enumerate([
    ('NSR_IHSG', 'IHSG_return', 'IHSG Net Sentiment', 'IHSG Return', COLOR_IHSG),
    ('NSR_USDIDR', 'USDIDR_return', 'USD/IDR Net Sentiment', 'USD/IDR Return', COLOR_USD),
]):
    sub = combined.dropna(subset=[xcol, ycol])
    x = sub[xcol].values
    y = sub[ycol].values

    slope, intercept, r_val, p_val, std_err = stats.linregress(x, y)
    y_pred = slope * x + intercept
    residuals = y - y_pred

    # Row: Residuals vs Fitted
    ax_rf = fig.add_subplot(gs[0, idx])
    ax_rf.scatter(y_pred, residuals, alpha=0.5, s=40, color=color, edgecolors='white', linewidth=0.3)
    ax_rf.axhline(0, color='gray', linestyle='--', linewidth=1)
    # LOESS-like smooth
    sort_idx = np.argsort(y_pred)
    from scipy.ndimage import uniform_filter1d
    smooth = uniform_filter1d(residuals[sort_idx], size=max(3, len(y_pred)//3))
    ax_rf.plot(y_pred[sort_idx], smooth, color='black', linewidth=1.5, alpha=0.7)
    ax_rf.set_xlabel('Fitted Values', fontweight='bold')
    ax_rf.set_ylabel('Residuals', fontweight='bold')
    ax_rf.set_title(f'Residuals vs Fitted: {label_x} → {label_y}', fontsize=10)

    # Row: Q-Q of residuals
    ax_qq2 = fig.add_subplot(gs[1, idx])
    (osm, osr), (qq_slope, qq_intercept, r_qq) = probplot(residuals, dist="norm", plot=None)
    ax_qq2.scatter(osm, osr, alpha=0.5, s=25, color=color, edgecolors='white', linewidth=0.3)
    ax_qq2.plot(osm, qq_slope * osm + qq_intercept, '--', color='#2c3e50', linewidth=1.5)
    sh_res_stat, sh_res_p = shapiro(residuals)
    ax_qq2.set_title(f'Q-Q of Residuals (W={sh_res_stat:.3f}, p={sh_res_p:.4f})', fontsize=10)
    ax_qq2.set_xlabel('Theoretical Quantiles', fontsize=9)
    ax_qq2.set_ylabel('Sample Quantiles', fontsize=9)

    # Row: Scale-Location (sqrt |residuals| vs fitted)
    ax_sl = fig.add_subplot(gs[2, idx])
    sqrt_abs_res = np.sqrt(np.abs(residuals))
    ax_sl.scatter(y_pred, sqrt_abs_res, alpha=0.5, s=40, color=color, edgecolors='white', linewidth=0.3)
    smooth_sl = uniform_filter1d(sqrt_abs_res[sort_idx], size=max(3, len(y_pred)//3))
    ax_sl.plot(y_pred[sort_idx], smooth_sl, color='black', linewidth=1.5, alpha=0.7)
    ax_sl.set_xlabel('Fitted Values', fontweight='bold')
    ax_sl.set_ylabel('√|Residuals|', fontweight='bold')
    ax_sl.set_title(f'Scale-Location: {label_x} → {label_y}', fontsize=10)

plt.suptitle('Residual Diagnostics for Sentiment → Return Linear Models', fontsize=14, fontweight='bold', y=1.00)
safe_save(fig, 'D09_residual_diagnostics.png')

# ============================================================
# FIGURE D10: DENSITY RIDGELINE — sentiment by period
# ============================================================
print("Creating Figure D10: Density comparison by period...")

fig, axes = plt.subplots(2, 2, figsize=(14, 10))

for ax, df, col, title, color in box_specs:
    for period, pcolor, ls in zip(period_order, palette_period, ['-', '-', '-']):
        vals = df[df['period'] == period][col].dropna().values
        if len(vals) < 3:
            continue
        kde = gaussian_kde(vals)
        x_kde = np.linspace(vals.min(), vals.max(), 200)
        ax.plot(x_kde, kde(x_kde), color=pcolor, linewidth=1.8, label=f'{period} (n={len(vals)})')
        ax.fill_between(x_kde, kde(x_kde), alpha=0.08, color=pcolor)

        # Mean marker
        mean_val = vals.mean()
        ax.axvline(mean_val, color=pcolor, linestyle='--', linewidth=1, alpha=0.6)

    ax.set_title(title, fontsize=11, fontweight='bold')
    ax.set_xlabel('Value', fontweight='bold')
    ax.set_ylabel('Density', fontweight='bold')
    ax.legend(fontsize=8)

plt.suptitle('Kernel Density Estimates by Period', fontsize=14, fontweight='bold', y=1.01)
plt.tight_layout()
safe_save(fig, 'D10_density_by_period.png')

# ============================================================
# EXPORT NORMALITY TESTS TO CSV
# ============================================================
norm_path = os.path.join(script_dir, 'normality_test_results.csv')
norm_df.to_csv(norm_path, index=False)
print(f"\nNormality tests exported to: {norm_path}")

print(f"\nAll 10 diagnostic charts saved to: {diagnostics_dir}")
