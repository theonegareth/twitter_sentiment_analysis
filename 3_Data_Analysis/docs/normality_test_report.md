# Normality Test Report

**Generated:** 2026-06-04 17:11
**Variables:** IHSG Net Sentiment (NSR), USD/IDR Net Sentiment (NSR), IHSG Daily Return (%), USD/IDR Daily Return (%)

---

## Test Descriptions

| Test | Null Hypothesis (H0) | Reject H0 if p < 0.05 means |
|------|---------------------|------------------------------|
| **Shapiro-Wilk** | Data are normally distributed | Data are significantly non-normal |
| **Jarque-Bera** | Skewness = 0 and kurtosis = 3 | Data deviate from normal in skew or kurtosis |
| **D'Agostino-Pearson K²** | Kurtosis = 3 and skewness = 0 (omnibus) | Combined skewness + kurtosis deviation from normal |
| **Kolmogorov-Smirnov** | Empirical CDF matches N(mean, sd) | Distribution differs from fitted normal |

---

## Full Period Results (n=25)

| Variable | SW W | SW p | SW Ok? | JB Stat | JB p | JB Ok? | DA K² | DA p | DA Ok? | KS D | KS p | KS Ok? |
|----------|------|------|--------|---------|------|--------|--------|------|--------|------|------|--------|
| IHSG Net Sentiment (NSR) | 0.9310 | 0.0914 | **YES** | 8.5563 | 0.0139 | **NO** | 9.8903 | 0.0071 | **NO** | 0.1345 | 0.7073 | **YES** |
| USD/IDR Net Sentiment (NSR) | 0.8714 | 0.0046 | **NO** | 8.8774 | 0.0118 | **NO** | 10.6873 | 0.0048 | **NO** | 0.2395 | 0.0955 | **YES** |
| IHSG Return (%) | 0.9775 | 0.8315 | **YES** | 0.1639 | 0.9213 | **YES** | 0.7058 | 0.7027 | **YES** | 0.1011 | 0.9377 | **YES** |
| USD/IDR Return (%) | 0.9131 | 0.0357 | **NO** | 3.5041 | 0.1734 | **YES** | 4.6972 | 0.0955 | **YES** | 0.1490 | 0.5845 | **YES** |

### Summary Statistics

| Variable | n | Mean | SD | Skewness | Kurtosis |
|----------|---|------|----|----------|----------|
| IHSG Net Sentiment (NSR) | 25 | 0.0703 | 0.0447 | +1.0157 | +2.0218 |
| USD/IDR Net Sentiment (NSR) | 25 | 0.0544 | 0.0937 | +1.2486 | +1.5119 |
| IHSG Return (%) | 25 | 0.2160 | 0.8860 | +0.1887 | +0.1220 |
| USD/IDR Return (%) | 25 | -0.0069 | 0.3597 | -0.9156 | +0.1041 |

---

## Per-Period Breakdown

| Variable | Period | n | SW W | SW p | SW Ok? | JB Stat | JB p | JB Ok? |
|----------|--------|---|------|------|--------|---------|------|--------|
| IHSG Net Sentiment (NSR) | Full Period | 25 | 0.9310 | 0.0914 | **YES** | 8.5563 | 0.0139 | **NO** |
| IHSG Net Sentiment (NSR) | Before Demo | 14 | 0.9764 | 0.9487 | **YES** | 0.1068 | 0.9480 | **YES** |
| IHSG Net Sentiment (NSR) | Demo | 9 | 0.9201 | 0.3933 | **YES** | 1.3821 | 0.5011 | **YES** |
| IHSG Net Sentiment (NSR) | After Demo | 2 | — | — | insufficient | — | — | insufficient |
| USD/IDR Net Sentiment (NSR) | Full Period | 25 | 0.8714 | 0.0046 | **NO** | 8.8774 | 0.0118 | **NO** |
| USD/IDR Net Sentiment (NSR) | Before Demo | 15 | 0.8935 | 0.0757 | **YES** | 1.0666 | 0.5867 | **YES** |
| USD/IDR Net Sentiment (NSR) | Demo | 10 | 0.8557 | 0.0679 | **YES** | 1.2382 | 0.5384 | **YES** |
| USD/IDR Net Sentiment (NSR) | After Demo | 0 | — | — | insufficient | — | — | insufficient |
| IHSG Return (%) | Full Period | 25 | 0.9775 | 0.8315 | **YES** | 0.1639 | 0.9213 | **YES** |
| IHSG Return (%) | Before Demo | 14 | 0.9356 | 0.3647 | **YES** | 1.1623 | 0.5593 | **YES** |
| IHSG Return (%) | Demo | 9 | 0.9182 | 0.3779 | **YES** | 0.7768 | 0.6782 | **YES** |
| IHSG Return (%) | After Demo | 2 | — | — | insufficient | — | — | insufficient |
| USD/IDR Return (%) | Full Period | 25 | 0.9131 | 0.0357 | **NO** | 3.5041 | 0.1734 | **YES** |
| USD/IDR Return (%) | Before Demo | 15 | 0.9433 | 0.4259 | **YES** | 0.8910 | 0.6405 | **YES** |
| USD/IDR Return (%) | Demo | 10 | 0.7928 | 0.0118 | **NO** | 7.2978 | 0.0260 | **NO** |
| USD/IDR Return (%) | After Demo | 0 | — | — | insufficient | — | — | insufficient |

---

## Consensus Verdict

| IHSG Net Sentiment (NSR) | SW: YES | JB: NO | DA: NO | KS: YES | 2/4 pass | **BORDERLINE** |
| USD/IDR Net Sentiment (NSR) | SW: NO | JB: NO | DA: NO | KS: YES | 1/4 pass | **NON-NORMAL** |
| IHSG Return (%) | SW: YES | JB: YES | DA: YES | KS: YES | 4/4 pass | **NORMAL** |
| USD/IDR Return (%) | SW: NO | JB: YES | DA: YES | KS: YES | 3/4 pass | **NORMAL** |

### Implications for Correlation Analysis

- **IHSG Net Sentiment + IHSG Return:** Both variables pass normality. Pearson r is valid.
- **USD/IDR Net Sentiment:** Rejected by Shapiro-Wilk and Jarque-Bera (right-skewed). **Use Spearman rho** for USD/IDR correlations.
- **USD/IDR Return:** Rejected by Shapiro-Wilk (p=0.036). **Use Spearman rho** for USD/IDR correlations.
- **Sample size (n=25):** Tests have limited power at small n. Non-rejection does not prove normality — only that deviations are not detectable at this n.
- **Per-period n is very small (2–15):** Per-period normality tests are unreliable. Report full-period test results only.

---

**CSV:** [`normality_test_results.csv`](normality_test_results.csv)  
**Script:** [`normality_tests.py`](normality_tests.py)  
**Diagnostic charts:** [`charts/diagnostics/`](charts/diagnostics/)  
**Full diagnostic report:** [`diagnostic_plots.md`](diagnostic_plots.md)
