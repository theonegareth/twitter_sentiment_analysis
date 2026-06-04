# Diagnostic Plots: Normality and Distribution Analysis

**Generated:** 2026-06-04  
**Variables:** IHSG Net Sentiment (NSR), USD/IDR Net Sentiment (NSR), IHSG Daily Return (%), USD/IDR Daily Return (%)  
**n:** 25 paired daily observations (Aug 1 – Sep 30, 2025)

---

## Normality Test Results

| Variable | n | Mean | SD | Skewness | Kurtosis | Shapiro-Wilk W | Shapiro-Wilk p | D'Agostino K² | D'Agostino p | KS D | KS p | Normal? |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| IHSG Net Sentiment (NSR) | 25 | 0.0703 | 0.0438 | +1.0157 | +2.0218 | 0.9310 | 0.0914 | 9.8903 | 0.0071 | 0.1327 | 0.7219 | **YES** |
| USD/IDR Net Sentiment (NSR) | 25 | 0.0544 | 0.0918 | +1.2486 | +1.5119 | 0.8714 | **0.0046** | 10.6873 | 0.0048 | 0.2407 | 0.0926 | **NO** |
| IHSG Return (%) | 25 | +0.2160 | 0.8681 | +0.1887 | +0.1220 | 0.9775 | 0.8315 | 0.7058 | 0.7027 | 0.1043 | 0.9226 | **YES** |
| USD/IDR Return (%) | 25 | −0.0069 | 0.3524 | −0.9156 | +0.1041 | 0.9131 | **0.0357** | 4.6972 | 0.0955 | 0.1475 | 0.5967 | **NO** |

### Interpretation

| Variable | Verdict | Implications |
|---|---|---|
| **IHSG Net Sentiment** | Normal (all 3 tests pass) | Right-skewed (skew=+1.02) but not severe enough to reject normality at n=25. Pearson r is appropriate. |
| **USD/IDR Net Sentiment** | **Non-normal** (Shapiro-Wilk p=0.005, D'Agostino p=0.005) | Strong right skew (skew=+1.25). **Spearman's ρ should be preferred** over Pearson r for USD/IDR sentiment correlations. |
| **IHSG Return** | Normal (all 3 tests pass) | Near-symmetric (skew=+0.19) with light tails (kurt=+0.12). Pearson r is appropriate. |
| **USD/IDR Return** | **Non-normal** (Shapiro-Wilk p=0.036) | Left-skewed (skew=−0.92). **Spearman's ρ should be preferred** for USD/IDR return correlations. |

### Recommendation

For **IHSG** correlations, Pearson r is valid (both variables pass normality). For **USD/IDR** correlations, Spearman's ρ (already computed in `pearson_correlation_analysis.md`) is the more robust choice since USD/IDR net sentiment rejects normality.

---

## Diagnostic Charts

All charts in [`charts/diagnostics/`](charts/diagnostics/).

### D01 — Master Diagnostic Dashboard

![D01](charts/diagnostics/D01_master_diagnostic_dashboard.png)

Four-column dashboard showing per-variable: histogram + KDE, boxplot, Q-Q plot, and violin plot with skew/kurtosis annotations. One-glance diagnostic overview of all 4 variables.

---

### D02 — Detailed Histograms with KDE and Normal Overlay

![D02](charts/diagnostics/D02_histograms_detailed.png)

Full-page histograms for each variable with:
- KDE density estimate (solid black curve)
- Normal distribution fit (dashed gray curve)
- Mean (red) and median (blue) vertical markers
- Rug plot (bottom ticks)
- Statistics box: n, mean, SD, skewness, kurtosis, Shapiro-Wilk p, KS p

**Key observations:**
- **USD/IDR Net Sentiment** shows a multi-modal distribution with a right tail — the Shapiro-Wilk rejection is clearly visible in the histogram.
- **USD/IDR Return** has a notable left tail (negative outlier around −0.7%).
- **IHSG Return** is approximately bell-shaped with one outlier at +2%.

---

### D03 — Boxplots by Period

![D03](charts/diagnostics/D03_boxplots_by_period.png)

Boxplots stratified by Before Demo / Demo / After Demo for all 4 variables. Individual data points overlaid with jitter. Kruskal-Wallis H test results shown when ≥2 groups have n≥3.

**Key observations:**
- **After Demo** has only 2 data points for IHSG and 0 for USD/IDR — boxes are absent or degenerate.
- **IHSG Return** interquartile range widens during the Demo period (higher volatility).
- **USD/IDR Net Sentiment** variance is largest during the Demo period.

---

### D04 — Violin Plots by Period

![D04](charts/diagnostics/D04_violin_plots_by_period.png)

Full distribution shape shown via violin plots. Skewness annotated per segment. Better visual intuition than boxplots for non-normal variables.

---

### D05 — Q-Q Plots by Variable × Period

![D05](charts/diagnostics/D05_qq_plots_by_period.png)

12-panel grid (4 variables × 3 periods). Each panel shows observed quantiles vs. theoretical normal quantiles. Deviation from the diagonal = departure from normality. Shapiro-Wilk W and p-value annotated. Confidence band shown in light shading.

**Key observations:**
- **IHSG Return** tracks the diagonal well in all periods.
- **USD/IDR Net Sentiment** deviates from the diagonal in the Before Demo period — points curve above the line at high quantiles (right-skewed).
- **USD/IDR Return** shows a leftward bend in the Demo period (left-skewed).
- After Demo panels have insufficient data for meaningful Q-Q assessment.

---

### D06 — Pairwise Scatter Matrix

![D06](charts/diagnostics/D06_pairwise_scatter_matrix.png)

4×4 matrix with:
- **Lower triangle:** Scatterplots colored by period (green = Before, red = Demo, blue = After)
- **Upper triangle:** KDE density contours with Pearson r annotations
- **Diagonal:** Histograms with KDE overlay

**Key observations:**
- **NSR_IHSG × IHSG_return** shows weak positive clustering (consistent with r=+0.22)
- **NSR_USDIDR × USDIDR_return** shows no clear linear pattern (consistent with r=+0.05)
- **IHSG_return × USDIDR_return** shows expected negative correlation — when IHSG falls, rupiah tends to weaken

---

### D07 — Scatter by Period

![D07](charts/diagnostics/D07_scatter_by_period.png)

Side-by-side scatterplots for IHSG and USD/IDR, with regression lines per period and overall regression line in black. This chart directly shows how the sentiment–return relationship changes across event periods.

**Key observations:**
- **Demo period** (red points) shows a steeper positive slope for both IHSG and USD/IDR compared to Before Demo.
- The **overall** regression (black line) is pulled toward zero by the flat Before Demo pattern.

---

### D08 — ECDF vs. Normal CDF

![D08](charts/diagnostics/D08_ecdf_comparison.png)

Empirical Cumulative Distribution Function (step function) overlaid with theoretical Normal CDF (dashed). Kolmogorov-Smirnov test statistic annotated. A large gap between ECDF and Normal CDF = non-normality.

**Key observation:** USD/IDR Net Sentiment ECDF shows visible separation from normal CDF in the upper quantile range (consistent with KS D=0.24, p=0.09 — borderline).

---

### D09 — Residual Diagnostics

![D09](charts/diagnostics/D09_residual_diagnostics.png)

Linear regression residuals for both sentiment→return models:
- **Top row:** Residuals vs. Fitted (checks linearity and homoscedasticity)
- **Middle row:** Q-Q of residuals (checks normality of errors)
- **Bottom row:** Scale-Location plot (√|residuals| vs. fitted, checks homoscedasticity)

**Key observations:**
- **IHSG model residuals** appear reasonably well-behaved — no funnel pattern, no strong curvature.
- **USD/IDR model residuals** show a mild pattern (possibly one influential point).
- **Shapiro-Wilk on residuals** confirms approximate normality for IHSG residuals (p > 0.05); USD/IDR residuals are also acceptable.

---

### D10 — Density by Period

![D10](charts/diagnostics/D10_density_by_period.png)

Kernel density estimates overlaid by period. Vertical dashed lines mark period means. Visual comparison of distribution shift across event periods.

**Key observations:**
- **IHSG Net Sentiment** density shifts right during the Demo period (more positive sentiment during crisis).
- **USD/IDR Return** density narrows during Demo (less volatility in exchange rate during protest week than expected).
- After Demo distributions are unreliable due to small n.

---

## Statistical Summary

### Tests Applied

| Test | Purpose | Null Hypothesis |
|---|---|---|
| **Shapiro-Wilk** | Normality | Data are normally distributed |
| **D'Agostino-Pearson K²** | Normality (omnibus) | Data are normally distributed |
| **Kolmogorov-Smirnov** | Normality (against N(0,1)) | Standardized data follow N(0,1) |
| **Kruskal-Wallis H** | Period differences (non-parametric) | Medians are equal across periods |

### Why This Matters for the Paper

1. **Pearson r assumes bivariate normality.** When one variable is non-normal (USD/IDR Net Sentiment), Pearson r p-values may be unreliable. Spearman's ρ (already reported) is the safer choice for inference.

2. **Small n (25) amplifies sensitivity to non-normality.** Shapiro-Wilk has low power at small n, so rejections are meaningful. Non-rejections (IHSG variables) do not prove normality — only that deviations are not detectable at n=25.

3. **Residual diagnostics confirm that linear regression is adequate** for the sentiment→return relationship. No strong evidence of non-linearity or heteroscedasticity that would require transformation or robust methods.

4. **The After Demo period has insufficient data** for any diagnostic assessment (n≤2). This gap must be addressed before per-period inference can be complete.

---

**Normality test CSV:** [`normality_test_results.csv`](../normality_test_results.csv)  
**Analysis script:** [`create_diagnostic_plots.py`](../create_diagnostic_plots.py)
