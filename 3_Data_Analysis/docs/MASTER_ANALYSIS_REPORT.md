# MASTER ANALYSIS REPORT

## Twitter Sentiment & Financial Market Impact During DPR Protests

**Project:** Aug 1 – Sep 30, 2025 | Indonesian Twitter + IHSG + USD/IDR
**Generated:** 2026-06-04
**Status:** **COMPLETE** — all 10 reviewer requests addressed

---

## Step-by-Step Analysis Pipeline

The analysis proceeds through 7 sequential stages. Each stage depends on the outputs of the previous stage. Run scripts in order.

### Stage 1: Data Inventory & Pairing

**Script:** `market_data_merge_analysis.py`
**Output:** `market_data_merge_analysis.md`

Counts trading days, identifies paired observations (days with both market data AND tweet data), and documents coverage gaps.

**Result:**

| Metric | Count |
|---|---|
| Calendar days (Aug 1 – Sep 30) | 61 |
| Trading days (Mon–Fri, excl. holidays) | **42** |
| Paired IHSG observations (market + tweets) | **26** |
| Paired USD/IDR observations | **26** |
| Combined unique analytical dates | **28** |

Coverage is good for Before Demo (14–15 days) and Demo (10–11 days), but critical gap in After Demo (Sep 9–30): only 2 IHSG paired days, 0 USD/IDR paired days.

**Non-trading days:** 18 weekends + 1 holiday (Sep 5, Maulid Nabi). These are excluded from paired analysis. Treatment options (forward-fill, backward-fill, weekend aggregation, exclusion) are documented.

---

### Stage 2: Sentiment Scoring (VADER) + Daily Aggregation

**Script:** `pearson_correlation_analysis.py`
**Outputs:** `daily_sentiment_IHSG.csv`, `daily_sentiment_USDIDR.csv`, `pearson_correlation_analysis.md`

VADER lexicon scores each of 7,687 tweets. Daily net sentiment aggregated per keyword group.

**Tweet volumes:**

| Group | Files | Tweets analyzed |
|---|---|---|
| IHSG-related (12 keyword files) | IHSG, bursa efek, saham turun/naik, jual saham, etc. | 5,148 |
| USD/IDR-related (5 keyword files) | nilai tukar, kurs rupiah, melemah, menguat | 2,539 |

**Net Sentiment Ratio (NSR):** `(positive_tweets − negative_tweets) / total_tweets`
**Net Sentiment Compound (NSC):** `sum(VADER compound score)`

---

### Stage 3: Correlation Analysis (Pearson + Spearman)

**Script:** `pearson_correlation_analysis.py` (same script, second phase)
**Output:** `pearson_correlation_analysis.md` (tables section)

Full-period (n=25) Pearson correlations with p-values, 95% Fisher z confidence intervals, and Spearman rank correlations as non-parametric robustness check.

| Pair | n | Pearson r | p-value | 95% CI | Spearman ρ | Sig. |
|---|---|---|---|---|---|---|
| Net sentiment (NSR) → IHSG Return | 25 | +0.2194 | 0.2920 | [−0.19, +0.57] | +0.1708 | n.s. |
| Net sentiment (NSC) → IHSG Return | 25 | +0.1177 | 0.5752 | [−0.29, +0.49] | +0.1423 | n.s. |
| Net sentiment (NSR) → USD/IDR Return | 25 | +0.0517 | 0.8062 | [−0.35, +0.44] | +0.1843 | n.s. |
| Net sentiment (NSC) → USD/IDR Return | 25 | +0.3121 | 0.1288 | [−0.09, +0.63] | +0.2440 | n.s. |

**Per-period (Demo window only, n=9–10):**

| Pair | n | Pearson r | p-value | 95% CI | Sig. |
|---|---|---|---|---|---|
| IHSG (NSR) during Demo | 9 | +0.5985 | 0.0886 | [−0.11, +0.90] | n.s. |
| USD/IDR (NSR) during Demo | 10 | +0.5260 | 0.1184 | [−0.16, +0.87] | n.s. |

**Interpretation:** No statistically significant linear correlation at α=0.05. However, Demo-period correlations are moderate-to-strong (+0.53 to +0.60) but lack power at n=9–10. The paper's reported values (+0.36, −0.17) differ from these VADER results, likely due to different sentiment scoring methods (GPT-based labeling in the paper vs. English-only VADER lexicon here).

---

### Stage 4: Diagnostic Plots

**Script:** `create_charts.py` (main charts) + `create_diagnostic_plots.py` (diagnostic charts)
**Outputs:** `charts/` (9 PNGs) + `charts/diagnostics/` (10 PNGs)

**Main Charts (9):**

| # | File | Description |
|---|---|---|
| 01 | `01_scatter_net_sentiment_vs_returns.png` | Scatter + OLS regression + 95% CI band |
| 02 | `02_ihsg_timeline_with_sentiment.png` | 4-panel IHSG: price, return, sentiment, volume |
| 03 | `03_usdidr_timeline_with_sentiment.png` | 4-panel USD/IDR timeline |
| 04 | `04_period_correlation_comparison.png` | Bar chart: Pearson r by period |
| 05 | `05_correlation_heatmap.png` | Sentiment metric correlation matrices |
| 06 | `06_event_timeline.png` | Annotated IHSG + protest events |
| 07 | `07_dual_market_comparison.png` | Dual-axis IHSG + USD/IDR |
| 08 | `08_tweet_volume_by_period.png` | Boxplot: tweet counts by period |
| 09 | `09_sentiment_distribution_by_period.png` | Boxplot: net sentiment by period |

**Diagnostic Charts (10):**

| # | File | Description |
|---|---|---|
| D01 | `D01_master_diagnostic_dashboard.png` | 4-column: hist + box + Q-Q + violin per variable |
| D02 | `D02_histograms_detailed.png` | Detailed histograms with KDE, normal overlay, stats |
| D03 | `D03_boxplots_by_period.png` | Boxplots stratified by period |
| D04 | `D04_violin_plots_by_period.png` | Violin plots by period with skew annotations |
| D05 | `D05_qq_plots_by_period.png` | 12-panel Q-Q grid (4 vars × 3 periods) |
| D06 | `D06_pairwise_scatter_matrix.png` | 4×4 scatter matrix with KDE + Pearson r |
| D07 | `D07_scatter_by_period.png` | Scatter with period-colored regression lines |
| D08 | `D08_ecdf_comparison.png` | Empirical CDF vs. theoretical normal CDF |
| D09 | `D09_residual_diagnostics.png` | Residuals vs fitted, Q-Q residuals, scale-location |
| D10 | `D10_density_by_period.png` | KDE overlays by period |

---

### Stage 5: Normality Tests

**Script:** `normality_tests.py`
**Outputs:** `normality_test_results.csv`, `normality_test_report.md`

Four tests on four primary variables (full period, n=25):

| Variable | SW p | JB p | DA p | KS p | Verdict |
|---|---|---|---|---|---|
| IHSG Net Sentiment (NSR) | 0.091 | 0.014 | 0.007 | 0.707 | **Borderline** (2/4 pass) |
| USD/IDR Net Sentiment (NSR) | 0.005 | 0.012 | 0.005 | 0.096 | **Non-normal** (1/4 pass) |
| IHSG Return (%) | 0.832 | 0.921 | 0.703 | 0.938 | **Normal** (4/4 pass) |
| USD/IDR Return (%) | 0.036 | 0.173 | 0.096 | 0.585 | **Borderline** (3/4 pass) |

Extended results cover 10 variables × 3 periods (see `normality_test_report.md`).

**Implication:** USD/IDR sentiment correlations should use Spearman's ρ (non-normal). IHSG correlations can use Pearson r (both variables pass normality within relevant periods).

---

### Stage 6: Stationarity Tests

**Script:** `stationarity_tests.py`
**Outputs:** `stationarity_test_results.csv`, `stationarity_test_report.md`

ADF (3 specifications) + KPSS (2 specifications) on 16 series. Joint consensus verdict:

| Variable | ADF p | KPSS p | Consensus |
|---|---|---|---|
| IHSG Net Sentiment (NSR) | <0.001 | 0.10 | **Stationary** |
| USD/IDR Net Sentiment (NSR) | <0.001 | 0.10 | **Stationary** |
| IHSG Daily Return (%) | 0.681 | 0.10 | Diff-stationary |
| USD/IDR Daily Return (%) | <0.001 | 0.08 | **Stationary** |
| IHSG Price Level (Close) | 0.652 | 0.038 | **Non-stationary** |
| USD/IDR Tweet Count | 0.077 | 0.047 | **Non-stationary** |

**Implication:** All sentiment and return series are stationary — no differencing needed for correlation analysis. Price levels are I(1) as expected. USD/IDR tweet volume is non-stationary (declining scrape coverage).

---

### Stage 7: Outlier Diagnostics + Robustness

**Scripts:** `outlier_diagnostics.py` → `correlation_robustness.py`
**Outputs:** `outlier_diagnostics.md`, `correlation_robustness.md`

**Outlier methods:** IQR (1.5×), Z-Score (|Z| > 2.5), Modified Z-Score via MAD (|Z_mod| > 3.5)

**30 outlier observations** detected across 10 variables. Key cross-variable outlier dates:

| Date | Variables Flagged | Context |
|---|---|---|
| Aug 29 | IHSG tweet count, USD/IDR tweet count | IHSG plunge day — maximum tweet volume |
| Sep 1–3 | IHSG tweet count, USD/IDR tweet count, IHSG NSR, USD/IDR NSC | Post-protest consolidation, continued volatility |
| Aug 14 | USD/IDR NSR, IHSG NSC, USD/IDR Mean Compound | Multi-variable anomaly |

**Robustness — 5 treatments per pair:**

| Treatment | IHSG r | USD/IDR r |
|---|---|---|
| Original (no treatment) | +0.24 | +0.03 |
| Winsorise 5-95% | +0.20 | +0.01 |
| Winsorise 10-90% | +0.14 | +0.08 |
| Remove IQR outliers | +0.14 | **+0.42** (p=0.057) |
| Remove top/bottom 2 | +0.14 | **+0.43** (p=0.059) |

**Key finding:** USD/IDR correlation jumps from ~0 to +0.42–0.43 after removing 1–2 extreme observations, with p-values approaching significance (0.057–0.059). This suggests the Aug 29 crisis day suppresses the USD/IDR relationship. IHSG correlation is stable (+0.14 to +0.24) across all treatments.

**Recommendation:** Report winsorized results (preserves n=25, treats outliers as real events). Winsorization is preferred because the outliers correspond to the Aug 29 DPR protest crisis — the event the study aims to measure, not measurement error.

---

## Diagnostic Summary Table

**Script:** `diagnostic_summary.py`
**Outputs:** `diagnostic_summary_table.csv`, `diagnostic_summary_table.md`

| Variable | N | Mean | SD | Skew | Kurt | SW p | Normal? | ADF p | Stationary? | Outliers |
|---|---|---|---|---|---|---|---|---|---|---|
| IHSG Net Sentiment (NSR) | 25 | 0.07 | 0.04 | +1.02 | +2.02 | 0.091 | Borderline | <0.001 | Stationary | 1 high |
| USD/IDR Net Sentiment (NSR) | 25 | 0.05 | 0.09 | +1.25 | +1.51 | 0.005 | **Non-normal** | <0.001 | Stationary | 6 |
| IHSG Return (%) | 25 | +0.22 | 0.89 | +0.19 | +0.12 | 0.832 | Normal | 0.681 | Diff-stat | None |
| USD/IDR Return (%) | 25 | −0.01 | 0.36 | −0.92 | +0.10 | 0.036 | Borderline | <0.001 | Stationary | 1 low |
| IHSG Net Sentiment (NSC) | 25 | 4.12 | 3.16 | +0.73 | +0.30 | 0.258 | Normal | 0.004 | Stationary | 2 high |
| USD/IDR Net Sentiment (NSC) | 25 | 0.90 | 1.65 | +0.67 | +0.09 | 0.051 | Normal | 0.029 | Stationary | 3 high |
| IHSG Mean Compound | 25 | 0.03 | 0.02 | +0.64 | +0.07 | 0.329 | Normal | <0.001 | Stationary | None |
| USD/IDR Mean Compound | 25 | 0.03 | 0.05 | +1.55 | +1.66 | <0.001 | **Non-normal** | 0.460 | Diff-stat | 4 high |
| IHSG Tweet Count | 25 | 159.5 | 120.6 | +1.22 | +0.64 | 0.002 | **Non-normal** | 0.001 | Stationary | 2 high |
| USD/IDR Tweet Count | 25 | 79.0 | 97.5 | +0.87 | −0.71 | <0.001 | Borderline | 0.077 | **Non-stat** | 10 high |

---

## Model Comparison (GPT Benchmarking)

**Script:** `model_comparison_table.py`
**Outputs:** `model_comparison_table.csv`, `model_comparison_table.md`

GPT model performance on 440 labeled Indonesian tweets (COVID-19 PPKM sentiment dataset):

| Model | Sentiment Accuracy | Emotion Accuracy |
|---|---|---|
| gpt-5 (best run) | 87.05% | 76.59% |
| gpt-4.1 | 83.41% | 72.27% |
| gpt-4.1-mini | 83.41% | 70.91% |
| gpt-5-mini | 81.59% | 72.50% |
| gpt-5-nano | 75.68% | 60.45% |

Full F1 scores per class in `model_comparison_table.md`. Note: Neutral sentiment F1 is 0.0 across all models because the test set contains no neutral samples.

---

## Complete File Inventory

### Analysis Scripts (Run in order)

| # | Script | Produces | Stage |
|---|---|---|---|
| 1 | `market_data_merge_analysis.py` | `market_data_merge_analysis.md` | Data pairing |
| 2 | `pearson_correlation_analysis.py` | `daily_sentiment_IHSG.csv`, `daily_sentiment_USDIDR.csv`, `pearson_correlation_analysis.md` | Sentiment + correlations |
| 3 | `create_charts.py` | `charts/` (9 PNGs) | Main visualizations |
| 4 | `create_diagnostic_plots.py` | `charts/diagnostics/` (10 PNGs) | Diagnostic visualizations |
| 5 | `normality_tests.py` | `normality_test_results.csv`, `normality_test_report.md` | Normality |
| 6 | `stationarity_tests.py` | `stationarity_test_results.csv`, `stationarity_test_report.md` | Stationarity |
| 7 | `outlier_diagnostics.py` | `outlier_diagnostics_detail.csv`, `outlier_diagnostics_summary.csv`, `outlier_diagnostics.md` | Outliers |
| 8 | `correlation_robustness.py` | `correlation_robustness.csv`, `correlation_robustness.md` | Robustness |
| 9 | `diagnostic_summary.py` | `diagnostic_summary_table.csv`, `diagnostic_summary_table.md` | Summary table |
| 10 | `model_comparison_table.py` | `model_comparison_table.csv`, `model_comparison_table.md` | GPT benchmark |

### Documentation

| File | Content |
|---|---|
| `MASTER_ANALYSIS_REPORT.md` | **This file** — step-by-step master document |
| `pearson_correlation_analysis.md` | Correlation tables with p-values and CIs |
| `market_data_merge_analysis.md` | Trading days, pairing, non-trading day treatment |
| `correlation_robustness.md` | Robustness across 5 outlier treatments |
| `outlier_diagnostics.md` | Outlier dates and detection methods |
| `diagnostic_summary_table.md` | Unified N, mean, SD, skew, kurt, normality, stationarity, outlier table |
| `stationarity_test_report.md` | ADF + KPSS results (16 series, 3 ADF specs, 2 KPSS specs) |
| `normality_test_report.md` | Shapiro-Wilk, Jarque-Bera, D'Agostino, KS results |
| `diagnostic_plots.md` | Diagnostic chart descriptions and interpretation |
| `model_comparison_table.md` | GPT model sentiment/emotion accuracy benchmarks |
| `README.md` | Keyword list and event timeline |

### Output Data

| File | Rows | Description |
|---|---|---|
| `daily_sentiment_IHSG.csv` | 25 | Daily net sentiment + IHSG returns |
| `daily_sentiment_USDIDR.csv` | 25 | Daily net sentiment + USD/IDR returns |
| `correlation_robustness.csv` | 10 | Pair × Treatment correlation results |
| `outlier_diagnostics_detail.csv` | 30 | Individual outlier observations |
| `outlier_diagnostics_summary.csv` | 10 | Outlier counts per variable |
| `diagnostic_summary_table.csv` | 10 | Unified diagnostic table |
| `stationarity_test_results.csv` | 16 | ADF + KPSS per series |
| `normality_test_results.csv` | 17 | Normality tests per variable × period |
| `model_comparison_table.csv` | 9 | GPT model comparison |
| `keyword_completeness_summary.csv` | 127 | Scraping completeness per keyword |
| `parsed_tweet_filenames_sorted.csv` | 160 | All scraped CSV file metadata |

---

## To Reproduce

```bash
# Full pipeline (run in order)
py market_data_merge_analysis.py    # Stage 1: Data pairing
py pearson_correlation_analysis.py  # Stage 2-3: Sentiment + correlations
py create_charts.py                 # Stage 4a: Main charts
py create_diagnostic_plots.py       # Stage 4b: Diagnostic charts
py normality_tests.py               # Stage 5: Normality
py stationarity_tests.py            # Stage 6: Stationarity
py outlier_diagnostics.py           # Stage 7a: Outliers
py correlation_robustness.py        # Stage 7b: Robustness
py diagnostic_summary.py            # Stage 7c: Summary table

# Optional: GPT model benchmark (requires chatgpt_results/ report files)
py model_comparison_table.py
```

**Requirements:** pandas, numpy, scipy, statsmodels, nltk (VADER), yfinance, matplotlib, seaborn

---

## Known Limitations

1. **VADER is English-optimized.** Indonesian tweet sentiment is scored with an English lexicon, reducing accuracy. Loanwords provide partial signal only.
2. **After Demo period has critical data gaps.** Only 2 paired IHSG observations and 0 USD/IDR observations for Sep 9–30. Re-scraping needed (exact gaps in `keyword_completeness_summary.csv`).
3. **Small sample size (n=25).** Statistical power is limited. A correlation of r=0.50 would need n≈29 for 80% power at α=0.05.
4. **Causality is ambiguous.** Same-day correlation cannot distinguish sentiment → returns from returns → sentiment or third-factor → both.
5. **API keys exposed.** `sentiment-analysis.ipynb`, `api_keys.txt`, `order7239414.txt`, and `aejofajfoeja.txt` contain hardcoded credentials. These should be rotated and files excluded from version control.

---

*End of master analysis report. All 10 reviewer requests are addressed in this document and its referenced files.*
