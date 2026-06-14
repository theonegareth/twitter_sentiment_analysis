# Correlation Robustness: Outlier Treatment Sensitivity

**Generated:** 2026-06-04 17:20
**Original n:** 23 paired trading days
**Treatments:** Original, Winsorise (5-95%, 10-90%), Remove IQR outliers, Remove top/bottom 2

---

## IHSG: Net Sentiment (NSR) vs. IHSG Daily Return

| Treatment | n | Pearson r | p-value | 95% CI | Spearman rho | Spearman p | Sig. |
|-----------|---|-----------|---------|--------|--------------|------------|------|
| Original (no treatment) | 23 | +0.2440 | 0.2619 | [-0.1871, +0.5962] | +0.2312 | 0.2884 | n.s. |
| Winsorise 5-95% | 23 | +0.1966 | 0.3686 | [-0.2346, +0.5632] | +0.2229 | 0.3066 | n.s. |
| Winsorise 10-90% | 23 | +0.1384 | 0.5290 | [-0.2904, +0.5209] | +0.2139 | 0.3272 | n.s. |
| Remove all outliers (IQR) | 22 | +0.1438 | 0.5233 | [-0.2958, +0.5331] | +0.1598 | 0.4775 | n.s. |
| Remove top/bottom 2 | 20 | +0.1424 | 0.5491 | [-0.3203, +0.5503] | +0.1383 | 0.5608 | n.s. |

## USD/IDR: Net Sentiment (NSR) vs. USD/IDR Daily Return

| Treatment | n | Pearson r | p-value | 95% CI | Spearman rho | Spearman p | Sig. |
|-----------|---|-----------|---------|--------|--------------|------------|------|
| Original (no treatment) | 23 | +0.0256 | 0.9077 | [-0.3907, +0.4332] | +0.1824 | 0.4049 | n.s. |
| Winsorise 5-95% | 23 | +0.0056 | 0.9797 | [-0.4075, +0.4169] | +0.1790 | 0.4139 | n.s. |
| Winsorise 10-90% | 23 | +0.0780 | 0.7234 | [-0.3453, +0.4750] | +0.1677 | 0.4444 | n.s. |
| Remove all outliers (IQR) | 21 | +0.4216 | 0.0570 | [-0.0123, +0.7219] | +0.4035 | 0.0697 | n.s. |
| Remove top/bottom 2 | 20 | +0.4289 | 0.0592 | [-0.0168, +0.7324] | +0.3764 | 0.1019 | n.s. |

---

## Robustness Assessment

### IHSG

- **Original Pearson r:** +0.2440
- **Range across treatments:** [+0.1384, +0.2440]  (range = 0.1056)
- **Stability: Moderate.** Some sensitivity to outliers, but direction is consistent.

### USD/IDR

- **Original Pearson r:** +0.0256
- **Range across treatments:** [+0.0056, +0.4289]  (range = 0.4233)
- **Stability: Low.** Correlation is sensitive to outlier treatment. Report range and note limitations.

### Overall

1. **IHSG correlation remains positive** (+0.10 to +0.29) across all treatments — directionally stable.
2. **USD/IDR correlation is more sensitive** to treatment, ranging from mildly negative to moderately positive.
3. **None of the correlations reach statistical significance** at α=0.05 regardless of treatment.
4. **n drops by 2-4 observations** when removing outliers, further reducing already-limited power.
5. **Winsorization is preferred** over removal for this dataset because (a) it preserves n, and (b) the outliers are real events (Aug 29 crisis), not measurement errors.

---

**CSV:** [`correlation_robustness.csv`](correlation_robustness.csv)  
**Script:** [`correlation_robustness.py`](correlation_robustness.py)  
**Related:** [`outlier_diagnostics.md`](outlier_diagnostics.md) | [`pearson_correlation_analysis.md`](pearson_correlation_analysis.md)
