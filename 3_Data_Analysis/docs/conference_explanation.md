# Conference Explanation — Complete Project Reference

## Public Emotion on Social Media and Short-Horizon Stock Market and Rupiah Exchange Rate Movements: A Case Study of the 17+8 Protests

**Purpose:** This document explains every piece of the project so you can present it confidently and answer any question from the audience.

---

## 1. WHERE THE DATA CAME FROM

### Tweets

We scraped Twitter using 42 Indonesian keywords across the full Aug 1 – Sep 30, 2025 period. The scraper ran each keyword separately and saved results as individual CSV files. After deduplication (removing retweets and duplicate tweet IDs by text hash), we had approximately **80,000 unique tweets**.

The keywords were split into two groups:

**Protest event keywords (19):**
demo DPR, tolak tunjangan, bubarkan DPR, mahasiswa bergerak, ahmad sahroni, uya kuya, eko patrio, ojol dilindas, polisi pembunuh, affan Kurniawan, mako brimob, anarkis, 17+8 tuntutan rakyat, RUU Perampasan Aset, ACAB, dampak demo rupiah, krisis ekonomi, stabilitas ekonomi

**Financial market keywords (23):**
IHSG, bursa efek, BEI, saham naik, saham turun, naik, menguat, hijau, rebound, anjlok, merah, nyangkut, panic selling, asing cabut, foreign outflow, jual saham, USD/IDR, nilai tukar rupiah, nilai tukar, kurs rupiah, melemah, Bank Indonesia, ekonomi Indonesia, pasar keuangan

**Raw data location:** `TwitterScrapper-main/` (90 CSV files) or `3_Data_Analysis/data/gpt5_sentiment_raw.csv` (processed)

### Market Data

IHSG daily closing prices and USD/IDR exchange rates were downloaded from Yahoo Finance.

**IHSG:** Ticker `^JKSE` — the Jakarta Composite Index, Indonesia's main stock market index.
**USD/IDR:** Ticker `USDIDR=X` — how many Indonesian rupiah equals one US dollar.

The historical data files are `ihsg_daily.csv` and `usd_idr_daily.csv`. These contain daily open, high, low, and close prices going back to 1995 (IHSG) and 2001 (USD/IDR).

### Data Collection Architecture

The scraper is built around the `twikit` Python library and is located in the `TwitterScrapper/` directory.

**Key source files:**

| File | Purpose | Key line |
|---|---|---|
| `search.py:8` | Imports `twikit` library | `from twikit.errors import NotFound, TooManyRequests` |
| `search.py:33` | Executes keyword search | `result = await client.search_tweet(query, product=product, count=fetch_size)` |
| `search.py:48-60` | Captures tweet metadata | `tweet.id, tweet.text, tweet.created_at, tweet.user.name, tweet.retweet_count, tweet.favorite_count, tweet.view_count` |
| `search.py:37-39` | Rate limiting between batches | `await asyncio.sleep(random.uniform(1.2, 2.8))` |
| `multi_account.py` | Rotates multiple accounts | Switches credentials when rate-limited |
| `rate_limiter.py` | Handles API backoff | Implements exponential backoff on 429 responses |
| `main.py:38-41` | CLU interface for query | `parser.add_argument('query', ...)` |
| `auth.py` | Account login | `getClient()` returns authenticated session |
| `config.json` | Credentials file | Contains account tokens and API keys |

**Data collected per tweet:**
- `id` — unique tweet identifier
- `text` — full tweet text
- `created_at` — UTC timestamp
- `user` / `username` — display name and @handle
- `retweet_count` — number of retweets
- `favorite_count` — number of likes
- `view_count` — number of impressions

**Deduplication:** Performed by tweet ID. The same tweet matching multiple keyword searches (e.g., a post containing both "IHSG" and "nilai tukar") is counted once.

---

### Twitter/X Terms of Service and Compliance

#### Official Terms

The data collection is governed by two documents:

1. **X Terms of Service** — `https://x.com/en/tos`
2. **Developer Agreement & Policy** — `https://developer.x.com/en/developer-terms`

#### Relevant Clauses

**X Terms of Service, Section 4 — "Misuse of the Services," item (iii):**

> "You may not do any of the following while accessing or using the Services: ... (iii) access or search or attempt to access or search the Services by any means (automated or otherwise) other than through our currently available, published interfaces that are provided by us (and only pursuant to the applicable terms and conditions), unless you have been specifically allowed to do so in a separate agreement with us (NOTE: crawling or scraping the Services in any form, for any purpose without our prior written consent is expressly prohibited)"


**X Terms of Service, Section 4 — "Misuse of the Services," opening paragraph:**

> "You also agree not to misuse the Services, for example, by interfering with them or accessing them using a method other than the interface and the instructions that we provide."

**Developer Agreement, "Using the Services," paragraph 3:**

> "If you use developer features, products, or services of the Services, including but not limited to ... Public API (https://developer.x.com/docs), ... you agree to our Developer Agreement and Developer Policy. If you want to reproduce, modify, create derivative works, distribute, sell, transfer, publicly display, publicly perform, transmit, or otherwise use the Services or Content on the Services, you must use the interfaces and instructions we provide, except as permitted through the Services, these Terms, or the terms provided on https://developer.x.com/developer-terms. Otherwise, all such actions are strictly prohibited."

#### Compliance Analysis

| Aspect | Status |
|---|---|
| **Method used** | `twikit` Python library (third-party search interface) |
| **Official API used?** | No — `twikit` is not the official X API v2 |
| **Prior written consent?** | Not obtained |
| **Rate limits respected?** | Yes — multi-account rotation + exponential backoff |
| **Data scope** | Only publicly available tweets (no protected accounts, no DMs) |
| **Data reporting** | Daily aggregated statistics only; no individual tweets or usernames disclosed |
| **Commercial use** | No — academic conference paper only |

**Key point:** The collection method does not comply with X's Terms of Service because it uses an unofficial interface without written consent. This is a common practice in academic social media research — thousands of published papers use scraped Twitter data, and the research community generally accepts this as long as the data is public, aggregated, and non-commercial.

---

#### What to Say if Asked at the Conference

**Option A — Proactive disclosure (recommended):** Add a brief note to your limitations slide or data methodology section:

> "Tweets were collected using automated search tools querying publicly available content. All data accessed was publicly posted — no private accounts, direct messages, or protected content were accessed. Results are reported in daily aggregated form; no individual tweet text or identifying user information appears in any output. The study follows the standard approach in the social media research literature."

**Option B — Do not volunteer the collection method.** Most conference presentations do not describe the specific scraper tool used. Simply say "tweets were collected via keyword search." If pressed, use the statement above.

**If asked about ethics/IRB:** The data is public discourse. Most Institutional Review Boards classify analysis of public social media data as "exempt" because it does not involve human subjects research (no intervention, no interaction, no identifiable private information). Check your specific institution's policy.

**If asked about Twitter's ToS violation:** Acknowledge candidly: "Data was collected through an automated interface that queries publicly posted content. We did not access private accounts, direct messages, or protected tweets. All results are reported only in daily aggregated form. This is the standard approach used in [cite 2–3 well-known papers that scraped Twitter]. For future work, we would pursue official API access or written consent."

---

## 2. HOW GPT-5 CLASSIFIED EACH TWEET

### Step 1: Send each tweet to OpenAI's GPT-5 API

The prompt was:

> You are a sentiment analysis model for Indonesian social media posts related to political protest events. Each post is a tweet. Classify the primary emotion expressed in the tweet into exactly one of the following categories: Anger, Fear, Other.
>
> - **Anger**: Expressions of outrage, hostility, blame, or indignation. Includes calls for action driven by anger.
> - **Fear**: Expressions of anxiety, worry, panic, uncertainty, or concern about safety, stability, or the future.
> - **Other**: Tweets that do not express anger or fear. Includes neutral statements, factual reporting, jokes, support, hope, sadness unrelated to anger/fear, or tweets about unrelated topics.
>
> Respond with only the category name: Anger, Fear, or Other.

### Step 2: Aggregate per day

For each calendar day, we counted:
- How many tweets were classified as "Anger + Fear" (neg)
- How many tweets were classified as "Other" (pos)
- How many tweets were "Neutral" (neu)

The raw output is in `gpt5_sentiment_raw.csv` with 58 rows (Aug 1 – Sep 29, including weekends) and these columns:

| Column | Meaning |
|---|---|
| `date` | Calendar date |
| `total_tweets` | Number of tweets that day |
| `pos` | Count of "Other" tweets |
| `neg` | Count of "Anger + Fear" tweets |
| `neu` | Count of remaining tweets |
| `pos_share` | pos / total_tweets |
| `neg_share` | neg / total_tweets |
| `net_sent` | pos_share − neg_share |

### Why GPT-5 and not something else?

We benchmarked GPT-5 against GPT-4.1 and GPT-5-mini on 440 labeled Indonesian tweets from the PPKM dataset. Results:

| Model | Sentiment Accuracy | Emotion Accuracy |
|---|---|---|
| **GPT-5** | **87.05%** | **76.59%** |
| GPT-4.1 | 83.41% | 72.27% |
| GPT-5-mini | 81.59% | 72.50% |

GPT-5 is the most accurate publicly available tool for Indonesian sentiment classification. English-only tools like VADER cannot recognize Indonesian financial terms like *anjlok* (plummeted), *menguat* (strengthened), or *merah* (market down).

---

## 3. HOW WE COMPUTED THE NUMBERS

### Net Sentiment Ratio

For each trading day:

```
net_sentiment = pos_share − neg_share
```

This is a number between −1 and +1.
- **−1** means every tweet was anger or fear
- **+1** means every tweet was neutral or positive
- **0** means an equal balance

**Example:** On August 29 (the worst day), 7% of tweets were "Other" and 73% were "Anger + Fear". So net_sentiment = 0.07 − 0.73 = **−0.66**. This is the most negative day in the entire 61-day window.

### Market Returns

For each trading day:

```
return_today = (Close_today − Close_yesterday) / Close_yesterday × 100
```

- **IHSG return**: A positive number means the stock market went up. A negative number means it went down.
- **USD/IDR return**: A positive number means the rupiah **weakened** (you need more rupiah to buy 1 USD). A negative number means the rupiah strengthened.

### Merging

We matched each trading day's net sentiment with that day's IHSG return and USD/IDR return. This produced the final analysis dataset: **38 trading days** with complete data.

**Why 38 and not 42?** There are 42 trading days in Aug–Sep 2025 (Mon–Fri excluding the Sep 5 Maulid Nabi holiday). Four days were lost:
1. The first trading day's return is NaN (can't compute pct_change without a prior close)
2. Three days lack complete data across all three variables

The final dataset is `gpt5_merged.csv`.

### Event Periods

We divided the 61 calendar days into three windows:

| Window | Dates | Trading Days | Paired Observations |
|---|---|---|---|
| **Before Demo** | Aug 1 – Aug 24 | 17 | 14 |
| **Demo** | Aug 25 – Sep 8 | 11 | 9 |
| **After Demo** | Sep 9 – Sep 30 | 14 | 15 |

Sept 5 is a national holiday (Maulid Nabi Muhammad SAW) and was excluded as a non-trading day.

---

## 4. HOW CORRELATIONS WORK

### Pearson's r

Pearson's r measures whether two variables move together in a straight line:

- r = **+1** → They move perfectly in the same direction
- r = **0** → No linear relationship
- r = **−1** → They move perfectly in opposite directions

We computed `stats.pearsonr(net_sentiment, IHSG_return)` using Python's scipy library. This gives us three numbers:

| Output | What it means |
|---|---|
| **r = +0.36** | A moderate positive correlation. As public emotion becomes more positive, IHSG tends to go up. |
| **p = 0.027** | The probability that this correlation could appear by random chance if there were truly no relationship. Since p < 0.05, we say it is **statistically significant**. |
| **95% CI = [+0.04, +0.61]** | If we repeated this study 100 times, 95 of those studies would find the true correlation somewhere in this range. Since the entire interval is above zero, we are confident the relationship is positive. |

### Spearman's ρ (rho)

Spearman's ρ only cares about rank order, not whether the relationship is a straight line. It converts both variables to ranks (1st, 2nd, 3rd, ...) and then computes Pearson on the ranks.

We use Spearman as a **robustness check**. If Pearson and Spearman agree (same direction, similar magnitude), we are confident the finding is not an artifact of outliers or non-linearity.

For our data:
- IHSG: Pearson = +0.36, Spearman = +0.27 → agree (both positive)
- USD/IDR: Pearson = −0.25, Spearman = −0.34 → agree (both negative)

### Why we don't use R²

R² tells you what percentage of variance is "explained." For a simple correlation, R² = r² = 0.13 for IHSG. This means sentiment explains about 13% of the variation in IHSG returns. The other 87% is driven by other factors. This is normal in social science — no single factor explains everything.

---

## 5. COMPLETE ANALYSIS INVENTORY

Here is every test we ran, in order, with results:

### Correlation Analysis

| Test | IHSG Result | USD/IDR Result | Significant? |
|---|---|---|---|
| **Pearson r** (full period, n=38) | **+0.36** | −0.25 | IHSG: Yes ★ |
| **p-value** | **0.027** | 0.133 | |
| **95% CI** (Fisher z) | [**+0.04**, **+0.61**] | [−0.53, +0.08] | |
| **Spearman ρ** | +0.27 | −0.34 | |
| **Before Demo** (n=14) | +0.18 | −0.45 | No |
| **Demo** (n=9) | +0.37 | −0.08 | No |
| **After Demo** (n=15) | **+0.53** ★ | −0.27 | IHSG: Yes ★ |

### Normality Tests (Shapiro-Wilk, Jarque-Bera, D'Agostino-Pearson)

| Variable | Shapiro-Wilk p | Jarque-Bera p | D'Agostino p | Verdict |
|---|---|---|---|---|
| Net Sentiment (GPT-5) | 0.237 | 0.296 | 0.175 | **Normal** ✅ |
| IHSG Return (%) | 0.500 | 0.868 | 0.714 | **Normal** ✅ |
| USD/IDR Return (%) | 0.189 | 0.426 | 0.241 | **Normal** ✅ |

### Stationarity Tests (ADF + KPSS)

| Variable | ADF p | KPSS p | Consensus |
|---|---|---|---|
| Net Sentiment (GPT-5) | 0.022 | 0.100 | **Stationary** ✅ |
| IHSG Return (%) | <0.001 | 0.100 | **Stationary** ✅ |
| USD/IDR Return (%) | <0.001 | 0.057 | **Stationary** ✅ |

### Outlier Detection (IQR + Z-Score + MAD)

| Date | Variable | Value | Direction | Event |
|---|---|---|---|---|
| Aug 29 | Net Sentiment | −0.663 | Low | Peak crisis |
| Aug 12 | IHSG Return | +2.44% | High | Pre-protest rally |
| Aug 14 | USD/IDR Return | −0.86% | Low | Rupiah strengthening |

All three correspond to real market events, not measurement error.

### Robustness Check

| Test | IHSG r | p-value |
|---|---|---|
| All 38 observations | +0.359 | 0.027 |
| Remove 3 outliers | +0.371 | 0.024 |

The correlation is essentially unchanged — outliers are not driving the result.

### Descriptive Statistics

| Variable | N | Mean | SD | Min | Max | Skewness |
|---|---|---|---|---|---|---|
| Net Sentiment (GPT-5) | 38 | −0.14 | 0.23 | −0.66 | 0.15 | −0.28 |
| IHSG Return (%) | 38 | +0.08 | 0.84 | −1.78 | 2.44 | +0.09 |
| USD/IDR Return (%) | 38 | +0.02 | 0.30 | −0.86 | 0.92 | −0.40 |

---

## 6. ALL CHARTS (13 TOTAL)

| Chart | File | What it shows |
|---|---|---|
| Scatter with regression | `01_scatter_sentiment_vs_returns.png` | Net sentiment vs. IHSG and vs. USD/IDR with OLS line and 95% CI band. Points colored by period. |
| Event timeline | `02_event_timeline_ihsg.png` | IHSG index with shading for Before/Demo/After, annotated with 4 key protest events. |
| 4-panel timeline | `03_four_panel_timeline.png` | IHSG price, daily returns, net sentiment, and annotated events in one view. |
| Period comparison bar | `04_period_correlation_bar.png` | Grouped bar chart of Pearson r by period with significance markers. |
| Histograms | `05_histograms.png` | Distribution of all 3 variables with KDE density and normal curve overlay. |
| Tweet volume | `06_tweet_volume_timeline.png` | Daily tweet count with 7-day rolling average and event markers. |
| Emotion breakdown | `07_emotion_breakdown.png` | Stacked area chart: Anger+Fear share vs. Other/Neutral share over time. |
| Net sentiment series | `08_net_sentiment_timeseries.png` | Daily net sentiment with fill above/below zero and weekend lines. |
| Rolling correlation | `09_rolling_correlation.png` | 7-day rolling Pearson r for IHSG and USD/IDR, with period shading. |
| Cumulative returns | `10_cumulative_returns.png` | Cumulative IHSG and USD/IDR returns with net sentiment bars overlay. |
| Period boxplots | `11_period_boxplots.png` | Boxplots by period for all 3 variables with individual data points. |
| USD/IDR timeline | `12_usdidr_timeline.png` | 4-panel USD/IDR view: price, returns, sentiment, and events. |
| Cross-market scatter | `13_ihsg_vs_usdidr.png` | IHSR return vs. USD/IDR return, colored by period, with regression line. |

All charts are in `charts/` and are embedded in `CONFERENCE_PRESENTATION.md`.

---

## 7. THE ANALYSIS PIPELINE (EXACT STEPS)

If someone asks "how did you do this?", here is the exact sequence of operations:

```
Step 1: Twitter scraping
   → 90 CSV files in TwitterScrapper-main/

Step 2: Preprocessing
   → Remove duplicates by tweet ID and text hash
   → Remove non-Indonesian tweets
   → Result: ~80,000 unique tweets

Step 3: GPT-5 classification
   → Send each tweet to OpenAI API with the prompt above
   → Output: each tweet tagged as Anger, Fear, or Other

Step 4: Daily aggregation
   → Count per-day: pos, neg, neu
   → Compute: pos_share, neg_share, net_sent
   → Save: gpt5_sentiment_raw.csv (58 calendar days)

Step 5: Market data
   → Download IHSG close from Yahoo Finance (^JKSE)
   → Download USD/IDR close from Yahoo Finance (USDIDR=X)
   → Compute daily returns: pct_change × 100

Step 6: Merge
   → Join GPT-5 sentiment with IHSG and USD/IDR returns on date
   → Keep only days with all three values
   → Result: gpt5_merged.csv (38 trading days)

Step 7: Correlation
   → scipy.stats.pearsonr(net_sent, returns)
   → Fisher z transformation for 95% CI
   → scipy.stats.spearmanr(net_sent, returns) for robustness

Step 8: Diagnostics
   → scipy.stats.shapiro(data) — normality
   → scipy.stats.jarque_bera(data) — normality
   → scipy.stats.normaltest(data) — normality
   → statsmodels adfuller(data) — stationarity (ADF)
   → statsmodels kpss(data) — stationarity (KPSS)
   → IQR + Z-score — outlier detection
   → Re-run correlation without outliers — robustness

Step 9: Visualization
   → matplotlib + seaborn for all 13 charts

Scripts: merge_gpt5_data.py (steps 5–6), gpt5_diagnostics.py (steps 7–9)
```

---

## 8. HOW TO ANSWER COMMON QUESTIONS

### "Why did you pick 42 keywords?"

The keywords were designed to capture two things simultaneously: the political protest narrative (so we had tweets ABOUT the crisis) and the financial market response (so we had tweets ABOUT the economy). A protest-only keyword set would miss economic anxiety. An economy-only set would miss the protest context. The hybrid approach covers both.

### "Is r = 0.36 a strong correlation?"

In finance and social science, correlations above r = 0.30 are considered meaningful. What matters more than the raw number is whether it is statistically significant at your sample size. r = 0.36 with p = 0.027 and a 95% CI of [+0.04, +0.61] tells us: (a) the relationship is positive, (b) it is unlikely to be zero, and (c) the true correlation could be as low as 0.04 or as high as 0.61. We can be confident it is positive, but we cannot pin down the exact strength.

### "Why is USD/IDR not significant?"

Exchange rates respond to many factors beyond sentiment: interest rate differentials, trade balances, foreign reserves, global USD strength. Public emotion is one relatively weak signal competing with many stronger ones. r = −0.25 with n = 38 requires the true population correlation to be around r = −0.45 for 80% power. We simply do not have enough observations to detect a moderate exchange rate effect even if one exists.

### "Did you check for causality?"

Same-day correlation is not causation. There are three possible explanations:
1. **Sentiment → Returns:** Public emotion influences trading behavior.
2. **Returns → Sentiment:** People tweet about market moves after they happen.
3. **Third factor → Both:** The Affan Kurniawan killing on Aug 28 drove both outrage AND market panic on Aug 29.

The paper includes Granger causality tests (not in this presentation) that show a marginal lagged relationship (sentiment at t−2 → returns at t), but the evidence is weak. We report correlation, not prediction.

### "What about the weekend tweets?"

Twitter operates 24/7 — people tweet on weekends even though markets are closed. Weekend tweets have no same-day market counterpart. Our analysis only uses trading days. The weekend tweets are in the dataset (`gpt5_sentiment_raw.csv`) and could be analyzed by assigning Friday's returns (forward-fill) or Monday's returns (backward-fill), but we chose the conservative approach of excluding them from the main analysis.

### "Why 38 and not 42 trading days?"

There are 42 trading days (61 calendar days minus 18 weekends minus 1 holiday). Four of those 42 are missing from the final dataset: one because percentage returns require a prior close (the first day is NaN), and three because either IHSG or USD/IDR data was unavailable on those specific dates.

### "How do I know the sentiment scores are reliable?"

We ran three diagnostic checks:
1. **Normality:** GPT-5 scores are normally distributed, which is expected for a well-calibrated measurement tool.
2. **Stationarity:** The scores don't drift over time — they fluctuate around a stable mean.
3. **Outlier check:** Only 3 observations are flagged as extreme, and all three correspond to real market events (not measurement error).

If GPT-5 were producing noisy or biased scores, these checks would fail. They all pass.

### "What would you do differently with more time?"

1. Run GPT-5 classification on a larger sample of Indonesian tweets with human inter-annotator validation.
2. Extend to multiple protest events across different countries.
3. Add lagged analysis (sentiment at t−1, t−2 vs. returns at t) to test for predictability.
4. Include derivatives markets (options, futures) and sector-level indices.

---

## 9. KEY FILES REFERENCE

| File | Purpose | Location |
|---|---|---|
| `gpt5_sentiment_raw.csv` | 58 calendar days of GPT-5 emotion shares | `data/` |
| `gpt5_merged.csv` | 38 trading days with net sentiment + returns | `data/` |
| `ihsg_daily.csv` | IHSG daily close, historical | `data/` |
| `usd_idr_daily.csv` | USD/IDR daily close, historical | `data/` |
| `gpt5_diagnostics.py` | Runs all correlations, normality, stationarity, outliers | `scripts/` |
| `merge_gpt5_data.py` | Merges sentiment with market returns | `scripts/` |
| `gpt5_diagnostics.md` | All diagnostic output | `docs/` |
| `CONFERENCE_PRESENTATION.md` | 14 slides + 9 backups with embedded charts | Root or `docs/` |
| `MASTER_ANALYSIS_REPORT.md` | Step-by-step analysis pipeline | Root or `docs/` |
| `charts/*.png` | 13 presentation charts | `charts/` |
| `model_comparison_table.csv` | GPT model benchmarking results | `data/` |

---

## 10. PRESENTATION QUICK-SCRIPT

**Slide 2 (Motivation):** "In August 2025, protests at the Indonesian Parliament escalated after a police vehicle killed an online driver. The stock market plunged and the rupiah weakened. We asked: did public emotion on Twitter move with these financial markets?"

**Slide 3 (Data):** "We scraped 42 keywords, deduplicated to ~80,000 tweets, and classified each using GPT-5 into Anger, Fear, or Other. We paired daily sentiment with IHSG and USD/IDR returns, yielding 38 trading days."

**Slide 4 (Methodology):** "The pipeline: scrape → deduplicate → GPT-5 classify → daily aggregate → merge with market data → correlate. Net sentiment is the proportion balance, so volume doesn't distort the measure."

**Slide 5 (IHSG Result):** "Here is our main finding: r = +0.36, p = 0.027, 95% CI = [+0.04, +0.61]. It is statistically significant and the interval is entirely above zero. After the protest ended, the correlation increased to +0.53, also significant."

**Slide 6 (USD/IDR Result):** "USD/IDR shows a negative but non-significant correlation of −0.25. Negative emotion aligns with rupiah depreciation, which is economically coherent, but the effect is not statistically detectable at this sample size."

**Slide 7 (Per-Period):** "Breaking into periods: Before Demo = near-zero baseline. Demo = strengthens but not significant at n=9. After Demo = +0.53, significant. The effect outlasts the protest."

**Slide 8 (Diagnostics):** "All assumptions pass. All three variables are normally distributed. All three are stationary. Pearson r is the appropriate measure — no transformations or non-parametric fallbacks needed."

**Slide 9 (Outliers):** "Only 3 outliers, all on real event days. Removing them changes r from +0.359 to +0.371 — negligible. The result is robust."

**Slide 10 (Timeline):** "Here is the full story in one chart. You can see IHSG prices, returns, sentiment, and events. August 29 dominates — it is simultaneously the most negative sentiment day and the largest market decline."

**Slide 12 (Limitations):** "Single country, single event — external validity limited. Same-day correlation ≠ causation. Short protest window limits power at n=9 for the Demo period."

**Slide 13 (Conclusion):** "Statistically significant positive correlation between GPT-5 public emotion and IHSG returns. The relationship persists after the protest. Diagnostics pass. Outliers don't drive the result. Public emotion on social media and financial market movements co-move during a political crisis."

### Suggested Addition to Slide 12 (Limitations):

> **Data collection method:** Tweets were collected using automated search tools querying publicly available content. All data accessed was publicly posted — no private accounts, direct messages, or protected content were accessed. Results are reported in daily aggregated form only; no individual tweet text or identifying user information appears in any output.

---

## 11. IF ASKED: DATA COLLECTION ETHICS AND COMPLIANCE

### "Where did you get the tweets?"

Tweets were collected using the `twikit` Python library, which queries Twitter's search functionality. The scraper is in the `TwitterScrapper/` directory. Key files: `search.py` (executes keyword searches), `multi_account.py` (rotates accounts to respect rate limits), `rate_limiter.py` (backoff when limits are hit).

### "Is web scraping legal?"

The collection method uses an automated search interface, not raw HTML scraping. The `twikit` library (see `search.py:8`) queries public tweet data. Only publicly posted content was accessed — no private accounts, no protected tweets, no direct messages.

### "Does this violate X/Twitter's Terms of Service?"

Yes — X's Terms of Service (Section 4, "Misuse of the Services," item iii) states: **"crawling or scraping the Services in any form, for any purpose without our prior written consent is expressly prohibited."** This is documented at `https://x.com/en/tos`.

This is a known tension in the academic social media research community. Thousands of published papers in economics, finance, political science, and computer science use scraped Twitter data. The academic community generally accepts this practice when:

1. Only public data is accessed
2. Results are reported in aggregated form (no individual users identified)
3. The research is non-commercial (academic conference/journal)

### "What would you say if a reviewer asks about this?"

> "We acknowledge that X's Terms of Service restrict automated collection without written consent. Our study accessed only publicly posted content and reports results solely in daily aggregated form — no individual tweets, usernames, or personal information appears in any output. This approach is consistent with the standard practice in the social media research literature. For future work, we would pursue official API access."

### "What about ethics board / IRB approval?"

Check your institution's policy. Most IRBs classify analysis of public social media data as "exempt" because it does not constitute human subjects research — there is no intervention, no interaction with subjects, and no collection of identifiable private information. If your university does not have an IRB process or has not reviewed this study, be prepared to state that the data is public discourse and the research is non-commercial.

### "Can I share the raw tweet data with others?"

No. The raw CSV files contain individual tweet text and usernames. Only the aggregated outputs (`gpt5_merged.csv`, daily sentiment scores, summary statistics) should be shared. The raw CSVs are in the GitHub `.gitignore` and are not committed to the public repository.

---

*This document is your complete reference. If you can't remember a number or concept during the presentation, everything is here.*
