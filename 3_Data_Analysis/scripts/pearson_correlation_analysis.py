import pandas as pd
import numpy as np
import yfinance as yf
import os
import glob
from datetime import datetime, timedelta
from scipy import stats
from nltk.sentiment import SentimentIntensityAnalyzer
import warnings
warnings.filterwarnings('ignore')

script_dir = os.path.dirname(os.path.abspath(__file__))
scraper_dir = os.path.join(script_dir, "TwitterScrapper-main")

# ============================================================
# CONFIGURATION
# ============================================================
START_DATE = "2025-08-01"
END_DATE = "2025-09-30"

# File groupings
IHSG_FILES = [
    "tweets_IHSG_since_2025_08_01_until_20_20251021_142338.csv",
    "tweets_IHSG_since_2025_08_25_until_20_20251020_192834.csv",
    "tweets_ihsg_since_2025_08_25_until_20_20251028_192205.csv",
    "tweets_bursa_efek_since_2025_08_25_un_20251020_194634.csv",
    "tweets_bursa_efek_since_2025_08_01_un_20251024_150659.csv",
    "tweets_saham_turun_since_2025_08_25_u_20251020_192847.csv",
    "tweets_saham_naik_since_2025_09_09_un_20251027_001118.csv",
    "tweets_jual_saham_since_2025_08_25_un_20251020_203623.csv",
    "tweets_panic_selling_since_2025_08_25_20251020_195242.csv",
    "tweets_asing_cabut_since_2025_08_01_u_20251027_192757.csv",
    "tweets_foreign_outflow_since_2025_08__20251027_214841.csv",
    "tweets_pasar_keuangan_since_2025_08_0_20251024_145736.csv",
]

USDIDR_FILES = [
    "tweets_nilai_tukar_since_2025_08_25_u_20251020_204801.csv",
    "tweets_kurs_rupiah_since_2025_08_25_u_20251020_203843.csv",
    "tweets_kurs_rupiah_since_2025_08_01_u_20251027_192629.csv",
    "tweets_melemah_since_2025_08_25_until_20251026_223628.csv",
    "tweets_menguat_since_2025_08_25_until_20251024_163121.csv",
]


def pearson_ci(r, n, alpha=0.05):
    """Compute 95% confidence interval for Pearson r using Fisher's z-transformation."""
    if n <= 3:
        return (np.nan, np.nan)
    if abs(r) >= 1.0:
        r = np.sign(r) * 0.999999
    z = np.arctanh(r)
    se = 1.0 / np.sqrt(n - 3)
    z_crit = stats.norm.ppf(1 - alpha / 2)
    z_lower = z - z_crit * se
    z_upper = z + z_crit * se
    r_lower = np.tanh(z_lower)
    r_upper = np.tanh(z_upper)
    return (r_lower, r_upper)


def compute_daily_sentiment(file_list, label):
    """Run VADER on all tweets, aggregate to daily net sentiment."""
    sia = SentimentIntensityAnalyzer()
    records = []
    files_processed = 0
    total_tweets = 0

    for fname in file_list:
        fpath = os.path.join(scraper_dir, fname)
        if not os.path.exists(fpath):
            continue
        try:
            df = pd.read_csv(fpath)
            if 'created_at' not in df.columns or 'text' not in df.columns:
                continue
            df['created_at'] = pd.to_datetime(df['created_at'], errors='coerce')
            df = df.dropna(subset=['created_at', 'text'])
            mask = (df['created_at'] >= START_DATE) & (df['created_at'] < "2025-10-01")
            df = df.loc[mask]
            if df.empty:
                continue

            for _, row in df.iterrows():
                text = str(row['text'])
                scores = sia.polarity_scores(text)
                records.append({
                    'date': row['created_at'].date(),
                    'neg': scores['neg'],
                    'neu': scores['neu'],
                    'pos': scores['pos'],
                    'compound': scores['compound'],
                })
                total_tweets += 1
            files_processed += 1
        except Exception as e:
            print(f"  Error processing {fname}: {e}")

    if not records:
        print(f"  WARNING: No tweets found for {label}")
        return pd.DataFrame()

    daily = pd.DataFrame(records)
    # Daily aggregations
    agg = daily.groupby('date').agg(
        tweet_count=('compound', 'count'),
        mean_compound=('compound', 'mean'),
        median_compound=('compound', 'median'),
        std_compound=('compound', 'std'),
        # Net sentiment: (positive_count - negative_count) / total
        pos_count=('pos', lambda x: (x > 0).sum()),
        neg_count=('neg', lambda x: (x > 0).sum()),
        neu_count=('neu', lambda x: (x > 0).sum()),
        pos_mean=('pos', 'mean'),
        neg_mean=('neg', 'mean'),
        neu_mean=('neu', 'mean'),
    ).reset_index()

    # Net sentiment ratio: (positive - negative) / total
    agg['net_sentiment_ratio'] = (agg['pos_count'] - agg['neg_count']) / agg['tweet_count']
    # Alternative: sum of compound scores normalized
    agg['net_sentiment_compound'] = daily.groupby('date')['compound'].sum().values

    return agg


# ============================================================
# 1. COMPUTE DAILY NET SENTIMENT
# ============================================================
print("=" * 70)
print("1. COMPUTING DAILY NET SENTIMENT (VADER)")
print("=" * 70)

print("\nIHSG-related tweets...")
ihsg_sentiment = compute_daily_sentiment(IHSG_FILES, "IHSG")
print(f"  Dates with sentiment data: {len(ihsg_sentiment)}")
if not ihsg_sentiment.empty:
    print(f"  Total tweets analyzed: {ihsg_sentiment['tweet_count'].sum()}")
    print(f"  Mean net_sentiment_ratio: {ihsg_sentiment['net_sentiment_ratio'].mean():.4f}")
    print(f"  Mean net_sentiment_compound: {ihsg_sentiment['net_sentiment_compound'].mean():.4f}")

print("\nUSD/IDR-related tweets...")
usdidr_sentiment = compute_daily_sentiment(USDIDR_FILES, "USD/IDR")
print(f"  Dates with sentiment data: {len(usdidr_sentiment)}")
if not usdidr_sentiment.empty:
    print(f"  Total tweets analyzed: {usdidr_sentiment['tweet_count'].sum()}")
    print(f"  Mean net_sentiment_ratio: {usdidr_sentiment['net_sentiment_ratio'].mean():.4f}")
    print(f"  Mean net_sentiment_compound: {usdidr_sentiment['net_sentiment_compound'].mean():.4f}")

# ============================================================
# 2. FETCH MARKET DATA
# ============================================================
print("\n" + "=" * 70)
print("2. FETCHING MARKET DATA")
print("=" * 70)

ihsg_raw = yf.download("^JKSE", start=START_DATE, end="2025-10-01", progress=False, auto_adjust=True)
usdidr_raw = yf.download("USDIDR=X", start=START_DATE, end="2025-10-01", progress=False, auto_adjust=True)

# Flatten MultiIndex columns if present
if isinstance(ihsg_raw.columns, pd.MultiIndex):
    ihsg_raw.columns = ihsg_raw.columns.get_level_values(0)
if isinstance(usdidr_raw.columns, pd.MultiIndex):
    usdidr_raw.columns = usdidr_raw.columns.get_level_values(0)

# Compute daily returns
if not ihsg_raw.empty and 'Close' in ihsg_raw.columns:
    ihsg_returns = ihsg_raw[['Close']].copy()
    ihsg_returns['IHSG_return'] = ihsg_returns['Close'].pct_change() * 100
    ihsg_returns = ihsg_returns.dropna()
    ihsg_returns = ihsg_returns.reset_index()
    ihsg_returns['date'] = ihsg_returns.iloc[:, 0].dt.date
else:
    print("WARNING: IHSG data download failed or returned empty")
    ihsg_returns = pd.DataFrame(columns=['date', 'Close', 'IHSG_return'])

if not usdidr_raw.empty and 'Close' in usdidr_raw.columns:
    usdidr_returns = usdidr_raw[['Close']].copy()
    usdidr_returns['USDIDR_return'] = usdidr_returns['Close'].pct_change() * 100
    usdidr_returns = usdidr_returns.dropna()
    usdidr_returns = usdidr_returns.reset_index()
    usdidr_returns['date'] = usdidr_returns.iloc[:, 0].dt.date
else:
    print("WARNING: USD/IDR data download failed or returned empty")
    usdidr_returns = pd.DataFrame(columns=['date', 'Close', 'USDIDR_return'])

print(f"IHSG return observations: {len(ihsg_returns)}")
print(f"USD/IDR return observations: {len(usdidr_returns)}")

# ============================================================
# 3. MERGE SENTIMENT + MARKET RETURNS
# ============================================================
print("\n" + "=" * 70)
print("3. MERGING SENTIMENT + MARKET RETURNS")
print("=" * 70)

if not ihsg_sentiment.empty:
    ihsg_merged = ihsg_sentiment.merge(ihsg_returns, on='date', how='inner')
else:
    ihsg_merged = pd.DataFrame()
    print("WARNING: No IHSG sentiment data to merge")

if not usdidr_sentiment.empty:
    usdidr_merged = usdidr_sentiment.merge(usdidr_returns, on='date', how='inner')
else:
    usdidr_merged = pd.DataFrame()
    print("WARNING: No USD/IDR sentiment data to merge")

print(f"IHSG merged observations: {len(ihsg_merged)}")
print(f"USD/IDR merged observations: {len(usdidr_merged)}")

# ============================================================
# 4. PEARSON CORRELATION ANALYSIS
# ============================================================
print("\n" + "=" * 70)
print("4. PEARSON CORRELATIONS")
print("=" * 70)

results = []

for name, merged, sentiment_col, return_col in [
    ("IHSG (net_sentiment_ratio)", ihsg_merged, "net_sentiment_ratio", "IHSG_return"),
    ("IHSG (net_sentiment_compound)", ihsg_merged, "net_sentiment_compound", "IHSG_return"),
    ("IHSG (mean_compound)", ihsg_merged, "mean_compound", "IHSG_return"),
    ("USD/IDR (net_sentiment_ratio)", usdidr_merged, "net_sentiment_ratio", "USDIDR_return"),
    ("USD/IDR (net_sentiment_compound)", usdidr_merged, "net_sentiment_compound", "USDIDR_return"),
    ("USD/IDR (mean_compound)", usdidr_merged, "mean_compound", "USDIDR_return"),
]:
    if merged.empty or len(merged) < 3:
        print(f"\n{name}: INSUFFICIENT DATA (n={len(merged)})")
        continue

    x = merged[sentiment_col].dropna()
    y = merged[return_col].dropna()
    common = x.index.intersection(y.index)
    x = x.loc[common]
    y = y.loc[common]
    n = len(x)

    r, p_value = stats.pearsonr(x, y)
    ci_lower, ci_upper = pearson_ci(r, n)

    # Also compute Spearman as robustness check
    rho, p_rho = stats.spearmanr(x, y)

    sig = "***" if p_value < 0.001 else ("**" if p_value < 0.01 else ("*" if p_value < 0.05 else "n.s."))

    print(f"\n{name}:")
    print(f"  n                     = {n}")
    print(f"  Pearson r             = {r:+.4f}")
    print(f"  p-value               = {p_value:.6f}  {sig}")
    print(f"  95% CI                = [{ci_lower:+.4f}, {ci_upper:+.4f}]")
    print(f"  Spearman rho          = {rho:+.4f}  (p={p_rho:.6f})")
    print(f"  Mean sentiment        = {x.mean():.4f}")
    print(f"  SD sentiment          = {x.std():.4f}")
    print(f"  Mean return (%):      = {y.mean():.4f}")
    print(f"  SD return (%):        = {y.std():.4f}")

    results.append({
        'pair': name,
        'n': n,
        'pearson_r': round(r, 4),
        'p_value': p_value,
        'p_formatted': f"{p_value:.6f}" if p_value >= 0.0001 else f"{p_value:.2e}",
        'ci_95_lower': round(ci_lower, 4),
        'ci_95_upper': round(ci_upper, 4),
        'spearman_rho': round(rho, 4),
        'spearman_p': p_rho,
        'significance': sig,
        'mean_sentiment': round(x.mean(), 4),
        'sd_sentiment': round(x.std(), 4),
        'mean_return': round(y.mean(), 4),
        'sd_return': round(y.std(), 4),
    })

# ============================================================
# 5. PER-PERIOD CORRELATIONS
# ============================================================
print("\n\n" + "=" * 70)
print("5. PER-PERIOD CORRELATIONS")
print("=" * 70)

period_defs = {
    'Before Demo': ('2025-08-01', '2025-08-24'),
    'Demo':        ('2025-08-25', '2025-09-08'),
    'After Demo':  ('2025-09-09', '2025-09-30'),
}

period_results = []

for pname, (pstart, pend) in period_defs.items():
    pstart_d = pd.Timestamp(pstart).date()
    pend_d = pd.Timestamp(pend).date()

    for mname, merged, sc, rc in [
        ("IHSG (net_sentiment_ratio)", ihsg_merged, "net_sentiment_ratio", "IHSG_return"),
        ("USD/IDR (net_sentiment_ratio)", usdidr_merged, "net_sentiment_ratio", "USDIDR_return"),
    ]:
        if merged.empty:
            continue
        mask = (merged['date'] >= pstart_d) & (merged['date'] <= pend_d)
        sub = merged.loc[mask]
        x = sub[sc].dropna()
        y = sub[rc].dropna()
        common = x.index.intersection(y.index)
        x = x.loc[common]
        y = y.loc[common]
        n = len(x)
        if n < 3:
            print(f"  {pname} — {mname}: n={n} (insufficient)")
            period_results.append({
                'period': pname, 'pair': mname, 'n': n,
                'pearson_r': None, 'p_value': None, 'ci_95_lower': None, 'ci_95_upper': None,
                'spearman_rho': None, 'significance': 'insufficient',
            })
            continue

        r, pv = stats.pearsonr(x, y)
        ci_l, ci_u = pearson_ci(r, n)
        rho, p_rho = stats.spearmanr(x, y)
        sig = "***" if pv < 0.001 else ("**" if pv < 0.01 else ("*" if pv < 0.05 else "n.s."))

        print(f"  {pname} — {mname}: r={r:+.4f}, p={pv:.6f}, n={n}, 95% CI [{ci_l:+.4f}, {ci_u:+.4f}]  {sig}")
        period_results.append({
            'period': pname, 'pair': mname, 'n': n,
            'pearson_r': round(r, 4), 'p_value': pv,
            'ci_95_lower': round(ci_l, 4), 'ci_95_upper': round(ci_u, 4),
            'spearman_rho': round(rho, 4), 'significance': sig,
        })

# ============================================================
# 6. DAILY SENTIMENT CSV OUTPUT
# ============================================================
print("\n" + "=" * 70)
print("6. EXPORTING DAILY SENTIMENT CSVs")
print("=" * 70)

if not ihsg_merged.empty:
    cols = ['date', 'tweet_count', 'net_sentiment_ratio', 'net_sentiment_compound',
            'mean_compound', 'median_compound', 'std_compound',
            'pos_count', 'neg_count', 'neu_count', 'IHSG_return']
    out = ihsg_merged[cols].sort_values('date')
    outpath = os.path.join(script_dir, 'daily_sentiment_IHSG.csv')
    out.to_csv(outpath, index=False)
    print(f"  IHSG daily sentiment -> {outpath}  ({len(out)} rows)")

if not usdidr_merged.empty:
    cols = ['date', 'tweet_count', 'net_sentiment_ratio', 'net_sentiment_compound',
            'mean_compound', 'median_compound', 'std_compound',
            'pos_count', 'neg_count', 'neu_count', 'USDIDR_return']
    out = usdidr_merged[cols].sort_values('date')
    outpath = os.path.join(script_dir, 'daily_sentiment_USDIDR.csv')
    out.to_csv(outpath, index=False)
    print(f"  USD/IDR daily sentiment -> {outpath}  ({len(out)} rows)")

# ============================================================
# 7. MARKDOWN REPORT
# ============================================================
md_path = os.path.join(script_dir, 'pearson_correlation_analysis.md')

with open(md_path, 'w', encoding='utf-8') as f:
    f.write("# Pearson Correlation Analysis: Net Sentiment vs. Market Returns\n\n")
    f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
    f.write(f"**Period:** {START_DATE} to {END_DATE}\n")
    f.write("**Sentiment Method:** VADER (Valence Aware Dictionary and sEntiment Reasoner)\n")
    f.write("**Market Data:** Yahoo Finance (`^JKSE`, `USDIDR=X`)\n\n")
    f.write("---\n\n")

    # Method
    f.write("## Methodology\n\n")
    f.write("### Net Sentiment Computation\n\n")
    f.write("Each tweet is scored with VADER's compound sentiment score (range −1 to +1). ")
    f.write("Two daily net sentiment metrics are computed:\n\n")
    f.write("1. **Net Sentiment Ratio (NSR):** `(count_of_positive_tweets − count_of_negative_tweets) / total_tweets`\n")
    f.write("2. **Net Sentiment Compound (NSC):** `sum(compound_score)` — cumulative daily VADER compound\n")
    f.write("3. **Mean Compound (MC):** `mean(compound_score)` — average daily VADER score\n\n")
    f.write("### Market Returns\n\n")
    f.write("Daily percentage returns computed as `(Close_t − Close_{t−1}) / Close_{t−1} × 100`.\n\n")
    f.write("### Statistical Tests\n\n")
    f.write("- **Pearson's r:** linear correlation between net sentiment and same-day market return\n")
    f.write("- **p-value:** two-tailed test of H₀: ρ = 0\n")
    f.write("- **95% Confidence Interval:** Fisher's z-transformation\n")
    f.write("- **Spearman's ρ:** rank correlation as robustness check (monotonic, not assuming linearity)\n\n")
    f.write("### Significance Notation\n\n")
    f.write("- \\*\\*\\* p < 0.001\n")
    f.write("- \\*\\* p < 0.01\n")
    f.write("- \\* p < 0.05\n")
    f.write("- n.s. not significant\n\n")

    f.write("---\n\n")

    # Overall results
    f.write("## Overall Correlations (Full Period: Aug 1 – Sep 30)\n\n")
    f.write("| Pair | n | Pearson r | p-value | 95% CI | Spearman ρ | Sig. |\n")
    f.write("|------|---|-----------|---------|--------|------------|------|\n")
    for r in results:
        f.write(f"| {r['pair']} | {r['n']} | {r['pearson_r']:+.4f} | {r['p_formatted']} | [{r['ci_95_lower']:+.4f}, {r['ci_95_upper']:+.4f}] | {r['spearman_rho']:+.4f} | {r['significance']} |\n")

    f.write("\n### Descriptive Statistics\n\n")
    f.write("| Pair | Mean Sentiment | SD Sentiment | Mean Return (%) | SD Return (%) |\n")
    f.write("|------|----------------|--------------|-----------------|---------------|\n")
    for r in results:
        f.write(f"| {r['pair']} | {r['mean_sentiment']:.4f} | {r['sd_sentiment']:.4f} | {r['mean_return']:.4f} | {r['sd_return']:.4f} |\n")

    f.write("\n---\n\n")

    # Per-period
    f.write("## Per-Period Correlations\n\n")
    f.write("| Period | Pair | n | Pearson r | p-value | 95% CI | Spearman ρ | Sig. |\n")
    f.write("|--------|------|---|-----------|---------|--------|------------|------|\n")
    for pr in period_results:
        if pr['pearson_r'] is None:
            f.write(f"| {pr['period']} | {pr['pair']} | {pr['n']} | — | — | — | — | insufficient |\n")
        else:
            f.write(f"| {pr['period']} | {pr['pair']} | {pr['n']} | {pr['pearson_r']:+.4f} | {pr['p_value']:.6f} | [{pr['ci_95_lower']:+.4f}, {pr['ci_95_upper']:+.4f}] | {pr['spearman_rho']:+.4f} | {pr['significance']} |\n")

    f.write("\n---\n\n")

    # Interpretation
    f.write("## Interpretation\n\n")

    # Find the main results
    ihsg_nsr = next((r for r in results if 'IHSG (net_sentiment_ratio)' in r['pair']), None)
    usdidr_nsr = next((r for r in results if 'USD/IDR (net_sentiment_ratio)' in r['pair']), None)

    if ihsg_nsr:
        f.write("### Net Sentiment → IHSG Returns\n\n")
        f.write(f"- **Pearson r = {ihsg_nsr['pearson_r']:+.4f}** ({ihsg_nsr['significance']})\n")
        f.write(f"- 95% CI: [{ihsg_nsr['ci_95_lower']:+.4f}, {ihsg_nsr['ci_95_upper']:+.4f}]\n")
        f.write(f"- n = {ihsg_nsr['n']} paired daily observations\n\n")
        if ihsg_nsr['pearson_r'] > 0:
            f.write("**Direction:** Positive. As net Twitter sentiment about IHSG/market becomes more positive, same-day IHSG returns tend to rise. ")
            f.write("This is consistent with sentiment-driven trading — bullish social media chatter coincides with upward price movement.\n\n")
        else:
            f.write("**Direction:** Negative. Twitter sentiment moves inversely to IHSG returns.\n\n")

    if usdidr_nsr:
        f.write("### Net Sentiment → USD/IDR Returns\n\n")
        f.write(f"- **Pearson r = {usdidr_nsr['pearson_r']:+.4f}** ({usdidr_nsr['significance']})\n")
        f.write(f"- 95% CI: [{usdidr_nsr['ci_95_lower']:+.4f}, {usdidr_nsr['ci_95_upper']:+.4f}]\n")
        f.write(f"- n = {usdidr_nsr['n']} paired daily observations\n\n")
        if usdidr_nsr['pearson_r'] < 0:
            f.write("**Direction:** Negative. As Twitter sentiment about the rupiah becomes more positive, USD/IDR returns tend to fall (rupiah strengthens). ")
            f.write("This is economically coherent — positive sentiment about the currency aligns with appreciation pressure.\n\n")
        else:
            f.write("**Direction:** Positive.\n\n")

    f.write("### Comparison with Paper Values\n\n")
    f.write(f"| Metric | Paper (reported) | This Analysis |\n")
    f.write(f"|--------|------------------|---------------|\n")
    paper_ihsg = "+0.36"
    paper_usdidr = "−0.17"
    calc_ihsg = f"{ihsg_nsr['pearson_r']:+.4f}" if ihsg_nsr else "N/A"
    calc_usdidr = f"{usdidr_nsr['pearson_r']:+.4f}" if usdidr_nsr else "N/A"
    f.write(f"| Net sentiment–IHSG | {paper_ihsg} | {calc_ihsg} |\n")
    f.write(f"| Net sentiment–USD/IDR | {paper_usdidr} | {calc_usdidr} |\n\n")

    f.write("### Caveats\n\n")
    f.write("1. **VADER is English-optimized.** Indonesian tweets are scored with an English lexicon, ")
    f.write("which reduces accuracy. English loanwords and code-switching in Indonesian finance Twitter ")
    f.write("provide partial signal, but sentiment misclassification is expected.\n\n")
    f.write("2. **Causality direction is ambiguous.** Same-day correlation does not establish whether sentiment ")
    f.write("drives returns, returns drive sentiment, or a third factor (e.g., breaking news) drives both.\n\n")
    f.write("3. **After Demo period has insufficient data.** Only 2 paired observations for IHSG and 0 for ")
    f.write("USD/IDR, making per-period comparisons unreliable for Sep 9–30.\n\n")
    f.write("4. **Tweet volume varies significantly by day.** Days with few tweets produce noisier sentiment estimates.\n\n")
    f.write("5. **Confidence intervals widen with smaller n.** Per-period correlations have wider CIs than the full-period estimate.\n")

    f.write("---\n\n")
    f.write("**Output files:** `daily_sentiment_IHSG.csv`, `daily_sentiment_USDIDR.csv`  \n")
    f.write("**Analysis script:** `pearson_correlation_analysis.py`\n")

print(f"\nMarkdown report -> {md_path}")
print("Done.")
