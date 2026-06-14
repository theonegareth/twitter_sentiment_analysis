import pandas as pd, numpy as np
from scipy import stats
from scipy.stats import shapiro, jarque_bera, normaltest, iqr
from statsmodels.tsa.stattools import adfuller, kpss
import os, warnings
from datetime import datetime
warnings.filterwarnings('ignore')

script_dir = os.path.dirname(os.path.abspath(__file__))
df = pd.read_csv(os.path.join(script_dir, 'gpt5_merged.csv'), parse_dates=['date'])
n = len(df)

def classify_period(d):
    d = pd.Timestamp(d)
    if d < pd.Timestamp('2025-08-25'): return 'Before Demo'
    elif d <= pd.Timestamp('2025-09-08'): return 'Demo'
    else: return 'After Demo'

df['period'] = df['date'].apply(classify_period)

VARS = [
    ('Net Sentiment (GPT-5)', df['net_sentiment_ratio']),
    ('IHSG Return (%)',       df['IHSG_return']),
    ('USD/IDR Return (%)',    df['USDIDR_return']),
]

# ---- Normality ----
print("="*80)
print("NORMALITY TESTS (GPT-5 Data)")
print("="*80)
norm_rows = []
for name, s in VARS:
    vals = s.dropna().values
    sw_w, sw_p = shapiro(vals)
    jb_s, jb_p = jarque_bera(vals)
    da_k, da_p = normaltest(vals)
    sk = stats.skew(vals)
    ku = stats.kurtosis(vals)

    sw_ok = sw_p > 0.05
    jb_ok = jb_p > 0.05
    da_ok = da_p > 0.05
    fc = sum(1 for ok in [not sw_ok, not jb_ok, not da_ok] if ok)
    verdict = 'Non-normal' if fc >= 2 else ('Borderline' if fc == 1 else 'Normal')

    print(f"{name}: SW p={sw_p:.4f} JB p={jb_p:.4f} DA p={da_p:.4f} -> {verdict}")
    norm_rows.append({'Variable': name, 'N': len(vals), 'Mean': round(vals.mean(),4), 'SD': round(vals.std(ddof=1),4),
                      'Skew': round(sk,4), 'Kurt': round(ku,4), 'SW W': round(sw_w,4), 'SW p': round(sw_p,4),
                      'JB Stat': round(jb_s,4), 'JB p': round(jb_p,4), 'DA K2': round(da_k,4), 'DA p': round(da_p,4),
                      'Verdict': verdict})

# ---- Stationarity ----
print("\n" + "="*80)
print("STATIONARITY TESTS (GPT-5 Data)")
print("="*80)
for name, s in VARS:
    vals = s.dropna().values
    nv = len(vals)
    nlags = max(0, min(8, nv//2-2-1))
    if nlags < 0: nlags = 0
    try:
        adf_s, adf_p, _, _, adf_crit, _ = adfuller(vals, regression='c', autolag='AIC', maxlag=nlags)
        adf_ok = adf_p < 0.05
    except:
        adf_s, adf_p, adf_ok = np.nan, np.nan, None

    k_nlags = min(4, max(0, nv//2-1))
    try:
        kpss_s, kpss_p, _, kpss_crit = kpss(vals, regression='c', nlags=k_nlags)
        kpss_ok = kpss_p > 0.05
    except:
        kpss_s, kpss_p, kpss_ok = np.nan, np.nan, None

    if adf_ok is not None and kpss_ok is not None:
        if adf_ok and kpss_ok: consensus = 'Stationary'
        elif not adf_ok and not kpss_ok: consensus = 'Non-stationary'
        elif adf_ok and not kpss_ok: consensus = 'Trend-stationary'
        else: consensus = 'Diff-stationary'
    else:
        consensus = 'Inconclusive'

    print(f"{name}: ADF p={adf_p}, KPSS p={kpss_p} -> {consensus}")

# ---- Outliers ----
print("\n" + "="*80)
print("OUTLIER DETECTION (GPT-5 Data)")
print("="*80)
def detect_outliers(vals, dates):
    q1, q3 = np.percentile(vals, [25,75]); iqr_v = q3-q1; lo, hi = q1-1.5*iqr_v, q3+1.5*iqr_v
    iqr_idx = [i for i,v in enumerate(vals) if v<lo or v>hi]
    z = np.abs((vals - vals.mean())/vals.std(ddof=1)); z_idx = [i for i,zv in enumerate(z) if zv>2.5]
    all_idx = sorted(set(iqr_idx)|set(z_idx))
    return [(dates.iloc[i], vals[i], 'HIGH' if vals[i] > vals.mean() else 'LOW') for i in all_idx]

all_outliers = []
for name, s in VARS:
    sub = df[['date','net_sentiment_ratio','IHSG_return','USDIDR_return']].dropna()
    col = {VARS[0][0]:'net_sentiment_ratio', VARS[1][0]:'IHSG_return', VARS[2][0]:'USDIDR_return'}[name]
    outs = detect_outliers(sub[col].values, sub['date'])
    for d, v, direction in outs:
        all_outliers.append(f"  {pd.Timestamp(d).strftime('%Y-%m-%d')} | {name:25s} | {v:+10.4f} | {direction}")
    print(f"{name}: {len(outs)} outliers")
for o in all_outliers: print(o)

# ---- Correlations ----
print("\n" + "="*80)
print("CORRELATIONS (GPT-5 Data)")
print("="*80)
for xcol, ycol, label in [('net_sentiment_ratio','IHSG_return','IHSG'), ('net_sentiment_ratio','USDIDR_return','USD/IDR')]:
    x = df[xcol]; y = df[ycol]
    r,p = stats.pearsonr(x,y); rho,rp = stats.spearmanr(x,y)
    z = np.arctanh(r); se = 1/np.sqrt(n-3); zc = stats.norm.ppf(0.975)
    ci_l, ci_u = np.tanh(z - zc*se), np.tanh(z + zc*se)
    print(f"{label}: r={r:+.4f}, p={p:.4f}, [{ci_l:+.4f},{ci_u:+.4f}], Spearman={rho:+.4f}, n={n}")

# Per-period
for pn in ['Before Demo','Demo','After Demo']:
    sub = df[df['period']==pn]
    if len(sub) < 3: continue
    for xcol, ycol, label in [('net_sentiment_ratio','IHSG_return','IHSG'), ('net_sentiment_ratio','USDIDR_return','USD/IDR')]:
        r,p = stats.pearsonr(sub[xcol], sub[ycol])
        print(f"{label} [{pn}] n={len(sub)}: r={r:+.4f}, p={p:.4f}")

# ---- Markdown ----
md = os.path.join(script_dir, 'gpt5_diagnostics.md')
with open(md,'w',encoding='utf-8') as f:
    f.write("# GPT-5 Sentiment Diagnostics\n\n")
    f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
    f.write(f"**Observations:** {n} trading days (Aug 1 – Sep 30, 2025)\n\n")
    f.write("---\n\n## Normality\n\n")
    f.write("| Variable | N | SW p | JB p | DA p | Verdict |\n")
    f.write("|---|---|---|---|---|---|\n")
    for r in norm_rows: f.write(f"| {r['Variable']} | {r['N']} | {r['SW p']:.4f} | {r['JB p']:.4f} | {r['DA p']:.4f} | **{r['Verdict']}** |\n")

    f.write("\n## Correlations\n\n")
    f.write("| Pair | r | p | 95% CI | Spearman | n |\n")
    f.write("|---|---|---|---|---|---|\n")
    for xcol, ycol, label in [('net_sentiment_ratio','IHSG_return','IHSG'), ('net_sentiment_ratio','USDIDR_return','USD/IDR')]:
        x,y = df[xcol], df[ycol]; r,p=stats.pearsonr(x,y); rho,rp=stats.spearmanr(x,y)
        z=np.arctanh(r); se=1/np.sqrt(n-3); zc=stats.norm.ppf(0.975)
        f.write(f"| {label} | {r:+.4f} | {p:.4f} | [{np.tanh(z-zc*se):+.4f},{np.tanh(z+zc*se):+.4f}] | {rho:+.4f} | {n} |\n")

print(f"\nMarkdown -> {md}")
print("Done.")
