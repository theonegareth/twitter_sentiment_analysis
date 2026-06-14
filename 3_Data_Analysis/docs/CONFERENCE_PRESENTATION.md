# Conference Presentation Outline

## "Does Twitter Sentiment Predict Financial Market Movements? Evidence from the 2025 Indonesian DPR Protests"

**Target:** 12–14 slides | **Duration:** 12–15 min | **Audience:** Academic conference

---

## Slide 1 — Title

**Title:** Does Twitter Sentiment Predict Financial Market Movements? Evidence from the 2025 Indonesian DPR Protests

**Subtitle:** Sentiment Analysis of ~80,000 Indonesian Tweets Using GPT-5 During Political Crisis

**Presenter / Affiliation**

---

## Slide 2 — Motivation & Context

The August–September 2025 DPR (Parliament) protests in Indonesia provide a natural experiment: a political shock with measurable financial market consequences.

| Date | Event |
|---|---|
| Aug 25 | Mass protests at Parliament over allowance increases |
| Aug 28 | Police vehicle kills online driver Affan Kurniawan — protests escalate |
| Aug 29 | **IHSG plunges, rupiah weakens, foreign capital flees** |
| Aug 30 | Protesters target politicians' homes |
| Sep 1–2 | 17+8 People's Demands consolidated |

**Research question:** *Did Twitter sentiment co-move with financial markets during this political crisis?*

**Chart:** `charts/06_event_timeline.png` — Annotated IHSG timeline with protest events marked.

---

## Slide 3 — Data Overview

| Metric | Value |
|---|---|
| Analysis period | Aug 1 – Sep 30, 2025 (61 calendar days) |
| Trading days | 42 (excl. weekends + Sep 5 Maulid Nabi holiday) |
| Event window periods | Before (Aug 1–24), Demo (Aug 25–Sep 8), After (Sep 9–30) |
| Keywords scraped | 42 Indonesian keywords (protest + economic terms) |
| Total scraped tweets | ~80,000 (after deduplication and cleaning) |
| Sentiment method | GPT-5 emotion classification (anger / fear / other) |
| Market data | IHSG Composite and USD/IDR exchange rate |
| **Paired observations** | **38** trading days with complete data |

---

## Slide 4 — Methodology

```
Twitter raw text → VADER lexicon scoring → Daily net sentiment aggregation
                                                 ↓
          Yahoo Finance → Daily % returns → Pearson r + Spearman ρ
```

### Sentiment Metrics

| Metric | Formula |
|---|---|
| Net Sentiment Ratio (NSR) | `(positive_tweets − negative_tweets) / total_tweets` |
| Net Sentiment Compound (NSC) | `sum(VADER compound score)` |
| Mean Compound (MC) | `mean(compound score)` |

### Statistical Framework

| Test | Purpose |
|---|---|
| Pearson r + Fisher z 95% CI | Linear correlation |
| Spearman ρ | Non-parametric robustness (reviewer-requested) |
| Shapiro-Wilk, Jarque-Bera | Normality diagnostics |
| ADF + KPSS | Stationarity diagnostics |
| IQR + Z-score + MAD | Outlier detection |
| Winsorization + IQR removal | Robustness across 5 treatments |

---

## Slide 5 — Main Result: Net Sentiment → IHSG Returns

| Window | n | Pearson r | p-value | 95% CI | Spearman ρ | Sig. |
|---|---|---|---|---|---|---|
| Full period (Aug 1 – Sep 30) | 38 | **+0.36** | **0.027** | [**+0.04**, **+0.61**] | +0.27 | **\*** |
| Demo period only (Aug 25 – Sep 8) | 9 | +0.37 | 0.329 | [−0.38, +0.85] | +0.33 | n.s. |
| After Demo (Sep 9 – Sep 30) | 15 | **+0.53** | **0.043** | [+0.02, +0.82] | +0.36 | **\*** |

- **Statistically significant** positive linear relationship (p=0.027)
- 95% CI excludes zero — sentiment and IHSG returns co-move
- After Demo period also significant (r=+0.53, p=0.043) — relationship persists after the crisis
- Spearman ρ = +0.27 (full period) — consistent non-parametric signal

**Chart:** `charts/01_scatter_net_sentiment_vs_returns.png` (will need regeneration with GPT-5 data)

---

## Slide 6 — Main Result: Net Sentiment → USD/IDR Returns

| Window | n | Pearson r | p-value | 95% CI | Spearman ρ | Sig. |
|---|---|---|---|---|---|---|
| Full period (Aug 1 – Sep 30) | 38 | **−0.25** | 0.133 | [−0.53, +0.08] | **−0.34** | n.s. |
| Demo period only (Aug 25 – Sep 8) | 9 | −0.08 | 0.844 | — | — | n.s. |

- Negative direction — negative sentiment aligns with rupiah depreciation (positive USD/IDR returns)
- Consistent with the paper's reported ~−0.17, though not statistically significant
- Spearman ρ = −0.34 — stronger non-parametric signal suggests non-linear relationship
- Exchange rate relationship is weaker than equity relationship

**Chart:** `charts/01_scatter_net_sentiment_vs_returns.png` (USD/IDR right panel, needs regeneration)

---

## Slide 7 — IHSG vs. USD/IDR: Divergent Paths During Crisis

- Aug 29: Simultaneous IHSG drop and rupiah weakening
- Tweet volume spikes 3× normal during Demo period (Aug 25 – Sep 8)
- Both markets respond to the same political shock — but with different correlation structures
- IHSG sentiment shows stable positive relationship; USD/IDR is more volatile

**Chart:** `charts/07_dual_market_comparison.png` — Dual-axis IHSG + USD/IDR overlay with Aug 29 crisis annotation.

---

## Slide 8 — Per-Period Correlation Comparison

| Period | IHSG r | USD/IDR r | IHSG n | USD/IDR n |
|---|---|---|---|---|
| Before Demo (Aug 1–24) | +0.18 | **−0.45** | 14 | 14 |
| Demo (Aug 25 – Sep 8) | +0.37 | −0.08 | 9 | 9 |
| **After Demo (Sep 9–30)** | **+0.53\*** | −0.27 | **15** | **15** |

- Before Demo near zero for IHSG — expected baseline
- Before Demo USD/IDR r = −0.45 (p=0.11) — notable negative pre-existing relationship
- After Demo IHSG is significant (p=0.043) — relationship persists and strengthens after crisis
- After Demo has data! 15 days with tweets — the event sparked sustained discussion

**Chart:** `charts/04_period_correlation_comparison.png` — Grouped bar chart with n annotations.

---

## Slide 9 — Robustness: Minimal Outlier Impact

**Only 3 outlier observations** detected via combined IQR + Z-score:

| Date | Variable | Value | Direction |
|---|---|---|---|
| Aug 29 | Net Sentiment (GPT-5) | −0.663 | LOW (crisis panic) |
| Aug 12 | IHSG Return (%) | +2.44% | HIGH (pre-crisis spike) |
| Aug 14 | USD/IDR Return (%) | −0.86% | LOW (rupiah strengthening) |

- GPT-5 data is substantially cleaner than VADER (3 outliers vs. 30)
- All 3 outliers correspond to real market events, not measurement error
- Removing these yields r_IHSG = +0.37 (p=0.024) — essentially unchanged
- **Robustness verdict:** Correlations are not driven by outliers

---

## Slide 10 — Diagnostic Verification

All econometric assumptions pass validation.

### Normality (Shapiro-Wilk, Jarque-Bera, D'Agostino)

| Variable | Shapiro-Wilk p | JB p | DA p | Verdict |
|---|---|---|---|---|
| Net Sentiment (GPT-5) | 0.237 | 0.296 | 0.175 | **Normal** ✅ |
| IHSG Return (%) | 0.500 | 0.868 | 0.714 | **Normal** ✅ |
| USD/IDR Return (%) | 0.189 | 0.426 | 0.241 | **Normal** ✅ |

### Stationarity (ADF + KPSS Consensus)

| Variable | ADF p | KPSS p | Verdict |
|---|---|---|---|
| Net Sentiment (GPT-5) | 0.022 | 0.10 | **Stationary** ✅ |
| IHSG Return (%) | <0.001 | 0.10 | **Stationary** ✅ |
| USD/IDR Return (%) | <0.001 | 0.06 | **Stationary** ✅ |

### Implications

- **Pearson r is valid** — all variables pass normality
- **No differencing needed** — all variables are stationary
- **GPT-5 produces clean, well-behaved sentiment measures** — substantially better than lexicon-based alternatives

---

## Slide 11 — Time Series Narrative

4-panel visualization connecting events to data.

**Chart:** `charts/02_ihsg_timeline_with_sentiment.png`

| Panel | Shows |
|---|---|
| IHSG Price | Daily close with Before/Demo/After shading |
| IHSG Returns | Bar chart of daily % changes |
| Net Sentiment | Daily NSR (orange bars) |
| Tweet Volume | Fill-plot of daily tweet count |

Annotated with key events: Aug 25 (protest begins), Aug 28 (Affan killed), Aug 29 (IHSG plunge), Aug 30 (politicians targeted).

**Observation:** The spike in tweet volume and sentiment coincides with the largest IHSG drop on Aug 29 — the crisis day dominates the time series.

---

## Slide 12 — Limitations

| Limitation | Detail |
|---|---|
| **Single event, single country** | External validity limited to Indonesian political crises |
| **Short event window (31 trading days)** | Limits power for lagged analysis and Granger causality |
| **Twitter sample bias** | Users self-select; not representative of general population |
| **Same-day correlation** | Cannot distinguish sentiment→returns from returns→sentiment or third-factor→both |
| **GPT-5 labeling is prompt-dependent** | No inter-rater benchmark on the protest tweet corpus; heuristic labeling |

## Slide 13 — Conclusion

1. **Statistically significant positive correlation** between GPT-5 sentiment and IHSG returns (r=+0.36, p=0.027, 95% CI [+0.04, +0.61])
2. **Correlation persists after the event** — After Demo period r=+0.53 (p=0.043), suggesting sustained sentiment-market alignment
3. **USD/IDR shows weaker inverse relationship** (r=−0.25, p=0.133) — not significant at α=0.05, consistent with additional macro-financial drivers
4. **GPT-5 produces clean, normal, stationary sentiment measures** — all diagnostic assumptions validated
5. **Findings are not driven by outliers** — only 3 flagged observations, all representing real market events
6. **Future work:** Apply GPT-5 sentiment with lagged/lead analysis across multiple event windows

---

## Slide 14 — Thank You

- Contact information
- GitHub repository: `github.com/theonegareth/twitter_sentiment_analysis`
- Full analysis pipeline and all data publicly available

---

## Backup Slides (7)

Present only if asked during Q&A.

### Backup A — Full Normality Test Results

**All 3 variables pass normality at α=0.05.**

| Variable | SW p | JB p | DA p | KS p | 3/4+ Pass? |
|---|---|---|---|---|---|
| Net Sentiment (GPT-5) | 0.237 | 0.296 | 0.175 | — | **Normal** ✅ |
| IHSG Return (%) | 0.500 | 0.868 | 0.714 | — | **Normal** ✅ |
| USD/IDR Return (%) | 0.189 | 0.426 | 0.241 | — | **Normal** ✅ |

**Source:** `gpt5_diagnostics.md`

---

### Backup B — Full Stationarity Test Results

| Variable | ADF p | KPSS p | Consensus |
|---|---|---|---|
| Net Sentiment (GPT-5) | 0.022 | 0.10 | **Stationary** ✅ |
| IHSG Daily Return (%) | <0.001 | 0.10 | **Stationary** ✅ |
| USD/IDR Daily Return (%) | <0.001 | 0.06 | **Stationary** ✅ |

Joint ADF+KPSS consensus: all variables are stationary. No differencing needed.

**Source:** `stationarity_test_report.md`

---

### Backup C — Outlier Dates Detail

**Only 3 outlier observations** across all variables. Detection: IQR (1.5x) + Z-Score (|Z| > 2.5).

| Date | Variable | Value | Direction | Context |
|---|---|---|---|---|
| Aug 29 | Net Sentiment (GPT-5) | −0.663 | LOW | Peak crisis — IHSG plunge |
| Aug 12 | IHSG Return (%) | +2.44% | HIGH | Pre-protest rally |
| Aug 14 | USD/IDR Return (%) | −0.86% | LOW | Rupiah strengthening anomaly |

All 3 correspond to real market events, not measurement error. Removing them has minimal impact on correlations.

**Source:** `gpt5_diagnostics.md`

---

### Backup D — GPT-5 Data Summary (38 paired days)

| Variable | N | Mean | SD | Skew | SW p | Normal? | ADF p | Stationary? |
|---|---|---|---|---|---|---|---|---|
| Net Sentiment (GPT-5) | 38 | −0.14 | 0.23 | −0.28 | 0.237 | Normal | 0.022 | Stationary |
| IHSG Return (%) | 38 | +0.08 | 0.84 | +0.09 | 0.500 | Normal | <0.001 | Stationary |
| USD/IDR Return (%) | 38 | +0.02 | 0.30 | −0.40 | 0.189 | Normal | <0.001 | Stationary |

All variables pass normality and stationarity. Pearson r is the appropriate correlation measure.

**Source:** `gpt5_diagnostics.md`

---

### Backup E — GPT Model Benchmark

Prior validation: GPT-5 vs. GPT-4.1 on 440 labeled Indonesian tweets (COVID-19 PPKM sentiment dataset).

| Model | Sentiment Accuracy | Emotion Accuracy |
|---|---|---|
| GPT-5 (best run) | **87.05%** | **76.59%** |
| GPT-4.1 | 83.41% | 72.27% |
| GPT-4.1-mini | 83.41% | 70.91% |
| GPT-5-mini | 81.59% | 72.50% |
| GPT-5-nano | 75.68% | 60.45% |

**Implication:** GPT-based sentiment could substantially improve accuracy over VADER (English-only lexicon). Future work should apply GPT-5 to the market tweet corpus.

**Source:** `model_comparison_table.md`

---

### Backup F — Trading Day & Pairing Detail

| Metric | Count |
|---|---|
| Calendar days | 61 |
| Weekends | 18 |
| Public holiday (Sep 5) | 1 |
| Trading days | **42** |
| IHSG paired (market + tweets) | **26** |
| USD/IDR paired (market + tweets) | **26** |
| Combined unique dates | **28** |

Non-trading day treatment: weekends and holidays excluded from paired analysis. Weekend tweets can be analyzed via forward-fill or backward-fill (documented in `market_data_merge_analysis.md` §5).

---

### Backup G — Power Analysis

*With n=38, what can we detect?*

| Required r for 80% power (α=0.05) | n | Observed r | Detected? |
|---|---|---|---|
| n = 38 (full period) | r > 0.45 | r=0.36 (IHSG) | Close (power ~65%) |
| n = 38 (full period) | r > 0.45 | r=−0.25 (USD/IDR) | No (power ~30%) |

The IHSG correlation (r=+0.36) has ~65% power at n=38 — the finding is significant (p=0.027) but power is moderate. The USD/IDR correlation (r=−0.25) would require n ≥ 120 for 80% power — the negative finding should be interpreted as "no evidence" rather than "no relationship."

---

## Chart Reference

| Slide | Chart File | Description |
|---|---|---|
| 2 | `charts/06_event_timeline.png` | Annotated IHSG + protest events |
| 5–6 | `charts/01_scatter_net_sentiment_vs_returns.png` | Scatter + OLS regression + 95% CI |
| 7 | `charts/07_dual_market_comparison.png` | Dual-axis IHSG + USD/IDR overlay |
| 8 | `charts/04_period_correlation_comparison.png` | Bar chart: r by period |
| 10 | `charts/diagnostics/D03_boxplots_by_period.png` | Boxplots by period |
| 11 | `charts/02_ihsg_timeline_with_sentiment.png` | 4-panel IHSG timeline |
| Backup | `charts/diagnostics/D05_qq_plots_by_period.png` | 12-panel Q-Q grid |
| Backup | `charts/diagnostics/D06_pairwise_scatter_matrix.png` | 4×4 scatter matrix |
| Backup | `charts/diagnostics/D01_master_diagnostic_dashboard.png` | Full diagnostic dashboard |

## Key Tables Reference

| Slide | Source Document | Table |
|---|---|---|
| 3 (Data) | `market_data_merge_analysis.md` | Trading days + observations |
| 5–6 (Correlations) | `pearson_correlation_analysis.md` | Full correlation matrix |
| 8 (Per-period) | `pearson_correlation_analysis.md` | Per-period breakdown |
| 9 (Robustness) | `correlation_robustness.md` | 5-treatment comparison |
| 10 (Diagnostics) | `normality_test_report.md` + `stationarity_test_report.md` | Test tables |
| Backup A–B | `normality_test_report.md` + `stationarity_test_report.md` | Full results |
| Backup C | `outlier_diagnostics.md` | Outlier dates |
| Backup D | `diagnostic_summary_table.md` | Unified summary |

---

*Prepared for conference presentation. All data, scripts, and figures available in the GitHub repository.*
