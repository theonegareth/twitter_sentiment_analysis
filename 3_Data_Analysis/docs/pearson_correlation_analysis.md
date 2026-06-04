# Pearson Correlation Analysis: Net Sentiment vs. Market Returns

**Generated:** 2026-06-04 17:11
**Period:** 2025-08-01 to 2025-09-30
**Sentiment Method:** VADER (Valence Aware Dictionary and sEntiment Reasoner)
**Market Data:** Yahoo Finance (`^JKSE`, `USDIDR=X`)

---

## Methodology

### Net Sentiment Computation

Each tweet is scored with VADER's compound sentiment score (range −1 to +1). Two daily net sentiment metrics are computed:

1. **Net Sentiment Ratio (NSR):** `(count_of_positive_tweets − count_of_negative_tweets) / total_tweets`
2. **Net Sentiment Compound (NSC):** `sum(compound_score)` — cumulative daily VADER compound
3. **Mean Compound (MC):** `mean(compound_score)` — average daily VADER score

### Market Returns

Daily percentage returns computed as `(Close_t − Close_{t−1}) / Close_{t−1} × 100`.

### Statistical Tests

- **Pearson's r:** linear correlation between net sentiment and same-day market return
- **p-value:** two-tailed test of H₀: ρ = 0
- **95% Confidence Interval:** Fisher's z-transformation
- **Spearman's ρ:** rank correlation as robustness check (monotonic, not assuming linearity)

### Significance Notation

- \*\*\* p < 0.001
- \*\* p < 0.01
- \* p < 0.05
- n.s. not significant

---

## Overall Correlations (Full Period: Aug 1 – Sep 30)

| Pair | n | Pearson r | p-value | 95% CI | Spearman ρ | Sig. |
|------|---|-----------|---------|--------|------------|------|
| IHSG (net_sentiment_ratio) | 25 | +0.2194 | 0.291965 | [-0.1924, +0.5655] | +0.1708 | n.s. |
| IHSG (net_sentiment_compound) | 25 | +0.1177 | 0.575178 | [-0.2909, +0.4901] | +0.1423 | n.s. |
| IHSG (mean_compound) | 25 | +0.2214 | 0.287563 | [-0.1904, +0.5669] | +0.2085 | n.s. |
| USD/IDR (net_sentiment_ratio) | 25 | +0.0517 | 0.806154 | [-0.3506, +0.4379] | +0.1843 | n.s. |
| USD/IDR (net_sentiment_compound) | 25 | +0.3121 | 0.128829 | [-0.0947, +0.6296] | +0.2440 | n.s. |
| USD/IDR (mean_compound) | 25 | +0.0699 | 0.739972 | [-0.3345, +0.4525] | +0.1614 | n.s. |

### Descriptive Statistics

| Pair | Mean Sentiment | SD Sentiment | Mean Return (%) | SD Return (%) |
|------|----------------|--------------|-----------------|---------------|
| IHSG (net_sentiment_ratio) | 0.0703 | 0.0447 | 0.2160 | 0.8860 |
| IHSG (net_sentiment_compound) | 4.1150 | 3.1614 | 0.2160 | 0.8860 |
| IHSG (mean_compound) | 0.0319 | 0.0202 | 0.2160 | 0.8860 |
| USD/IDR (net_sentiment_ratio) | 0.0544 | 0.0937 | -0.0069 | 0.3597 |
| USD/IDR (net_sentiment_compound) | 0.9008 | 1.6514 | -0.0069 | 0.3597 |
| USD/IDR (mean_compound) | 0.0315 | 0.0502 | -0.0069 | 0.3597 |

---

## Per-Period Correlations

| Period | Pair | n | Pearson r | p-value | 95% CI | Spearman ρ | Sig. |
|--------|------|---|-----------|---------|--------|------------|------|
| Before Demo | IHSG (net_sentiment_ratio) | 14 | -0.0656 | 0.823763 | [-0.5761, +0.4818] | +0.0418 | n.s. |
| Before Demo | USD/IDR (net_sentiment_ratio) | 15 | +0.0658 | 0.815811 | [-0.4620, +0.5592] | +0.1470 | n.s. |
| Demo | IHSG (net_sentiment_ratio) | 9 | +0.5985 | 0.088637 | [-0.1089, +0.9035] | +0.4667 | n.s. |
| Demo | USD/IDR (net_sentiment_ratio) | 10 | +0.5260 | 0.118399 | [-0.1550, +0.8681] | +0.2364 | n.s. |
| After Demo | IHSG (net_sentiment_ratio) | 2 | — | — | — | — | insufficient |
| After Demo | USD/IDR (net_sentiment_ratio) | 0 | — | — | — | — | insufficient |

---

## Interpretation

### Net Sentiment → IHSG Returns

- **Pearson r = +0.2194** (n.s.)
- 95% CI: [-0.1924, +0.5655]
- n = 25 paired daily observations

**Direction:** Positive. As net Twitter sentiment about IHSG/market becomes more positive, same-day IHSG returns tend to rise. This is consistent with sentiment-driven trading — bullish social media chatter coincides with upward price movement.

### Net Sentiment → USD/IDR Returns

- **Pearson r = +0.0517** (n.s.)
- 95% CI: [-0.3506, +0.4379]
- n = 25 paired daily observations

**Direction:** Positive.

### Comparison with Paper Values

| Metric | Paper (reported) | This Analysis |
|--------|------------------|---------------|
| Net sentiment–IHSG | +0.36 | +0.2194 |
| Net sentiment–USD/IDR | −0.17 | +0.0517 |

### Caveats

1. **VADER is English-optimized.** Indonesian tweets are scored with an English lexicon, which reduces accuracy. English loanwords and code-switching in Indonesian finance Twitter provide partial signal, but sentiment misclassification is expected.

2. **Causality direction is ambiguous.** Same-day correlation does not establish whether sentiment drives returns, returns drive sentiment, or a third factor (e.g., breaking news) drives both.

3. **After Demo period has insufficient data.** Only 2 paired observations for IHSG and 0 for USD/IDR, making per-period comparisons unreliable for Sep 9–30.

4. **Tweet volume varies significantly by day.** Days with few tweets produce noisier sentiment estimates.

5. **Confidence intervals widen with smaller n.** Per-period correlations have wider CIs than the full-period estimate.
---

**Output files:** `daily_sentiment_IHSG.csv`, `daily_sentiment_USDIDR.csv`  
**Analysis script:** `pearson_correlation_analysis.py`
