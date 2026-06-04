# Market Data Merge Analysis

**Generated:** 2026-06-04  
**Period:** August 1 – September 30, 2025  
**Source:** Yahoo Finance (IHSG via `^JKSE`, USD/IDR via `USDIDR=X`) + scraped Twitter keyword CSV files

---

## Visualizations

![Event Timeline](charts/06_event_timeline.png)
*Figure 6: Annotated IHSG timeline with key protest events.*

![Dual Market Comparison](charts/07_dual_market_comparison.png)
*Figure 7: IHSG and USD/IDR overlaid — note the divergence during the Aug 29 crisis.*

---

## Trading Days

| Metric | Count |
|---|---|
| Calendar days (Aug 1 – Sep 30) | 61 |
| Standard business days (Mon–Fri) | 43 |
| Indonesian public holidays on weekdays | –1 |
| **Trading days** | **42** |

**Holiday deducted:** Maulid Nabi Muhammad SAW — September 5, 2025 (Friday). Independence Day (Aug 17) fell on Sunday and did not affect trading.

---

## IHSG — Paired Observations

| Metric | Count |
|---|---|
| Days with IHSG market data (Yahoo Finance) | 41 |
| Days with IHSG-related tweets (12 CSV files) | 41 |
| **Paired IHSG observations** (market + tweets on same day) | **26** |

## USD/IDR — Paired Observations

| Metric | Count |
|---|---|
| Days with USD/IDR market data (Yahoo Finance) | 43 |
| Days with USD/IDR-related tweets (5 CSV files) | 37 |
| **Paired USD/IDR observations** (market + tweets on same day) | **26** |

---

## Combined Analytical Observations

| Metric | Count |
|---|---|
| Unique IHSG + USD/IDR paired dates (union) | **28** |

---

## Final Summary

| Metric | Count |
|---|---|
| Trading days (Aug 1 – Sep 30, 2025) | **42** |
| Paired observations for IHSG | **26** |
| Paired observations for USD/IDR | **26** |
| Total combined analytical observations | **28** |

---

## Paired Date Detail

### IHSG (26 dates)

| Date | Day | Period |
|---|---|---|
| 2025-08-01 | Friday | Before Demo |
| 2025-08-04 | Monday | Before Demo |
| 2025-08-05 | Tuesday | Before Demo |
| 2025-08-06 | Wednesday | Before Demo |
| 2025-08-07 | Thursday | Before Demo |
| 2025-08-08 | Friday | Before Demo |
| 2025-08-11 | Monday | Before Demo |
| 2025-08-12 | Tuesday | Before Demo |
| 2025-08-13 | Wednesday | Before Demo |
| 2025-08-14 | Thursday | Before Demo |
| 2025-08-15 | Friday | Before Demo |
| 2025-08-19 | Tuesday | Before Demo |
| 2025-08-20 | Wednesday | Before Demo |
| 2025-08-21 | Thursday | Before Demo |
| 2025-08-22 | Friday | Before Demo |
| 2025-08-25 | Monday | **Demo** |
| 2025-08-26 | Tuesday | **Demo** |
| 2025-08-27 | Wednesday | **Demo** |
| 2025-08-28 | Thursday | **Demo** |
| 2025-08-29 | Friday | **Demo** |
| 2025-09-01 | Monday | **Demo** |
| 2025-09-02 | Tuesday | **Demo** |
| 2025-09-03 | Wednesday | **Demo** |
| 2025-09-04 | Thursday | **Demo** |
| 2025-09-26 | Friday | After Demo |
| 2025-09-29 | Monday | After Demo |

### USD/IDR (26 dates)

| Date | Day | Period |
|---|---|---|
| 2025-08-01 | Friday | Before Demo |
| 2025-08-04 | Monday | Before Demo |
| 2025-08-05 | Tuesday | Before Demo |
| 2025-08-06 | Wednesday | Before Demo |
| 2025-08-07 | Thursday | Before Demo |
| 2025-08-08 | Friday | Before Demo |
| 2025-08-11 | Monday | Before Demo |
| 2025-08-12 | Tuesday | Before Demo |
| 2025-08-13 | Wednesday | Before Demo |
| 2025-08-14 | Thursday | Before Demo |
| 2025-08-15 | Friday | Before Demo |
| 2025-08-18 | Monday | Before Demo |
| 2025-08-19 | Tuesday | Before Demo |
| 2025-08-20 | Wednesday | Before Demo |
| 2025-08-21 | Thursday | Before Demo |
| 2025-08-22 | Friday | Before Demo |
| 2025-08-25 | Monday | **Demo** |
| 2025-08-26 | Tuesday | **Demo** |
| 2025-08-27 | Wednesday | **Demo** |
| 2025-08-28 | Thursday | **Demo** |
| 2025-08-29 | Friday | **Demo** |
| 2025-09-01 | Monday | **Demo** |
| 2025-09-02 | Tuesday | **Demo** |
| 2025-09-03 | Wednesday | **Demo** |
| 2025-09-04 | Thursday | **Demo** |
| 2025-09-05 | Friday | **Demo** (Holiday) |

---

## Coverage Gap

Both IHSG and USD/IDR tweet coverage drops off after September 4–5, with no tweet data again until September 26. This aligns with `keyword_completeness_summary.csv`, which marks many financial keywords as **Incomplete** or **No Data Found** in the After Demo period (Sep 9–30).

The **Demo period** (Aug 25 – Sep 8) has 10 paired days for IHSG and 11 for USD/IDR. The **Before Demo** period (Aug 1–24) has 14–15 paired days each. **After Demo** (Sep 9–30) has only 2 paired IHSG days and 0 paired USD/IDR days due to incomplete scraping.

---

## Data Sources

| Source | Files Used |
|---|---|
| IHSG tweets | 12 CSV files (IHSG, bursa efek, saham turun/naik, jual saham, panic selling, asing cabut, foreign outflow, pasar keuangan) |
| USD/IDR tweets | 5 CSV files (nilai tukar, kurs rupiah, melemah, menguat) |
| Market data | Yahoo Finance (`^JKSE`, `USDIDR=X`) |

**Analysis script:** `market_data_merge_analysis.py`

---

## Treatment of Non-Trading Days and Missing Data

### 1. Definition of Non-Trading Days

A **non-trading day** is any calendar date where the Indonesia Stock Exchange (IDX) is closed and no market price data is available from Yahoo Finance. In this dataset, non-trading days fall into two categories:

| Category | Dates | Count |
|---|---|---|
| **Weekends** (Saturday–Sunday) | Every Sat/Sun, Aug 1 – Sep 30 | 18 |
| **Public holidays on weekdays** | Sep 5 (Maulid Nabi Muhammad SAW) | 1 |
| **Total non-trading days** | | **19** |

These 19 non-trading days + 42 trading days = 61 calendar days.

### 2. Why Non-Trading Days Matter

Twitter operates 24/7. Tweets about IHSG, USD/IDR, and market sentiment are posted on weekends and holidays, but there is **no corresponding market price movement** on those days. This creates an alignment problem for any regression or time-series analysis that pairs tweet sentiment with market returns.

### 3. Types of Missing Data

The dataset contains two distinct kinds of absence:

#### 3a. Structural Absence: Non-Trading Days (Weekends + Holidays)

- **Market data:** Always absent (market closed). Yahoo Finance returns no row for these dates.
- **Tweet data:** May or may not be present. Our scrapers collected tweets on weekends/holidays because the Twitter API returns `created_at` timestamps for all calendar days.
- **Pairing result:** These dates are automatically excluded from paired observations since market data is missing.

#### 3b. Contingent Absence: Scraping Gaps (Incomplete Coverage)

- **Market data:** Present (market open).
- **Tweet data:** Missing because the keyword was not scraped for that date range.
- **Pairing result:** These trading days are excluded from paired observations, reducing the usable N.

### 4. Breakdown by Period

#### Before Demo (Aug 1–24, 2025) — 17 trading days

| | IHSG | USD/IDR |
|---|---|---|
| Trading days in period | 17 | 17 |
| Days with market data | 16 | 17 |
| Days with tweet data | 17 | 17 |
| **Paired observations** | **14** | **15** |
| Trading days lost to scrape gap | 2 (Aug 18 missing) | 1 |
| Non-trading days in period | 7 (weekends) | 7 (weekends) |

**Missing IHSG dates (market data absent):** Aug 18 — Yahoo Finance did not return a row. This may be a data feed gap rather than an actual market closure.

#### Demo (Aug 25 – Sep 8, 2025) — 11 trading days

| | IHSG | USD/IDR |
|---|---|---|
| Trading days in period | 11 | 11 |
| Days with market data | 11 | 11 |
| Days with tweet data | 10 | 11 |
| **Paired observations** | **10** | **11** |
| Trading days lost to scrape gap | 1 (Sep 5 holiday, no tweets scraped) + 1 (IHSG: Sep 8 missing) | 0 |
| Non-trading days in period | 4 (weekends + Sep 5 holiday) | 4 |

**Note:** Sep 5 appears in the USD/IDR paired list because Yahoo Finance returned data for USDIDR=X (forex trades globally), but IDX was closed for the holiday. For IHSG, Sep 5 is absent from market data as expected. Additionally, IHSG tweet scraping on Sep 8 is missing.

#### After Demo (Sep 9–30, 2025) — 14 trading days

| | IHSG | USD/IDR |
|---|---|---|
| Trading days in period | 14 | 14 |
| Days with market data | 14 | 15 (forex includes some weekends) |
| Days with tweet data | 2 | 0 |
| **Paired observations** | **2** | **0** |
| Trading days lost to scrape gap | 12 | 14 |
| Non-trading days in period | 8 (weekends) | 8 |

**This is the critical gap.** Tweet scraping for most financial keywords was not executed for the After Demo period. Only Sep 26 and Sep 29 have IHSG tweets. USD/IDR keywords have zero tweet coverage in this period.

### 5. Treatment Options

Depending on the analytical goal, choose one or more of the following:

#### Option A: Forward-Fill Market Returns Across Non-Trading Days

Assign Friday's market return to Saturday and Sunday tweets. This is standard in event studies where social media engagement accumulates over the weekend but is presumed to reflect Friday's price action.

- **Strength:** Preserves all tweet data. Maximizes N.
- **Weakness:** Assumes weekend sentiment is driven by Friday's close, which may not hold if news breaks Saturday.

#### Option B: Backward-Fill Market Returns (Monday Attribution)

Assign Monday's market return to weekend tweets. This treats weekend social media as *anticipatory* of Monday's open.

- **Strength:** Captures forward-looking sentiment (traders positioning over the weekend).
- **Weakness:** Causality is questionable — weekend tweets may *respond* to Monday's open, not predict it.

#### Option C: Exclude Weekends Entirely (Conservative)

Drop all tweets posted on Saturday and Sunday. Only use trading-day tweets matched to same-day market data.

- **Strength:** Cleanest causal alignment. No assumptions about weekend information flow.
- **Weakness:** Loses 18 days of potential tweet data from the 61-day window.

#### Option D: Weekend Aggregation (Pooled Sentiment)

Aggregate all weekend tweets into a single weekend-level observation. Assign the Friday→Monday overnight return as the dependent variable.

- **Strength:** Reduces noise from low-volume weekend tweet days.
- **Weakness:** Collapses multiple days into one observation, reducing granularity.

#### Option E: For the After Demo Scraping Gap

The After Demo period (Sep 9–30) has effectively no paired observations. Options:

1. **Exclude from market-sentiment analysis entirely.** The period cannot be analyzed with the current data. Report as a data limitation.
2. **Re-scrape missing keywords.** The `keyword_completeness_summary.csv` and `parsed_tweet_filenames_sorted.csv` identify exact date ranges and keywords that need scraping. This would recover up to 14 additional paired trading days.
3. **Use aggregate market returns only.** If tweet data cannot be recovered, the After Demo period can still be used for descriptive market statistics (mean IHSG return, volatility, etc.) without tweet-sentiment pairing.

### 6. Recommended Protocol

For a publishable event study, the recommended treatment is:

| Issue | Recommendation |
|---|---|
| Weekends (18 days) | **Option C — Exclude.** Sentiment analysis pairs only trading-day tweets with same-day market returns. |
| Holiday (Sep 5) | Exclude from IHSG pairing (market closed). USD/IDR forex data is available if cross-market analysis is needed. |
| After Demo scrape gap | **Option E.2 — Re-scrape** if budget/time permits. Otherwise **E.1 — Exclude** and flag as limitation. |
| IHSG market data gap (Aug 18) | Investigate — may be a Yahoo Finance artifact. If irrecoverable, forward-fill from Aug 15 or exclude. |

### 7. Impact on Final N

After applying the recommended protocol (exclude weekends, exclude After Demo gap pending re-scrape):

| Period | Trading Days | Paired (IHSG) | Paired (USD/IDR) |
|---|---|---|---|
| Before Demo (Aug 1–24) | 17 | 14 | 15 |
| Demo (Aug 25 – Sep 8) | 11 | 10 | 11 |
| After Demo (Sep 9–30) | 14 | **2** (gap) | **0** (gap) |
| **Usable total** | **42** | **24** (26 excluding gap) | **26** (excluding gap) |

**Minimum viable N for regression:** ~10 observations per period. The Before and Demo periods each clear this threshold. The After Demo period does not, and must be excluded or re-scraped.
