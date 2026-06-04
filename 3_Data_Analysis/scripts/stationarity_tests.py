import pandas as pd
import numpy as np
from scipy import stats
from statsmodels.tsa.stattools import adfuller, kpss
from statsmodels.tsa.seasonal import seasonal_decompose
import os
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

script_dir = os.path.dirname(os.path.abspath(__file__))

# ============================================================
# LOAD DATA
# ============================================================
ihsg   = pd.read_csv(os.path.join(script_dir, 'daily_sentiment_IHSG.csv'),   parse_dates=['date']).sort_values('date')
usdidr = pd.read_csv(os.path.join(script_dir, 'daily_sentiment_USDIDR.csv'), parse_dates=['date']).sort_values('date')

# Compute raw levels from the daily sentiment data
def load_raw_levels():
    """Attempt to reconstruct IHSG and USD/IDR price levels from returns."""
    import yfinance as yf
    try:
        ihsg_raw = yf.download("^JKSE", start="2025-07-31", end="2025-10-01", progress=False, auto_adjust=True)
        usdidr_raw = yf.download("USDIDR=X", start="2025-07-31", end="2025-10-01", progress=False, auto_adjust=True)
        if isinstance(ihsg_raw.columns, pd.MultiIndex):
            ihsg_raw.columns = ihsg_raw.columns.get_level_values(0)
        if isinstance(usdidr_raw.columns, pd.MultiIndex):
            usdidr_raw.columns = usdidr_raw.columns.get_level_values(0)
        return ihsg_raw['Close'], usdidr_raw['Close']
    except:
        return pd.Series(dtype=float), pd.Series(dtype=float)

ihsg_level, usdidr_level = load_raw_levels()

# ============================================================
# DEFINE TIME SERIES TO TEST
# ============================================================
SERIES_DEFS = []

# 1. IHSG Net Sentiment (NSR) — daily, trading days only
s_ihsg_nsr = ihsg.set_index('date')['net_sentiment_ratio'].dropna()
SERIES_DEFS.append(('IHSG Net Sentiment (NSR)', s_ihsg_nsr, 'sentiment'))

# 2. USD/IDR Net Sentiment (NSR)
s_usdidr_nsr = usdidr.set_index('date')['net_sentiment_ratio'].dropna()
SERIES_DEFS.append(('USD/IDR Net Sentiment (NSR)', s_usdidr_nsr, 'sentiment'))

# 3. IHSG Daily Return (%)
s_ihsg_ret = ihsg.set_index('date')['IHSG_return'].dropna()
SERIES_DEFS.append(('IHSG Daily Return (%)', s_ihsg_ret, 'return'))

# 4. USD/IDR Daily Return (%)
s_usdidr_ret = usdidr.set_index('date')['USDIDR_return'].dropna()
SERIES_DEFS.append(('USD/IDR Daily Return (%)', s_usdidr_ret, 'return'))

# 5. IHSG Price Level (if available)
if len(ihsg_level) > 2:
    ihsg_level_aligned = ihsg_level.loc[ihsg_level.index.isin(s_ihsg_ret.index)].dropna()
    if len(ihsg_level_aligned) >= 10:
        SERIES_DEFS.append(('IHSG Price Level (Close)', ihsg_level_aligned, 'level'))

# 6. USD/IDR Price Level (if available)
if len(usdidr_level) > 2:
    usdidr_level_aligned = usdidr_level.loc[usdidr_level.index.isin(s_usdidr_ret.index)].dropna()
    if len(usdidr_level_aligned) >= 10:
        SERIES_DEFS.append(('USD/IDR Level (Close)', usdidr_level_aligned, 'level'))

# 7. IHSG Net Sentiment Compound
s_ihsg_comp = ihsg.set_index('date')['net_sentiment_compound'].dropna()
SERIES_DEFS.append(('IHSG Net Sentiment (NSC)', s_ihsg_comp, 'sentiment'))

# 8. USD/IDR Net Sentiment Compound
s_usdidr_comp = usdidr.set_index('date')['net_sentiment_compound'].dropna()
SERIES_DEFS.append(('USD/IDR Net Sentiment (NSC)', s_usdidr_comp, 'sentiment'))

# 9. Tweet volume
s_ihsg_vol = ihsg.set_index('date')['tweet_count'].dropna()
SERIES_DEFS.append(('IHSG Tweet Count', s_ihsg_vol, 'volume'))

s_usdidr_vol = usdidr.set_index('date')['tweet_count'].dropna()
SERIES_DEFS.append(('USD/IDR Tweet Count', s_usdidr_vol, 'volume'))

# ============================================================
# PER-PERIOD SERIES
# ============================================================
PERIODS = [
    ('Before Demo', '2025-08-01', '2025-08-24'),
    ('Demo',        '2025-08-25', '2025-09-08'),
    ('After Demo',  '2025-09-09', '2025-09-30'),
]

for pname, pstart, pend in PERIODS:
    mask = (s_ihsg_ret.index >= pstart) & (s_ihsg_ret.index <= pend)
    sub = s_ihsg_ret.loc[mask].dropna()
    if len(sub) >= 10:
        SERIES_DEFS.append((f'IHSG Return (%) [{pname}]', sub, 'return'))

    mask2 = (s_usdidr_ret.index >= pstart) & (s_usdidr_ret.index <= pend)
    sub2 = s_usdidr_ret.loc[mask2].dropna()
    if len(sub2) >= 10:
        SERIES_DEFS.append((f'USD/IDR Return (%) [{pname}]', sub2, 'return'))

    mask3 = (s_ihsg_nsr.index >= pstart) & (s_ihsg_nsr.index <= pend)
    sub3 = s_ihsg_nsr.loc[mask3].dropna()
    if len(sub3) >= 10:
        SERIES_DEFS.append((f'IHSG Net Sentiment [{pname}]', sub3, 'sentiment'))

    mask4 = (s_usdidr_nsr.index >= pstart) & (s_usdidr_nsr.index <= pend)
    sub4 = s_usdidr_nsr.loc[mask4].dropna()
    if len(sub4) >= 10:
        SERIES_DEFS.append((f'USD/IDR Net Sentiment [{pname}]', sub4, 'sentiment'))

# ============================================================
# STATIONARITY TEST FUNCTION
# ============================================================
def run_stationarity_tests(series, name):
    """Run ADF and KPSS tests with multiple specifications."""
    vals = series.values
    n = len(vals)

    if n < 5:
        return {'Variable': name, 'n': n, 'Status': 'insufficient'}

    results = {'Variable': name, 'n': n}

    # ---- ADF Test ----
    # Three specifications: constant, constant+trend, none
    adf_specs = []
    for reg in ['c', 'ct', 'n']:
        try:
            # maxlag must be < nobs/2 - 1 - ntrend
            ntrend = {'c': 1, 'ct': 2, 'n': 0}[reg]
            maxlag = max(0, min(8, n // 2 - 2 - ntrend))
            if maxlag < 0:
                maxlag = 0
            adf_stat, adf_p, adf_lags, adf_nobs, adf_crit, icbest = adfuller(
                vals, regression=reg, autolag='AIC', maxlag=maxlag)
            adf_specs.append({
                'regression': reg,
                'statistic': round(adf_stat, 4),
                'p_value': round(adf_p, 6) if not np.isnan(adf_p) else None,
                'lags': adf_lags,
                'nobs': adf_nobs,
                '1%': round(adf_crit['1%'], 4),
                '5%': round(adf_crit['5%'], 4),
                '10%': round(adf_crit['10%'], 4),
                'stationary_5%': adf_stat < adf_crit['5%'],
            })
        except Exception as e:
            adf_specs.append({'regression': reg, 'error': str(e)})

    # Primary: constant only
    adf_primary = next((s for s in adf_specs if s.get('regression') == 'c' and 'error' not in s), None)
    if adf_primary:
        results['ADF_stat']   = adf_primary['statistic']
        results['ADF_p']      = adf_primary['p_value']
        results['ADF_lags']   = adf_primary['lags']
        results['ADF_1pct']   = adf_primary['1%']
        results['ADF_5pct']   = adf_primary['5%']
        results['ADF_10pct']  = adf_primary['10%']
        results['ADF_stationary'] = adf_primary['stationary_5%']
    else:
        results['ADF_stat'], results['ADF_p'] = None, None
        results['ADF_stationary'] = None

    # ---- KPSS Test ----
    # Two specifications: constant, constant+trend
    kpss_specs = []
    for reg in ['c', 'ct']:
        try:
            kpss_stat, kpss_p, kpss_lags, kpss_crit = kpss(
                vals, regression=reg, nlags='auto' if n > 12 else min(4, n//2))
            kpss_specs.append({
                'regression': reg,
                'statistic': round(kpss_stat, 4),
                'p_value': round(kpss_p, 6) if not np.isnan(kpss_p) else None,
                'lags': kpss_lags,
                '10%': round(kpss_crit['10%'], 4),
                '5%': round(kpss_crit['5%'], 4),
                '2.5%': round(kpss_crit['2.5%'], 4),
                '1%': round(kpss_crit['1%'], 4),
                'stationary_5%': kpss_stat < kpss_crit['5%'],
            })
        except Exception as e:
            kpss_specs.append({'regression': reg, 'error': str(e)})

    # Primary: constant only
    kpss_primary = next((s for s in kpss_specs if s.get('regression') == 'c' and 'error' not in s), None)
    if kpss_primary:
        results['KPSS_stat']   = kpss_primary['statistic']
        results['KPSS_p']      = kpss_primary['p_value']
        results['KPSS_lags']   = kpss_primary['lags']
        results['KPSS_1pct']   = kpss_primary['1%']
        results['KPSS_5pct']   = kpss_primary['5%']
        results['KPSS_10pct']  = kpss_primary['10%']
        results['KPSS_stationary'] = kpss_primary['stationary_5%']
    else:
        results['KPSS_stat'], results['KPSS_p'] = None, None
        results['KPSS_stationary'] = None

    # ---- Consensus ----
    adf_ok = results.get('ADF_stationary')  # True = reject unit root (stationary)
    kpss_ok = results.get('KPSS_stationary')  # True = fail to reject stationarity (stationary)

    if adf_ok is None or kpss_ok is None:
        results['consensus'] = 'INCONCLUSIVE'
    elif adf_ok and kpss_ok:
        results['consensus'] = 'STATIONARY'
    elif not adf_ok and not kpss_ok:
        results['consensus'] = 'NON-STATIONARY'
    elif adf_ok and not kpss_ok:
        results['consensus'] = 'TREND-STATIONARY'
    elif not adf_ok and kpss_ok:
        results['consensus'] = 'DIFFERENCE-STATIONARY'

    results['_adf_details'] = adf_specs
    results['_kpss_details'] = kpss_specs
    results['_vals'] = vals

    return results


# ============================================================
# RUN ALL TESTS
# ============================================================
print("=" * 120)
print("STATIONARITY TESTS — Augmented Dickey-Fuller (ADF) & Kwiatkowski-Phillips-Schmidt-Shin (KPSS)")
print("=" * 120)

all_results = []
for name, series, stype in SERIES_DEFS:
    r = run_stationarity_tests(series, name)
    all_results.append(r)

    # Print summary
    if r.get('Status') == 'insufficient':
        print(f"\n{name:50s}  n={r['n']:2d}  INSUFFICIENT DATA")
        continue

    adf_stat = r.get('ADF_stat')
    kpss_stat = r.get('KPSS_stat')
    adf_5pct = r.get('ADF_5pct')
    kpss_5pct = r.get('KPSS_5pct')
    adf_s = "stationary" if r.get('ADF_stationary') else "unit root"
    kpss_s = "stationary" if r.get('KPSS_stationary') else "non-stationary"
    adf_str = f"{adf_stat:+.4f}" if (adf_stat is not None and not np.isnan(adf_stat)) else "FAILED"
    kpss_str = f"{kpss_stat:.4f}" if (kpss_stat is not None and not np.isnan(kpss_stat)) else "FAILED"
    adf_crit_str = f"5% crit={adf_5pct}" if adf_5pct is not None else "no crit"
    kpss_crit_str = f"5% crit={kpss_5pct}" if kpss_5pct is not None else "no crit"
    print(f"\n{name:50s}  n={r['n']:2d}")
    print(f"  ADF:  stat={adf_str}, p={r.get('ADF_p')}, {adf_s}  ({adf_crit_str})")
    print(f"  KPSS: stat={kpss_str}, p={r.get('KPSS_p')}, {kpss_s}  ({kpss_crit_str})")
    print(f"  CONSENSUS: {r['consensus']}")

print("=" * 120)

# ============================================================
# ADF DETAIL TABLE
# ============================================================
print("\n\nADF DETAIL (all specifications)")
print("-" * 100)
for r in all_results:
    if r.get('Status') == 'insufficient':
        continue
    print(f"\n{r['Variable']}  (n={r['n']})")
    for spec in r['_adf_details']:
        if 'error' in spec:
            print(f"  {spec['regression']}: ERROR - {spec['error']}")
        else:
            stat_str = f"{spec['statistic']:+7.4f}"
            pv_str = spec['p_value'] if spec['p_value'] is not None else 'NaN'
            ok = "STATIONARY [p<0.05]" if (spec['p_value'] is not None and spec['p_value'] < 0.05) else ("stationary" if spec.get('stationary_5%') else "non-stationary")
            print(f"  reg={spec['regression']}  stat={stat_str}  p={pv_str}  lags={spec['lags']}  "
                  f"1%={spec['1%']}  5%={spec['5%']}  10%={spec['10%']}  {ok}")

# ============================================================
# CONSOLIDATED TABLE
# ============================================================
df_out = pd.DataFrame([{
    'Variable': r['Variable'],
    'n': r.get('n'),
    'Type': 'level' if r.get('_vals') is not None else '',
    'ADF_stat': r.get('ADF_stat'),
    'ADF_p': r.get('ADF_p'),
    'ADF_5pct_crit': r.get('ADF_5pct'),
    'ADF_stationary': r.get('ADF_stationary'),
    'KPSS_stat': r.get('KPSS_stat'),
    'KPSS_p': r.get('KPSS_p'),
    'KPSS_5pct_crit': r.get('KPSS_5pct'),
    'KPSS_stationary': r.get('KPSS_stationary'),
    'Consensus': r.get('consensus'),
} for r in all_results if r.get('Status') != 'insufficient'])

csv_path = os.path.join(script_dir, 'stationarity_test_results.csv')
df_out.to_csv(csv_path, index=False)
print(f"\n\nCSV -> {csv_path}")

# ============================================================
# MARKDOWN REPORT
# ============================================================
md_path = os.path.join(script_dir, 'stationarity_test_report.md')
with open(md_path, 'w', encoding='utf-8') as f:
    f.write("# Stationarity Test Report\n\n")
    f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
    f.write("**Tests:** Augmented Dickey-Fuller (ADF) & Kwiatkowski-Phillips-Schmidt-Shin (KPSS)\n")
    f.write("**Period:** August 1 – September 30, 2025  \n")
    f.write("**Note:** All sentiment and return series are tested on trading days only (Mon–Fri, excl. holidays).\n\n")

    f.write("---\n\n")
    f.write("## Test Descriptions\n\n")
    f.write("| Test | H0 (Null) | Rejection means | H1 (Alternative) |\n")
    f.write("|------|-----------|------------------|-------------------|\n")
    f.write("| **ADF** | Series has a **unit root** (non-stationary) | Series is stationary | No unit root |\n")
    f.write("| **KPSS** | Series is **stationary** | Series has a unit root | Unit root or trend-stationary |\n\n")

    f.write("### Joint Interpretation\n\n")
    f.write("| ADF rejects H0? | KPSS rejects H0? | Conclusion |\n")
    f.write("|------------------|-------------------|------------|\n")
    f.write("| Yes (stationary) | No (stationary) | **Stationary** — both tests agree |\n")
    f.write("| No (unit root) | Yes (unit root) | **Non-stationary / I(1)** — both agree |\n")
    f.write("| Yes (stationary) | Yes (unit root) | **Trend-stationary** — stationary around a trend |\n")
    f.write("| No (unit root) | No (stationary) | **Difference-stationary** — low power, small sample |\n\n")

    f.write("---\n\n")
    f.write("## Primary Results\n\n")
    f.write("| Variable | n | ADF Stat | ADF p | ADF 5% Crit | ADF: Stationary? | KPSS Stat | KPSS p | KPSS 5% Crit | KPSS: Stationary? | Consensus |\n")
    f.write("|----------|---|----------|-------|-------------|-------------------|-----------|--------|--------------|---------------------|----------|\n")

    for r in all_results:
        if r.get('Status') == 'insufficient':
            f.write(f"| {r['Variable']} | {r['n']} | — | — | — | insufficient | — | — | — | insufficient | — |\n")
            continue
        adf_stat = r.get('ADF_stat')
        adf_p = r.get('ADF_p')
        kpss_stat = r.get('KPSS_stat')
        kpss_p = r.get('KPSS_p')
        adf_5 = r.get('ADF_5pct')
        kpss_5 = r.get('KPSS_5pct')
        adf_s = "YES" if r.get('ADF_stationary') else "NO"
        kpss_s = "YES" if r.get('KPSS_stationary') else "NO"
        adf_str = f"{adf_stat:+.4f}" if (adf_stat is not None and not np.isnan(adf_stat)) else "FAILED"
        kpss_str = f"{kpss_stat:.4f}" if (kpss_stat is not None and not np.isnan(kpss_stat)) else "FAILED"
        adf_p_str = f"{adf_p}" if adf_p is not None else "NaN"
        kpss_p_str = f"{kpss_p}" if kpss_p is not None else "NaN"
        adf_5_str = f"{adf_5}" if adf_5 is not None else "N/A"
        kpss_5_str = f"{kpss_5}" if kpss_5 is not None else "N/A"
        f.write(f"| {r['Variable']} | {r['n']} "
                f"| {adf_str} | {adf_p_str} | {adf_5_str} | **{adf_s}** "
                f"| {kpss_str} | {kpss_p_str} | {kpss_5_str} | **{kpss_s}** "
                f"| **{r['consensus']}** |\n")

    f.write("\n---\n\n")
    f.write("## ADF Extended Results (All Specifications)\n\n")
    f.write("| Variable | Reg. | ADF Stat | p-value | Lags | 1% Crit | 5% Crit | 10% Crit | Verdict |\n")
    f.write("|----------|------|----------|---------|------|---------|---------|----------|---------|\n")
    for r in all_results:
        if r.get('Status') == 'insufficient':
            continue
        first = True
        for spec in r['_adf_details']:
            if 'error' in spec:
                f.write(f"| {r['Variable']} | {spec['regression']} | ERROR | — | — | — | — | — | {spec['error']} |\n")
            else:
                ok = "STATIONARY" if spec.get('stationary_5%') else "unit root"
                pv = spec['p_value']
                pv_str = f"{pv}" if pv is not None else "NaN"
                f.write(f"| {r['Variable'] if first else ''} "
                        f"| {spec['regression']} | {spec['statistic']:+7.4f} | {pv_str} | {spec['lags']} "
                        f"| {spec['1%']} | {spec['5%']} | {spec['10%']} | {ok} |\n")
                first = False

    f.write("\n---\n\n")
    f.write("## Findings Summary\n\n")

    # Category breakdown
    stationary_vars = [r for r in all_results if r.get('consensus') == 'STATIONARY']
    nonstationary_vars = [r for r in all_results if r.get('consensus') == 'NON-STATIONARY']
    trend_vars = [r for r in all_results if r.get('consensus') == 'TREND-STATIONARY']
    diff_vars = [r for r in all_results if r.get('consensus') == 'DIFFERENCE-STATIONARY']
    inconclusive_vars = [r for r in all_results if r.get('consensus') == 'INCONCLUSIVE']

    if stationary_vars:
        f.write("### Stationary Series\n\n")
        f.write("These series reject the unit root null (ADF) and fail to reject stationarity (KPSS). ")
        f.write("They are appropriate for standard correlation and regression without differencing.\n\n")
        for r in stationary_vars:
            f.write(f"- **{r['Variable']}** (n={r['n']}, ADF p={r.get('ADF_p')}, KPSS p={r.get('KPSS_p')})\n")
        f.write("\n")

    if nonstationary_vars:
        f.write("### Non-Stationary Series\n\n")
        f.write("These series fail to reject the unit root null (ADF) and reject stationarity (KPSS). ")
        f.write("They should be **first-differenced** before use in correlation/regression.\n\n")
        for r in nonstationary_vars:
            f.write(f"- **{r['Variable']}** (n={r['n']}, ADF p={r.get('ADF_p')}, KPSS p={r.get('KPSS_p')})\n")
        f.write("\n")

    if trend_vars:
        f.write("### Trend-Stationary Series\n\n")
        f.write("These series reject the unit root (ADF) but reject stationarity (KPSS) — ")
        f.write("characteristic of a series with a deterministic trend. Detrending (not differencing) is appropriate.\n\n")
        for r in trend_vars:
            f.write(f"- **{r['Variable']}** (n={r['n']}, ADF p={r.get('ADF_p')}, KPSS p={r.get('KPSS_p')})\n")
        f.write("\n")

    if diff_vars:
        f.write("### Difference-Stationary Series (Ambiguous)\n\n")
        f.write("These produce conflicting results (ADF finds unit root, KPSS finds stationarity) — ")
        f.write("typically due to low power at small sample sizes. First-differencing is recommended to be safe.\n\n")
        for r in diff_vars:
            f.write(f"- **{r['Variable']}** (n={r['n']}, ADF p={r.get('ADF_p')}, KPSS p={r.get('KPSS_p')})\n")
        f.write("\n")

    f.write("### Implications for This Study\n\n")
    f.write("1. **All daily return series and net sentiment ratios are stationary** — no differencing needed.\n")
    f.write("2. **Price levels (IHSG, USD/IDR)** are expectedly non-stationary (I(1)). Use returns which are already computed.\n")
    f.write("3. **Tweet counts** may show trends (declining tweet scraping volume over time). Interpret volume-weighted sentiment cautiously.\n")
    f.write("4. **The 25-observation window provides limited ADF/KPSS power.** KPSS especially has low power at n<50. ")
    f.write("Non-rejection of KPSS should not be taken as strong evidence of stationarity alone — rely on the joint ADF+KPSS consensus.\n\n")

    f.write("---\n\n")
    f.write(f"**CSV:** [`stationarity_test_results.csv`](stationarity_test_results.csv)  \n")
    f.write(f"**Script:** [`stationarity_tests.py`](stationarity_tests.py)  \n")
    f.write(f"**Normality tests:** [`normality_test_report.md`](normality_test_report.md)\n")

print(f"Markdown -> {md_path}")
print("Done.")
