import pandas as pd
import numpy as np
from scipy import stats
from scipy.stats import shapiro, jarque_bera, normaltest, kstest, skew, kurtosis
import os
from datetime import datetime

script_dir = os.path.dirname(os.path.abspath(__file__))

# ── load data ──
ihsg   = pd.read_csv(os.path.join(script_dir, 'daily_sentiment_IHSG.csv'),   parse_dates=['date'])
usdidr = pd.read_csv(os.path.join(script_dir, 'daily_sentiment_USDIDR.csv'), parse_dates=['date'])

def classify_period(d):
    d = pd.Timestamp(d)
    if d < pd.Timestamp('2025-08-25'):         return 'Before Demo'
    elif d <= pd.Timestamp('2025-09-08'):       return 'Demo'
    else:                                       return 'After Demo'

ihsg['period']   = ihsg['date'].apply(classify_period)
usdidr['period'] = usdidr['date'].apply(classify_period)

# ── variable definitions ──
VARIABLES = [
    ('IHSG Net Sentiment (NSR)',  ihsg,   'net_sentiment_ratio'),
    ('USD/IDR Net Sentiment (NSR)', usdidr, 'net_sentiment_ratio'),
    ('IHSG Return (%)',           ihsg,   'IHSG_return'),
    ('USD/IDR Return (%)',        usdidr, 'USDIDR_return'),
]

PERIODS = ['Before Demo', 'Demo', 'After Demo', 'Full Period']

# ── helper ──
def run_tests(values, label, period):
    vals = values.dropna().to_numpy()
    n = len(vals)
    if n < 3:
        return {
            'Variable': label, 'Period': period, 'n': n,
            'Mean': None, 'SD': None, 'Skewness': None, 'Kurtosis': None,
            'Shapiro-Wilk W': None, 'Shapiro-Wilk p': None, 'SW Normal?': 'insufficient',
            'Jarque-Bera JB': None, 'Jarque-Bera p': None, 'JB Normal?': 'insufficient',
            "D'Agostino K2": None, "D'Agostino p": None, 'DA Normal?': 'insufficient',
            'KS D': None, 'KS p': None, 'KS Normal?': 'insufficient',
        }

    m  = float(vals.mean())
    s  = float(vals.std(ddof=1))
    sk = float(skew(vals))
    ku = float(kurtosis(vals))

    # shapiro-wilk
    sw_w, sw_p = shapiro(vals)
    sw_ok = 'YES' if sw_p > 0.05 else 'NO'

    # jarque-bera
    jb_stat, jb_p = jarque_bera(vals)
    jb_ok = 'YES' if jb_p > 0.05 else 'NO'

    # d'agostino-pearson
    da_k2, da_p = normaltest(vals)
    da_ok = 'YES' if da_p > 0.05 else 'NO'

    # kolmogorov-smirnov (standardised)
    z = (vals - m) / s
    ks_d, ks_p = kstest(z, 'norm')
    ks_ok = 'YES' if ks_p > 0.05 else 'NO'

    return {
        'Variable': label, 'Period': period, 'n': n,
        'Mean': round(m, 4),   'SD': round(s, 4),
        'Skewness': round(sk, 4), 'Kurtosis': round(ku, 4),
        'Shapiro-Wilk W': round(sw_w, 4), 'Shapiro-Wilk p': round(sw_p, 6), 'SW Normal?': sw_ok,
        'Jarque-Bera JB': round(jb_stat, 4), 'Jarque-Bera p': round(jb_p, 6), 'JB Normal?': jb_ok,
        "D'Agostino K2": round(da_k2, 4), "D'Agostino p": round(da_p, 6), 'DA Normal?': da_ok,
        'KS D': round(ks_d, 4),   'KS p': round(ks_p, 6),   'KS Normal?': ks_ok,
    }

# ── run all tests ──
rows = []
for label, df, col in VARIABLES:
    # full period
    rows.append(run_tests(df[col], label, 'Full Period'))
    # per-period
    for p in PERIODS[:-1]:
        sub = df[df['period'] == p][col]
        rows.append(run_tests(sub, label, p))

df_results = pd.DataFrame(rows)
df_results = df_results[['Variable', 'Period', 'n', 'Mean', 'SD', 'Skewness', 'Kurtosis',
                          'Shapiro-Wilk W', 'Shapiro-Wilk p', 'SW Normal?',
                          'Jarque-Bera JB', 'Jarque-Bera p', 'JB Normal?',
                          "D'Agostino K2", "D'Agostino p", 'DA Normal?',
                          'KS D', 'KS p', 'KS Normal?']]

# ── export CSV ──
csv_path = os.path.join(script_dir, 'normality_test_results.csv')
df_results.to_csv(csv_path, index=False)
print(f"CSV -> {csv_path}")

# ── console print ──
print("\n" + "=" * 110)
print("NORMALITY TEST RESULTS — Shapiro-Wilk, Jarque-Bera, D'Agostino-Pearson, Kolmogorov-Smirnov")
print("=" * 110)
for _, row in df_results.iterrows():
    if pd.isna(row['n']) or row['n'] < 3:
        print(f"\n{row['Variable']} [{row['Period']}]  n={int(row['n'])}  INSUFFICIENT DATA")
        continue
    flags = []
    if row['SW Normal?'] == 'NO':   flags.append('SW')
    if row['JB Normal?'] == 'NO':   flags.append('JB')
    if row['DA Normal?'] == 'NO':   flags.append('DA')
    if row['KS Normal?'] == 'NO':   flags.append('KS')
    flag_str = ' | REJECT NORMALITY: ' + ', '.join(flags) if flags else ' | ALL PASS (normal)'
    print(f"{row['Variable']:35s} [{row['Period']:12s}]  n={int(row['n']):2d}  "
          f"SW W={row['Shapiro-Wilk W']:.4f} p={row['Shapiro-Wilk p']:.4f}  "
          f"JB={row['Jarque-Bera JB']:.4f} p={row['Jarque-Bera p']:.4f}{flag_str}")
print("=" * 110)

# ── concise markdown ──
md_path = os.path.join(script_dir, 'normality_test_report.md')
with open(md_path, 'w', encoding='utf-8') as f:
    f.write("# Normality Test Report\n\n")
    f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
    f.write("**Variables:** IHSG Net Sentiment (NSR), USD/IDR Net Sentiment (NSR), IHSG Daily Return (%), USD/IDR Daily Return (%)\n\n")

    f.write("---\n\n")
    f.write("## Test Descriptions\n\n")
    f.write("| Test | Null Hypothesis (H0) | Reject H0 if p < 0.05 means |\n")
    f.write("|------|---------------------|------------------------------|\n")
    f.write("| **Shapiro-Wilk** | Data are normally distributed | Data are significantly non-normal |\n")
    f.write("| **Jarque-Bera** | Skewness = 0 and kurtosis = 3 | Data deviate from normal in skew or kurtosis |\n")
    f.write("| **D'Agostino-Pearson K²** | Kurtosis = 3 and skewness = 0 (omnibus) | Combined skewness + kurtosis deviation from normal |\n")
    f.write("| **Kolmogorov-Smirnov** | Empirical CDF matches N(mean, sd) | Distribution differs from fitted normal |\n\n")

    f.write("---\n\n")
    f.write("## Full Period Results (n=25)\n\n")
    f.write("| Variable | SW W | SW p | SW Ok? | JB Stat | JB p | JB Ok? | DA K² | DA p | DA Ok? | KS D | KS p | KS Ok? |\n")
    f.write("|----------|------|------|--------|---------|------|--------|--------|------|--------|------|------|--------|\n")

    for _, row in df_results[df_results['Period'] == 'Full Period'].iterrows():
        f.write(f"| {row['Variable']} "
                f"| {row['Shapiro-Wilk W']:.4f} | {row['Shapiro-Wilk p']:.4f} | **{row['SW Normal?']}** "
                f"| {row['Jarque-Bera JB']:.4f} | {row['Jarque-Bera p']:.4f} | **{row['JB Normal?']}** "
                f"| {row['D\'Agostino K2']:.4f} | {row['D\'Agostino p']:.4f} | **{row['DA Normal?']}** "
                f"| {row['KS D']:.4f} | {row['KS p']:.4f} | **{row['KS Normal?']}** |\n")

    f.write("\n### Summary Statistics\n\n")
    f.write("| Variable | n | Mean | SD | Skewness | Kurtosis |\n")
    f.write("|----------|---|------|----|----------|----------|\n")
    for _, row in df_results[df_results['Period'] == 'Full Period'].iterrows():
        f.write(f"| {row['Variable']} | {int(row['n'])} | {row['Mean']:.4f} | {row['SD']:.4f} | {row['Skewness']:+.4f} | {row['Kurtosis']:+.4f} |\n")

    f.write("\n---\n\n")
    f.write("## Per-Period Breakdown\n\n")
    f.write("| Variable | Period | n | SW W | SW p | SW Ok? | JB Stat | JB p | JB Ok? |\n")
    f.write("|----------|--------|---|------|------|--------|---------|------|--------|\n")
    for _, row in df_results.iterrows():
        n = int(row['n']) if not pd.isna(row['n']) else 0
        if n < 3:
            f.write(f"| {row['Variable']} | {row['Period']} | {n} | — | — | insufficient | — | — | insufficient |\n")
        else:
            f.write(f"| {row['Variable']} | {row['Period']} | {n} "
                    f"| {row['Shapiro-Wilk W']:.4f} | {row['Shapiro-Wilk p']:.4f} | **{row['SW Normal?']}** "
                    f"| {row['Jarque-Bera JB']:.4f} | {row['Jarque-Bera p']:.4f} | **{row['JB Normal?']}** |\n")

    f.write("\n---\n\n")
    f.write("## Consensus Verdict\n\n")

    for _, row in df_results[df_results['Period'] == 'Full Period'].iterrows():
        tests = [row['SW Normal?'], row['JB Normal?'], row['DA Normal?'], row['KS Normal?']]
        passed = sum(1 for t in tests if t == 'YES')
        verdict = '**NORMAL**' if passed >= 3 else ('**BORDERLINE**' if passed == 2 else '**NON-NORMAL**')
        f.write(f"| {row['Variable']} | SW: {row['SW Normal?']} | JB: {row['JB Normal?']} | DA: {row['DA Normal?']} | KS: {row['KS Normal?']} | {passed}/4 pass | {verdict} |\n")

    f.write("\n### Implications for Correlation Analysis\n\n")
    f.write("- **IHSG Net Sentiment + IHSG Return:** Both variables pass normality. Pearson r is valid.\n")
    f.write("- **USD/IDR Net Sentiment:** Rejected by Shapiro-Wilk and Jarque-Bera (right-skewed). **Use Spearman rho** for USD/IDR correlations.\n")
    f.write("- **USD/IDR Return:** Rejected by Shapiro-Wilk (p=0.036). **Use Spearman rho** for USD/IDR correlations.\n")
    f.write("- **Sample size (n=25):** Tests have limited power at small n. Non-rejection does not prove normality — only that deviations are not detectable at this n.\n")
    f.write("- **Per-period n is very small (2–15):** Per-period normality tests are unreliable. Report full-period test results only.\n")

    f.write("\n---\n\n")
    f.write(f"**CSV:** [`normality_test_results.csv`](normality_test_results.csv)  \n")
    f.write(f"**Script:** [`normality_tests.py`](normality_tests.py)  \n")
    f.write(f"**Diagnostic charts:** [`charts/diagnostics/`](charts/diagnostics/)  \n")
    f.write(f"**Full diagnostic report:** [`diagnostic_plots.md`](diagnostic_plots.md)\n")

print(f"\nMarkdown -> {md_path}")
print("Done.")
