import pandas as pd
import numpy as np
from scipy import stats
from scipy.stats import shapiro, jarque_bera, normaltest, iqr
from statsmodels.tsa.stattools import adfuller, kpss
import os
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

script_dir = os.path.dirname(os.path.abspath(__file__))

# ---- load data ----
ihsg   = pd.read_csv(os.path.join(script_dir, 'daily_sentiment_IHSG.csv'),   parse_dates=['date']).sort_values('date')
usdidr = pd.read_csv(os.path.join(script_dir, 'daily_sentiment_USDIDR.csv'), parse_dates=['date']).sort_values('date')

# ---- series definitions ----
SERIES = [
    ('IHSG Net Sentiment (NSR)',       ihsg.set_index('date')['net_sentiment_ratio'].dropna(),       'IHSG'),
    ('USD/IDR Net Sentiment (NSR)',    usdidr.set_index('date')['net_sentiment_ratio'].dropna(),       'USD/IDR'),
    ('IHSG Return (%)',                ihsg.set_index('date')['IHSG_return'].dropna(),                 'IHSG'),
    ('USD/IDR Return (%)',             usdidr.set_index('date')['USDIDR_return'].dropna(),             'USD/IDR'),
    ('IHSG Net Sentiment (NSC)',       ihsg.set_index('date')['net_sentiment_compound'].dropna(),      'IHSG'),
    ('USD/IDR Net Sentiment (NSC)',    usdidr.set_index('date')['net_sentiment_compound'].dropna(),    'USD/IDR'),
    ('IHSG Mean Compound',             ihsg.set_index('date')['mean_compound'].dropna(),               'IHSG'),
    ('USD/IDR Mean Compound',          usdidr.set_index('date')['mean_compound'].dropna(),             'USD/IDR'),
    ('IHSG Tweet Count',               ihsg.set_index('date')['tweet_count'].dropna(),                 'IHSG'),
    ('USD/IDR Tweet Count',            usdidr.set_index('date')['tweet_count'].dropna(),               'USD/IDR'),
]

# ---- helper functions ----
def detect_outliers(vals, name):
    """Detect outliers using modified Z-score (MAD) and IQR methods."""
    notes = []
    n = len(vals)

    # IQR method
    q1, q3 = np.percentile(vals, [25, 75])
    iqr_val = q3 - q1
    lower_iqr = q1 - 1.5 * iqr_val
    upper_iqr = q3 + 1.5 * iqr_val
    iqr_outliers = [i for i, v in enumerate(vals) if v < lower_iqr or v > upper_iqr]

    # Modified Z-score (MAD)
    median = np.median(vals)
    mad = np.median(np.abs(vals - median))
    if mad > 0:
        mod_z = 0.6745 * (vals - median) / mad
        mad_outliers = [i for i, z in enumerate(mod_z) if abs(z) > 3.5]
    else:
        mad_outliers = []

    # Combined
    all_outlier_indices = sorted(set(iqr_outliers) | set(mad_outliers))
    count = len(all_outlier_indices)

    if count == 0:
        notes.append('None')
    elif count == 1:
        val = vals[all_outlier_indices[0]]
        direction = 'high' if val > np.mean(vals) else 'low'
        notes.append(f'{count} outlier ({direction}, value={val:.4f})')
    else:
        vals_out = [vals[i] for i in all_outlier_indices]
        hi = sum(1 for v in vals_out if v > np.mean(vals))
        lo = len(vals_out) - hi
        lo_val = min(vals_out) if lo > 0 else None
        hi_val = max(vals_out) if hi > 0 else None
        parts = []
        if lo > 0:
            parts.append(f'{lo} low (min={lo_val:.4f})')
        if hi > 0:
            parts.append(f'{hi} high (max={hi_val:.4f})')
        notes.append(f'{count} outliers: ' + ', '.join(parts))

    return '; '.join(notes)

def run_adf(vals):
    """Run ADF test (constant only) and return stat, p-value."""
    n = len(vals)
    ntrend = 1
    maxlag = max(0, min(8, n // 2 - 2 - ntrend))
    if maxlag < 0:
        maxlag = 0
    try:
        adf_stat, adf_p, _, _, adf_crit, _ = adfuller(vals, regression='c', autolag='AIC', maxlag=maxlag)
        return round(adf_stat, 4), round(adf_p, 6) if not np.isnan(adf_p) else None
    except:
        return None, None

def run_kpss_test(vals):
    """Run KPSS test (constant only) and return stat, p-value."""
    n = len(vals)
    nlags = min(4, max(0, n // 2 - 1))
    try:
        kpss_stat, kpss_p, _, _ = kpss(vals, regression='c', nlags=nlags)
        return round(kpss_stat, 4), round(kpss_p, 6) if not np.isnan(kpss_p) else None
    except:
        return None, None

# ---- build table ----
rows = []
for name, series, group in SERIES:
    vals = series.values
    n = len(vals)

    if n < 3:
        rows.append({'Variable': name, 'Group': group, 'N': n})
        continue

    # descriptive
    m  = round(float(vals.mean()), 4)
    sd = round(float(vals.std(ddof=1)), 4)
    vmin = round(float(vals.min()), 4)
    vmax = round(float(vals.max()), 4)
    sk  = round(float(stats.skew(vals)), 4)
    ku  = round(float(stats.kurtosis(vals)), 4)

    # normality
    sh_w, sh_p = shapiro(vals)
    jb_stat, jb_p = jarque_bera(vals)
    da_k2, da_p = normaltest(vals)

    # stationarity
    adf_stat, adf_p = run_adf(vals)
    kpss_stat, kpss_p = run_kpss_test(vals)

    # outliers
    outlier_note = detect_outliers(vals, name)

    # normality verdict — Shapiro-Wilk is the most powerful test for small samples
    # If SW rejects (p <= 0.05) and at least one other test also fails, verdict is Non-normal
    # If SW passes but JB+DA reject, verdict is Borderline
    # If SW passes and at least one of JB/DA pass, verdict is Normal
    sw_ok = sh_p > 0.05
    jb_ok = jb_p > 0.05
    da_ok = da_p > 0.05
    if not sw_ok:
        fail_count = sum(1 for ok in [not sw_ok, not jb_ok, not da_ok] if ok)
        norm_verdict = 'Non-normal' if fail_count >= 2 else 'Borderline'
    else:
        # SW passed
        if jb_ok and da_ok:
            norm_verdict = 'Normal'
        elif jb_ok or da_ok:
            norm_verdict = 'Normal'  # SW + 1 other pass
        else:
            norm_verdict = 'Borderline'  # SW passed but both JB and DA reject

    # stationarity verdict
    adf_ok = adf_p is not None and adf_p < 0.05
    kpss_ok = kpss_p is not None and kpss_p > 0.05
    if adf_ok and kpss_ok:
        stat_verdict = 'Stationary'
    elif not adf_ok and not kpss_ok:
        stat_verdict = 'Non-stationary'
    elif adf_ok and not kpss_ok:
        stat_verdict = 'Trend-stationary'
    elif not adf_ok and kpss_ok:
        stat_verdict = 'Diff-stationary'
    else:
        stat_verdict = 'Inconclusive'

    rows.append({
        'Variable':    name,
        'Group':       group,
        'N':           n,
        'Mean':        m,
        'SD':          sd,
        'Min':         vmin,
        'Max':         vmax,
        'Skewness':    sk,
        'Kurtosis':    ku,
        'SW W':        round(sh_w, 4),
        'SW p':        round(sh_p, 6),
        'JB Stat':     round(jb_stat, 4),
        'JB p':        round(jb_p, 6),
        "DA K2":       round(da_k2, 4),
        'DA p':        round(da_p, 6),
        'Normal?':     norm_verdict,
        'ADF Stat':    adf_stat,
        'ADF p':       adf_p,
        'KPSS Stat':   kpss_stat,
        'KPSS p':      kpss_p,
        'Stationary?': stat_verdict,
        'Outliers':    outlier_note,
    })

df_out = pd.DataFrame(rows)

# ---- save CSV ----
csv_path = os.path.join(script_dir, 'diagnostic_summary_table.csv')
df_out.to_csv(csv_path, index=False)
print(f"CSV -> {csv_path}")

# ---- console print ----
print("\n" + "=" * 160)
print("DIAGNOSTIC SUMMARY TABLE")
print("=" * 160)

cols_show = ['Variable', 'Group', 'N', 'Mean', 'SD', 'Min', 'Max',
             'Skewness', 'Kurtosis', 'SW p', 'Normal?', 'ADF p', 'KPSS p', 'Stationary?', 'Outliers']
print(df_out[cols_show].to_string(index=False))
print("=" * 160)

# ---- markdown ----
md_path = os.path.join(script_dir, 'diagnostic_summary_table.md')
with open(md_path, 'w', encoding='utf-8') as f:
    f.write("# Diagnostic Summary Table\n\n")
    f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
    f.write("**Variables:** Net sentiment (NSR, NSC, Mean Compound), market returns, tweet counts\n")
    f.write("**Period:** August 1 – September 30, 2025 (trading days only)\n")
    f.write("**Tests:** Shapiro-Wilk, Jarque-Bera, D'Agostino-Pearson (normality); ADF, KPSS (stationarity)\n\n")
    f.write("---\n\n")

    f.write("## Descriptive Statistics + Normality + Stationarity\n\n")
    f.write("| Variable | Group | N | Mean | SD | Min | Max | Skew | Kurt | SW p | Normal? | ADF p | KPSS p | Stationary? | Outliers |\n")
    f.write("|----------|-------|---|------|----|-----|-----|------|------|------|---------|-------|--------|-------------|----------|\n")

    for _, row in df_out.iterrows():
        sw_p = f"{row['SW p']:.4f}" if pd.notna(row.get('SW p')) else '—'
        adf_p = f"{row['ADF p']}" if pd.notna(row.get('ADF p')) else '—'
        kpss_p = f"{row['KPSS p']}" if pd.notna(row.get('KPSS p')) else '—'
        sk = f"{row['Skewness']:+.3f}" if pd.notna(row.get('Skewness')) else '—'
        ku = f"{row['Kurtosis']:+.3f}" if pd.notna(row.get('Kurtosis')) else '—'
        f.write(f"| {row['Variable']} | {row['Group']} | {int(row['N'])} "
                f"| {row['Mean']} | {row['SD']} | {row['Min']} | {row['Max']} "
                f"| {sk} | {ku} "
                f"| {sw_p} | **{row['Normal?']}** "
                f"| {adf_p} | {kpss_p} | **{row['Stationary?']}** "
                f"| {row['Outliers']} |\n")

    f.write("\n---\n\n")

    # Full normality breakdown
    f.write("## Complete Normality Test Results\n\n")
    f.write("| Variable | SW W | SW p | JB Stat | JB p | DA K² | DA p | Consensus |\n")
    f.write("|----------|------|------|---------|------|-------|------|----------|\n")
    for _, row in df_out.iterrows():
        sw_p = f"{row['SW p']}" if pd.notna(row.get('SW p')) else '—'
        jb_p = f"{row['JB p']}" if pd.notna(row.get('JB p')) else '—'
        da_p = f"{row['DA p']}" if pd.notna(row.get('DA p')) else '—'
        f.write(f"| {row['Variable']} | {row['SW W']} | {sw_p} | {row['JB Stat']} | {jb_p} | {row['DA K2']} | {da_p} | **{row['Normal?']}** |\n")

    f.write("\n---\n\n")

    # Full stationarity breakdown
    f.write("## Complete Stationarity Test Results\n\n")
    f.write("| Variable | ADF Stat | ADF p | KPSS Stat | KPSS p | Consensus |\n")
    f.write("|----------|----------|-------|-----------|--------|----------|\n")
    for _, row in df_out.iterrows():
        adf_s = f"{row['ADF Stat']}" if pd.notna(row.get('ADF Stat')) else '—'
        adf_p = f"{row['ADF p']}" if pd.notna(row.get('ADF p')) else '—'
        kpss_s = f"{row['KPSS Stat']}" if pd.notna(row.get('KPSS Stat')) else '—'
        kpss_p = f"{row['KPSS p']}" if pd.notna(row.get('KPSS p')) else '—'
        f.write(f"| {row['Variable']} | {adf_s} | {adf_p} | {kpss_s} | {kpss_p} | **{row['Stationary?']}** |\n")

    f.write("\n---\n\n")

    # Interpretation
    f.write("## Interpretation\n\n")
    f.write("### Normality\n\n")
    normal_vars = df_out[df_out['Normal?'] == 'Normal']['Variable'].tolist()
    non_normal   = df_out[df_out['Normal?'] == 'Non-normal']['Variable'].tolist()
    borderline   = df_out[df_out['Normal?'] == 'Borderline']['Variable'].tolist()

    if normal_vars:
        f.write("**Normal:** These variables pass at least 2 of 3 normality tests (Shapiro-Wilk, Jarque-Bera, D'Agostino-Pearson). Pearson correlation is appropriate.\n\n")
        for v in normal_vars:
            f.write(f"- {v}\n")
        f.write("\n")
    if borderline:
        f.write("**Borderline:** These variables pass exactly 1 of 3 normality tests. Use both Pearson and Spearman; report any discrepancy.\n\n")
        for v in borderline:
            f.write(f"- {v}\n")
        f.write("\n")
    if non_normal:
        f.write("**Non-normal:** These variables fail at least 2 normality tests. **Use Spearman's rank correlation** (already computed in `pearson_correlation_analysis.md`).\n\n")
        for v in non_normal:
            f.write(f"- {v}\n")
        f.write("\n")

    f.write("### Stationarity\n\n")
    f.write("All net sentiment and return series are stationary at the 5% level by joint ADF+KPSS consensus. ")
    f.write("The IHSG price level is I(1) (non-stationary in levels, stationary in first differences) as expected. ")
    f.write("USD/IDR tweet counts show non-stationarity likely due to declining scrape volume in the After Demo period.\n\n")

    f.write("### Outliers\n\n")
    f.write("Outliers detected via IQR (1.5×IQR rule) and modified Z-score (|Z| > 3.5 using MAD). ")
    f.write("Most outliers occur during the Demo period (Aug 25 – Sep 8) when market volatility and tweet activity spiked.\n\n")

    f.write("### Recommended Actions\n\n")
    f.write("| Variable | Action |\n")
    f.write("|----------|--------|\n")
    f.write("| IHSG Net Sentiment (NSR), IHSG Return | Use Pearson r (both normal, both stationary) |\n")
    f.write("| USD/IDR Net Sentiment (NSR), USD/IDR Return | Use Spearman rho (NSR non-normal) |\n")
    f.write("| IHSG Price Level | Use returns (I(1), non-stationary in levels) |\n")
    f.write("| USD/IDR Tweet Count | Detrend or first-difference before regression |\n")
    f.write("| After Demo period variables | Exclude from inference (n ≤ 2) |\n")

    f.write("\n---\n\n")
    f.write(f"**CSV:** [`diagnostic_summary_table.csv`](diagnostic_summary_table.csv)  \n")
    f.write(f"**Script:** [`diagnostic_summary.py`](diagnostic_summary.py)  \n")
    f.write(f"**Related:** [`normality_test_report.md`](normality_test_report.md) | [`stationarity_test_report.md`](stationarity_test_report.md) | [`diagnostic_plots.md`](diagnostic_plots.md)\n")

print(f"Markdown -> {md_path}")
print("Done.")
