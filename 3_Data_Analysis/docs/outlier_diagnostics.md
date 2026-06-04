# Outlier Diagnostics

**Generated:** 2026-06-04 17:11
**Methods:** IQR (1.5×IQR rule), Z-Score (|Z| > 2.5), Modified Z-Score via MAD (|Z_mod| > 3.5)

---

## Outlier Summary per Variable

| Variable | N | IQR | Z-Score | MAD | Union | % | High | Low |
|----------|---|-----|---------|-----|-------|---|------|------|
| IHSG Net Sentiment (NSR) | 25 | 1 | 1 | 1 | 1 | 4.0% | 1 | 0 |
| USD/IDR Net Sentiment (NSR) | 25 | 1 | 1 | 6 | 6 | 24.0% | 5 | 1 |
| IHSG Return (%) | 25 | 0 | 1 | 0 | 1 | 4.0% | 1 | 0 |
| USD/IDR Return (%) | 25 | 0 | 0 | 1 | 1 | 4.0% | 0 | 1 |
| IHSG Net Sentiment (NSC) | 25 | 2 | 0 | 0 | 2 | 8.0% | 2 | 0 |
| USD/IDR Net Sentiment (NSC) | 25 | 2 | 0 | 3 | 3 | 12.0% | 3 | 0 |
| IHSG Mean Compound | 25 | 0 | 0 | 0 | 0 | 0.0% | 0 | 0 |
| USD/IDR Mean Compound | 25 | 1 | 1 | 4 | 4 | 16.0% | 4 | 0 |
| IHSG Tweet Count | 25 | 2 | 0 | 2 | 2 | 8.0% | 2 | 0 |
| USD/IDR Tweet Count | 25 | 0 | 0 | 10 | 10 | 40.0% | 10 | 0 |

---

## Outlier Dates (Union of All Methods)

| Date | Variable | Value | Direction | Detection Method |
|------|----------|-------|-----------|------------------|
| 2025-09-03 00:00:00 | IHSG Net Sentiment (NSR) |      +0.2093 | HIGH | IQR, Z=3.11, MAD |
| 2025-08-04 00:00:00 | USD/IDR Net Sentiment (NSR) |      +0.3333 | HIGH | IQR, Z=2.98, MAD |
| 2025-08-13 00:00:00 | USD/IDR Net Sentiment (NSR) |      -0.1000 | LOW | MAD |
| 2025-08-14 00:00:00 | USD/IDR Net Sentiment (NSR) |      +0.2222 | HIGH | MAD |
| 2025-08-18 00:00:00 | USD/IDR Net Sentiment (NSR) |      +0.1667 | HIGH | MAD |
| 2025-08-21 00:00:00 | USD/IDR Net Sentiment (NSR) |      +0.1667 | HIGH | MAD |
| 2025-08-22 00:00:00 | USD/IDR Net Sentiment (NSR) |      +0.1429 | HIGH | MAD |
| 2025-08-12 00:00:00 | IHSG Return (%) |      +2.4425 | HIGH | Z=2.51 |
| 2025-08-14 00:00:00 | USD/IDR Return (%) |      -0.8567 | LOW | MAD |
| 2025-08-14 00:00:00 | IHSG Net Sentiment (NSC) |     +10.7808 | HIGH | IQR |
| 2025-08-15 00:00:00 | IHSG Net Sentiment (NSC) |     +11.7738 | HIGH | IQR |
| 2025-08-28 00:00:00 | USD/IDR Net Sentiment (NSC) |      +4.4042 | HIGH | IQR, MAD |
| 2025-09-02 00:00:00 | USD/IDR Net Sentiment (NSC) |      +3.7934 | HIGH | MAD |
| 2025-09-03 00:00:00 | USD/IDR Net Sentiment (NSC) |      +4.3894 | HIGH | IQR, MAD |
| 2025-08-04 00:00:00 | USD/IDR Mean Compound |      +0.1826 | HIGH | IQR, Z=3.01, MAD |
| 2025-08-14 00:00:00 | USD/IDR Mean Compound |      +0.1055 | HIGH | MAD |
| 2025-08-19 00:00:00 | USD/IDR Mean Compound |      +0.1186 | HIGH | MAD |
| 2025-08-22 00:00:00 | USD/IDR Mean Compound |      +0.1161 | HIGH | MAD |
| 2025-08-29 00:00:00 | IHSG Tweet Count |    +458.0000 | HIGH | IQR, MAD |
| 2025-09-01 00:00:00 | IHSG Tweet Count |    +441.0000 | HIGH | IQR, MAD |
| 2025-08-25 00:00:00 | USD/IDR Tweet Count |    +145.0000 | HIGH | MAD |
| 2025-08-26 00:00:00 | USD/IDR Tweet Count |    +134.0000 | HIGH | MAD |
| 2025-08-27 00:00:00 | USD/IDR Tweet Count |    +138.0000 | HIGH | MAD |
| 2025-08-28 00:00:00 | USD/IDR Tweet Count |    +163.0000 | HIGH | MAD |
| 2025-08-29 00:00:00 | USD/IDR Tweet Count |    +214.0000 | HIGH | MAD |
| 2025-09-01 00:00:00 | USD/IDR Tweet Count |    +297.0000 | HIGH | MAD |
| 2025-09-02 00:00:00 | USD/IDR Tweet Count |    +222.0000 | HIGH | MAD |
| 2025-09-03 00:00:00 | USD/IDR Tweet Count |    +196.0000 | HIGH | MAD |
| 2025-09-04 00:00:00 | USD/IDR Tweet Count |    +260.0000 | HIGH | MAD |
| 2025-09-05 00:00:00 | USD/IDR Tweet Count |     +97.0000 | HIGH | MAD |

---

## Key Outlier Dates (Cross-Variable)

Dates flagged as outliers in **2+ variables simultaneously**:

| Date | Variables Flagged | Notable Event |
|------|---------------------|---------------|
| 2025-08-14 00:00:00 | USD/IDR Net Sentiment (NSR), USD/IDR Return (%), IHSG Net Sentiment (NSC), USD/IDR Mean Compound |  |
| 2025-09-03 00:00:00 | IHSG Net Sentiment (NSR), USD/IDR Net Sentiment (NSC), USD/IDR Tweet Count |  |
| 2025-08-04 00:00:00 | USD/IDR Net Sentiment (NSR), USD/IDR Mean Compound |  |
| 2025-09-01 00:00:00 | IHSG Tweet Count, USD/IDR Tweet Count |  |
| 2025-08-22 00:00:00 | USD/IDR Net Sentiment (NSR), USD/IDR Mean Compound |  |
| 2025-08-28 00:00:00 | USD/IDR Net Sentiment (NSC), USD/IDR Tweet Count |  |
| 2025-09-02 00:00:00 | USD/IDR Net Sentiment (NSC), USD/IDR Tweet Count |  |
| 2025-08-29 00:00:00 | IHSG Tweet Count, USD/IDR Tweet Count |  |

---

## Overall Statistics

- Total variable-days checked: 250 (10 variables × varying n)
- Total outlier observations (union): 30
- Overall outlier rate: 12.00%

### Most Common Outlier Dates (Top 10)

- **2025-08-14 00:00:00**: flagged in 4 variables
- **2025-09-03 00:00:00**: flagged in 3 variables
- **2025-08-04 00:00:00**: flagged in 2 variables
- **2025-09-01 00:00:00**: flagged in 2 variables
- **2025-08-22 00:00:00**: flagged in 2 variables
- **2025-08-28 00:00:00**: flagged in 2 variables
- **2025-09-02 00:00:00**: flagged in 2 variables
- **2025-08-29 00:00:00**: flagged in 2 variables
- **2025-08-13 00:00:00**: flagged in 1 variables
- **2025-08-21 00:00:00**: flagged in 1 variables

---

**CSV detail:** [`outlier_diagnostics_detail.csv`](outlier_diagnostics_detail.csv)  
**CSV summary:** [`outlier_diagnostics_summary.csv`](outlier_diagnostics_summary.csv)  
**Script:** [`outlier_diagnostics.py`](outlier_diagnostics.py)
