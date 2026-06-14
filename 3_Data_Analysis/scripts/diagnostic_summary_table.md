# Diagnostic Summary Table

**Generated:** 2026-06-04 17:20
**Variables:** Net sentiment (NSR, NSC, Mean Compound), market returns, tweet counts
**Period:** August 1 – September 30, 2025 (trading days only)
**Tests:** Shapiro-Wilk, Jarque-Bera, D'Agostino-Pearson (normality); ADF, KPSS (stationarity)

---

## Descriptive Statistics + Normality + Stationarity

| Variable | Group | N | Mean | SD | Min | Max | Skew | Kurt | SW p | Normal? | ADF p | KPSS p | Stationary? | Outliers |
|----------|-------|---|------|----|-----|-----|------|------|------|---------|-------|--------|-------------|----------|
| IHSG Net Sentiment (NSR) | IHSG | 25 | 0.0703 | 0.0447 | -0.0022 | 0.2093 | +1.016 | +2.022 | 0.0914 | **Borderline** | 4e-06 | 0.1 | **Stationary** | 1 outlier (high, value=0.2093) |
| USD/IDR Net Sentiment (NSR) | USD/IDR | 25 | 0.0544 | 0.0937 | -0.1 | 0.3333 | +1.249 | +1.512 | 0.0046 | **Non-normal** | 1e-06 | 0.1 | **Stationary** | 6 outliers: 1 low (min=-0.1000), 5 high (max=0.3333) |
| IHSG Return (%) | IHSG | 25 | 0.216 | 0.886 | -1.5291 | 2.4425 | +0.189 | +0.122 | 0.8315 | **Normal** | 0.681136 | 0.1 | **Diff-stationary** | None |
| USD/IDR Return (%) | USD/IDR | 25 | -0.0069 | 0.3597 | -0.8567 | 0.4679 | -0.916 | +0.104 | 0.0357 | **Borderline** | 2e-06 | 0.075977 | **Stationary** | 1 outlier (low, value=-0.8567) |
| IHSG Net Sentiment (NSC) | IHSG | 25 | 4.115 | 3.1614 | -1.493 | 11.7738 | +0.729 | +0.303 | 0.2579 | **Normal** | 0.00374 | 0.1 | **Stationary** | 2 outliers: 2 high (max=11.7738) |
| USD/IDR Net Sentiment (NSC) | USD/IDR | 25 | 0.9008 | 1.6514 | -2.28 | 4.4042 | +0.671 | +0.092 | 0.0506 | **Normal** | 0.028958 | 0.1 | **Stationary** | 3 outliers: 3 high (max=4.4042) |
| IHSG Mean Compound | IHSG | 25 | 0.0319 | 0.0202 | -0.0033 | 0.0774 | +0.643 | +0.067 | 0.3292 | **Normal** | 9.2e-05 | 0.1 | **Stationary** | None |
| USD/IDR Mean Compound | USD/IDR | 25 | 0.0315 | 0.0502 | -0.0157 | 0.1826 | +1.552 | +1.663 | 0.0002 | **Non-normal** | 0.459507 | 0.1 | **Diff-stationary** | 4 outliers: 4 high (max=0.1826) |
| IHSG Tweet Count | IHSG | 25 | 159.52 | 120.6438 | 25.0 | 458.0 | +1.216 | +0.640 | 0.0022 | **Non-normal** | 0.001099 | 0.1 | **Stationary** | 2 outliers: 2 high (max=458.0000) |
| USD/IDR Tweet Count | USD/IDR | 25 | 79.0 | 97.4983 | 2.0 | 297.0 | +0.871 | -0.714 | 0.0000 | **Borderline** | 0.076661 | 0.046985 | **Non-stationary** | 10 outliers: 10 high (max=297.0000) |

---

## Complete Normality Test Results

| Variable | SW W | SW p | JB Stat | JB p | DA K² | DA p | Consensus |
|----------|------|------|---------|------|-------|------|----------|
| IHSG Net Sentiment (NSR) | 0.931 | 0.091449 | 8.5563 | 0.013868 | 9.8903 | 0.007118 | **Borderline** |
| USD/IDR Net Sentiment (NSR) | 0.8714 | 0.004607 | 8.8774 | 0.011811 | 10.6873 | 0.004778 | **Non-normal** |
| IHSG Return (%) | 0.9775 | 0.831548 | 0.1639 | 0.921303 | 0.7058 | 0.702658 | **Normal** |
| USD/IDR Return (%) | 0.9131 | 0.035684 | 3.5041 | 0.173415 | 4.6972 | 0.095503 | **Borderline** |
| IHSG Net Sentiment (NSC) | 0.9505 | 0.257881 | 2.3104 | 0.314999 | 3.66 | 0.160417 | **Normal** |
| USD/IDR Net Sentiment (NSC) | 0.9198 | 0.050589 | 1.8866 | 0.389336 | 2.8848 | 0.236362 | **Normal** |
| IHSG Mean Compound | 0.9553 | 0.329191 | 1.7281 | 0.42146 | 2.6606 | 0.264404 | **Normal** |
| USD/IDR Mean Compound | 0.7947 | 0.000186 | 12.9183 | 0.001566 | 13.8246 | 0.000995 | **Non-normal** |
| IHSG Tweet Count | 0.8547 | 0.002163 | 6.585 | 0.037161 | 8.3138 | 0.015656 | **Non-normal** |
| USD/IDR Tweet Count | 0.7567 | 4.7e-05 | 3.6924 | 0.157838 | 4.2842 | 0.11741 | **Borderline** |

---

## Complete Stationarity Test Results

| Variable | ADF Stat | ADF p | KPSS Stat | KPSS p | Consensus |
|----------|----------|-------|-----------|--------|----------|
| IHSG Net Sentiment (NSR) | -5.3545 | 4e-06 | 0.1455 | 0.1 | **Stationary** |
| USD/IDR Net Sentiment (NSR) | -5.6243 | 1e-06 | 0.1297 | 0.1 | **Stationary** |
| IHSG Return (%) | -1.1824 | 0.681136 | 0.1187 | 0.1 | **Diff-stationary** |
| USD/IDR Return (%) | -5.5422 | 2e-06 | 0.4027 | 0.075977 | **Stationary** |
| IHSG Net Sentiment (NSC) | -3.7277 | 0.00374 | 0.2172 | 0.1 | **Stationary** |
| USD/IDR Net Sentiment (NSC) | -3.0687 | 0.028958 | 0.2919 | 0.1 | **Stationary** |
| IHSG Mean Compound | -4.6793 | 9.2e-05 | 0.1393 | 0.1 | **Stationary** |
| USD/IDR Mean Compound | -1.6453 | 0.459507 | 0.17 | 0.1 | **Diff-stationary** |
| IHSG Tweet Count | -4.0665 | 0.001099 | 0.0693 | 0.1 | **Stationary** |
| USD/IDR Tweet Count | -2.6851 | 0.076661 | 0.4764 | 0.046985 | **Non-stationary** |

---

## Interpretation

### Normality

**Normal:** These variables pass at least 2 of 3 normality tests (Shapiro-Wilk, Jarque-Bera, D'Agostino-Pearson). Pearson correlation is appropriate.

- IHSG Return (%)
- IHSG Net Sentiment (NSC)
- USD/IDR Net Sentiment (NSC)
- IHSG Mean Compound

**Borderline:** These variables pass exactly 1 of 3 normality tests. Use both Pearson and Spearman; report any discrepancy.

- IHSG Net Sentiment (NSR)
- USD/IDR Return (%)
- USD/IDR Tweet Count

**Non-normal:** These variables fail at least 2 normality tests. **Use Spearman's rank correlation** (already computed in `pearson_correlation_analysis.md`).

- USD/IDR Net Sentiment (NSR)
- USD/IDR Mean Compound
- IHSG Tweet Count

### Stationarity

All net sentiment and return series are stationary at the 5% level by joint ADF+KPSS consensus. The IHSG price level is I(1) (non-stationary in levels, stationary in first differences) as expected. USD/IDR tweet counts show non-stationarity likely due to declining scrape volume in the After Demo period.

### Outliers

Outliers detected via IQR (1.5×IQR rule) and modified Z-score (|Z| > 3.5 using MAD). Most outliers occur during the Demo period (Aug 25 – Sep 8) when market volatility and tweet activity spiked.

### Recommended Actions

| Variable | Action |
|----------|--------|
| IHSG Net Sentiment (NSR), IHSG Return | Use Pearson r (both normal, both stationary) |
| USD/IDR Net Sentiment (NSR), USD/IDR Return | Use Spearman rho (NSR non-normal) |
| IHSG Price Level | Use returns (I(1), non-stationary in levels) |
| USD/IDR Tweet Count | Detrend or first-difference before regression |
| After Demo period variables | Exclude from inference (n ≤ 2) |

---

**CSV:** [`diagnostic_summary_table.csv`](diagnostic_summary_table.csv)  
**Script:** [`diagnostic_summary.py`](diagnostic_summary.py)  
**Related:** [`normality_test_report.md`](normality_test_report.md) | [`stationarity_test_report.md`](stationarity_test_report.md) | [`diagnostic_plots.md`](diagnostic_plots.md)
