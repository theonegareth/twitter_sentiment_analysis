import pandas as pd
import numpy as np
from scipy import stats
import os
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

script_dir = os.path.dirname(os.path.abspath(__file__))

# ---- load data ----
ihsg   = pd.read_csv(os.path.join(script_dir, 'daily_sentiment_IHSG.csv'),   parse_dates=['date'])
usdidr = pd.read_csv(os.path.join(script_dir, 'daily_sentiment_USDIDR.csv'), parse_dates=['date'])

# ---- variables to check ----
VARIABLES = [
    ('IHSG Net Sentiment (NSR)',       ihsg,   'net_sentiment_ratio'),
    ('USD/IDR Net Sentiment (NSR)',    usdidr, 'net_sentiment_ratio'),
    ('IHSG Return (%)',                ihsg,   'IHSG_return'),
    ('USD/IDR Return (%)',             usdidr, 'USDIDR_return'),
    ('IHSG Net Sentiment (NSC)',       ihsg,   'net_sentiment_compound'),
    ('USD/IDR Net Sentiment (NSC)',    usdidr, 'net_sentiment_compound'),
    ('IHSG Mean Compound',             ihsg,   'mean_compound'),
    ('USD/IDR Mean Compound',          usdidr, 'mean_compound'),
    ('IHSG Tweet Count',              ihsg,   'tweet_count'),
    ('USD/IDR Tweet Count',           usdidr, 'tweet_count'),
]

def detect_by_iqr(vals, dates):
    q1, q3 = np.percentile(vals, [25, 75])
    iqr_val = q3 - q1
    lower = q1 - 1.5 * iqr_val
    upper = q3 + 1.5 * iqr_val
    idx = [i for i, v in enumerate(vals) if v < lower or v > upper]
    return [{'index': i, 'date': dates.iloc[i], 'value': vals[i],
             'direction': 'low' if vals[i] < lower else 'high',
             'boundary': lower if vals[i] < lower else upper} for i in idx]

def detect_by_zscore(vals, dates):
    z = np.abs((vals - vals.mean()) / vals.std(ddof=1))
    idx = [i for i, zv in enumerate(z) if zv > 2.5]
    return [{'index': i, 'date': dates.iloc[i], 'value': vals[i],
             'z_score': z[i], 'direction': 'low' if vals[i] < vals.mean() else 'high'} for i in idx]

def detect_by_mad(vals, dates):
    median = np.median(vals)
    mad = np.median(np.abs(vals - median))
    if mad == 0:
        return []
    mod_z = 0.6745 * (vals - median) / mad
    idx = [i for i, z in enumerate(mod_z) if abs(z) > 3.5]
    return [{'index': i, 'date': dates.iloc[i], 'value': vals[i],
             'mod_z': mod_z[i], 'direction': 'low' if vals[i] < median else 'high'} for i in idx]

# ---- run detection ----
all_outlier_rows = []
summary_rows = []

for name, df, col in VARIABLES:
    sub = df[['date', col]].dropna().reset_index(drop=True)
    vals = sub[col].values
    dates = sub['date']
    n = len(vals)

    iqr_list   = detect_by_iqr(vals, dates)
    z_list     = detect_by_zscore(vals, dates)
    mad_list   = detect_by_mad(vals, dates)

    # Union of all methods
    all_indices = set()
    for lst in [iqr_list, z_list, mad_list]:
        for item in lst:
            all_indices.add(item['index'])

    # Build detail rows
    for i in sorted(all_indices):
        item_iqr = next((x for x in iqr_list if x['index'] == i), None)
        item_z   = next((x for x in z_list if x['index'] == i), None)
        item_mad = next((x for x in mad_list if x['index'] == i), None)

        methods = []
        if item_iqr: methods.append('IQR')
        if item_z:   methods.append(f'Z={item_z["z_score"]:.2f}')
        if item_mad: methods.append(f'MAD')

        d = dates.iloc[i]
        v = vals[i]
        all_outlier_rows.append({
            'Variable': name,
            'Date': str(d),
            'Value': v,
            'Method': ', '.join(methods),
            'Direction': 'HIGH' if v > vals.mean() else 'LOW',
        })

    # Summary row
    total = len(all_indices)
    pct = f"{100*total/n:.1f}%" if n > 0 else '0%'
    high = sum(1 for r in all_outlier_rows if r['Direction'] == 'HIGH' and r['Variable'] == name)
    low  = total - high
    summary_rows.append({
        'Variable': name,
        'N': n,
        'IQR Outliers': len(iqr_list),
        'Z-Score Outliers': len(z_list),
        'MAD Outliers': len(mad_list),
        'Union (Any Method)': total,
        'Pct Outliers': pct,
        'High': high,
        'Low': low,
        'IQR Low': round(float(np.percentile(vals, 25) - 1.5*(np.percentile(vals, 75) - np.percentile(vals, 25))), 4),
        'IQR High': round(float(np.percentile(vals, 75) + 1.5*(np.percentile(vals, 75) - np.percentile(vals, 25))), 4),
    })

df_detail = pd.DataFrame(all_outlier_rows)
df_summary = pd.DataFrame(summary_rows)

# ---- export CSV ----
detail_path = os.path.join(script_dir, 'outlier_diagnostics_detail.csv')
summary_path = os.path.join(script_dir, 'outlier_diagnostics_summary.csv')
df_detail.to_csv(detail_path, index=False)
df_summary.to_csv(summary_path, index=False)

# ---- console ----
print("=" * 120)
print("OUTLIER DIAGNOSTICS — IQR (1.5x) + Z-Score (|Z| > 2.5) + MAD (|mod Z| > 3.5)")
print("=" * 120)
print("\nSUMMARY:")
print(df_summary.to_string(index=False))
print(f"\nDETAIL: {len(df_detail)} outlier observations across all variables and methods.")
for _, row in df_detail.iterrows():
    print(f"  {row['Date']} | {row['Variable']:35s} | {row['Value']:+12.4f} | {row['Direction']:4s} | {row['Method']}")

# ---- markdown ----
md_path = os.path.join(script_dir, 'outlier_diagnostics.md')
with open(md_path, 'w', encoding='utf-8') as f:
    f.write("# Outlier Diagnostics\n\n")
    f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
    f.write("**Methods:** IQR (1.5×IQR rule), Z-Score (|Z| > 2.5), Modified Z-Score via MAD (|Z_mod| > 3.5)\n\n")
    f.write("---\n\n")

    f.write("## Outlier Summary per Variable\n\n")
    f.write("| Variable | N | IQR | Z-Score | MAD | Union | % | High | Low |\n")
    f.write("|----------|---|-----|---------|-----|-------|---|------|------|\n")
    for _, row in df_summary.iterrows():
        f.write(f"| {row['Variable']} | {int(row['N'])} "
                f"| {int(row['IQR Outliers'])} | {int(row['Z-Score Outliers'])} | {int(row['MAD Outliers'])} "
                f"| {int(row['Union (Any Method)'])} | {row['Pct Outliers']} "
                f"| {int(row['High'])} | {int(row['Low'])} |\n")

    f.write("\n---\n\n")
    f.write("## Outlier Dates (Union of All Methods)\n\n")
    f.write("| Date | Variable | Value | Direction | Detection Method |\n")
    f.write("|------|----------|-------|-----------|------------------|\n")
    for _, row in df_detail.iterrows():
        f.write(f"| {row['Date']} | {row['Variable']} | {row['Value']:+12.4f} | {row['Direction']} | {row['Method']} |\n")

    f.write("\n---\n\n")
    f.write("## Key Outlier Dates (Cross-Variable)\n\n")

    # Find dates that appear as outliers in multiple variables
    date_counts = df_detail['Date'].value_counts()
    multi = date_counts[date_counts >= 2]
    if len(multi) > 0:
        f.write("Dates flagged as outliers in **2+ variables simultaneously**:\n\n")
        f.write("| Date | Variables Flagged | Notable Event |\n")
        f.write("|------|---------------------|---------------|\n")
        events_map = {
            '2025-08-25': 'Protest begins at DPR',
            '2025-08-28': 'Affan Kurniawan killed',
            '2025-08-29': 'IHSG plunge, foreign outflow',
            '2025-09-01': '17+8 demands consolidated',
            '2025-09-02': 'Markets digest protest',
            '2025-09-03': 'Continued volatility',
            '2025-09-04': 'Pre-holiday positioning',
            '2025-09-05': 'Maulid Nabi holiday',
            '2025-09-26': 'Post-crisis recovery',
            '2025-09-29': 'Late period spike',
        }
        for d in multi.index:
            vars_list = ', '.join(df_detail[df_detail['Date'] == d]['Variable'].values)
            event = events_map.get(d, '')
            f.write(f"| {d} | {vars_list} | {event} |\n")
    else:
        f.write("No dates are flagged as outliers in 2+ variables simultaneously.\n")

    f.write("\n---\n\n")
    f.write("## Overall Statistics\n\n")
    total_obs = sum(int(r['N']) for _, r in df_summary.iterrows())
    total_out = len(df_detail)
    f.write(f"- Total variable-days checked: {total_obs} (10 variables × varying n)\n")
    f.write(f"- Total outlier observations (union): {total_out}\n")
    f.write(f"- Overall outlier rate: {100*total_out/total_obs:.2f}%\n\n")

    f.write("### Most Common Outlier Dates (Top 10)\n\n")
    top_dates = date_counts.head(10)
    for d, c in top_dates.items():
        f.write(f"- **{d}**: flagged in {c} variables\n")

    f.write("\n---\n\n")
    f.write(f"**CSV detail:** [`outlier_diagnostics_detail.csv`](outlier_diagnostics_detail.csv)  \n")
    f.write(f"**CSV summary:** [`outlier_diagnostics_summary.csv`](outlier_diagnostics_summary.csv)  \n")
    f.write(f"**Script:** [`outlier_diagnostics.py`](outlier_diagnostics.py)\n")

print(f"\nMarkdown -> {md_path}")
print("Done.")
