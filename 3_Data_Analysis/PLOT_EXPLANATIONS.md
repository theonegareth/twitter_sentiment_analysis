# Plot Interpretation Guide: Twitter Sentiment & Market Analysis

**Analysis Period**: August-September 2025 (Indonesian Protests)  
**Total Visualizations**: 17 professional plots  
**Location**: `3_Data_Analysis/plots/`

---

## **CATEGORY 1: Time Series Analysis (5 plots)**

### 1. `sentiment_vs_ihsg.png`
**What it shows**: Dual-axis time series of Twitter sentiment (blue) and IHSG daily returns (red) with raw IHSG closing prices (gray dashed line).

**How to read**:
- **Left axis**: Net sentiment score (range: -0.4 to +0.2)
- **Right axis (red)**: IHSG daily return percentage
- **Right axis (gray)**: Raw IHSG index level
- **Gray background**: Protest period shading

**What to look for**:
- Do sentiment spikes align with market movements?
- Are there visible lead-lag relationships?
- **Interpretation**: Visual inspection shows weak co-movement; correlation is moderate (0.222) but not strongly predictive.

---

### 2. `sentiment_vs_usd.png`
**What it shows**: Dual-axis time series of Twitter sentiment (blue) and USD/IDR daily returns (green) with raw exchange rates (gray dashed line).

**How to read**:
- **Left axis**: Net sentiment score
- **Right axis (green)**: USD/IDR daily return percentage
- **Right axis (gray)**: Raw exchange rate

**What to look for**:
- Does sentiment predict currency movements?
- Are there delayed reactions?
- **Interpretation**: Even weaker relationship than IHSG; correlation is minimal (-0.150).

---

### 3. `rolling_sentiment_vs_ihsg.png`
**What it shows**: 7-day rolling averages of sentiment and IHSG returns to smooth out daily noise.

**How to read**:
- **Blue line**: 7-day average net sentiment
- **Red line**: 7-day average IHSG returns
- **X-axis**: Date (August-September 2025)

**What to look for**:
- Do smoothed trends show clearer relationships?
- Are there sustained periods of alignment?
- **Interpretation**: Rolling averages reveal some co-movement but no strong predictive pattern.

---

### 4. `combined_analysis.png`
**What it shows**: Four-panel comprehensive overview (sentiment vs IHSG, sentiment vs USD/IDR, rolling averages, correlation heatmap).

**How to read**:
- **Top left**: Sentiment vs IHSG time series
- **Top right**: Sentiment vs USD/IDR time series
- **Bottom left**: Rolling averages
- **Bottom right**: Correlation matrix

**What to look for**:
- Consistency across different views
- Overall pattern strength
- **Interpretation**: Multi-panel view confirms weak but consistent relationships across methods.

---

### 5. `garch_volatility.png`
**What it shows**: IHSG returns (top) and conditional volatility from GARCH model (bottom).

**How to read**:
- **Top panel**: Daily IHSG returns over time
- **Bottom panel**: Estimated volatility (risk) from GARCH(1,1) model
- **Red line**: Volatility spikes indicate high-risk periods

**What to look for**:
- Does sentiment predict volatility spikes?
- Are high-volatility periods associated with extreme sentiment?
- **Interpretation**: Volatility is persistent (high beta) but not driven by sentiment.

---

## **CATEGORY 2: Distribution Analysis (3 plots)**

### 6. `sentiment_distribution.png`
**What it shows**: Histogram and box plot of net sentiment scores.

**How to read**:
- **Left**: Frequency distribution of sentiment values
- **Right**: Box plot showing median, quartiles, and outliers
- **Red dashed line**: Mean sentiment (-0.165)

**What to look for**:
- Is sentiment normally distributed?
- Are there extreme outliers?
- **Interpretation**: Sentiment is slightly negative (mean -0.165) with moderate variation (std 0.155).

---

### 7. `returns_distribution.png`
**What it shows**: Histograms of IHSG and USD/IDR daily returns.

**How to read**:
- **Left**: Distribution of IHSG returns (red)
- **Right**: Distribution of USD/IDR returns (green)
- **Red dashed lines**: Mean returns (near zero)

**What to look for**:
- Are returns normally distributed?
- Are there fat tails (extreme days)?
- **Interpretation**: Both markets show near-zero mean returns with typical volatility patterns.

---

### 8. `scatter_regression.png`
**What it shows**: Scatter plots with regression lines showing linear relationships.

**How to read**:
- **Left**: Sentiment (x-axis) vs IHSG returns (y-axis)
- **Right**: Sentiment (x-axis) vs USD/IDR returns (y-axis)
- **Dashed lines**: Best-fit regression lines
- **R² values**: Proportion of variance explained

**What to look for**:
- How tightly do points cluster around the line?
- Is the slope statistically significant?
- **Interpretation**: Very low R² values (near zero) indicate weak linear relationships.

---

## **CATEGORY 3: Statistical Testing (3 plots)**

### 9. `granger_causality_visualization.png`
**What it shows**: Granger causality test results across different lags.

**How to read**:
- **Left panel**: F-statistics for each lag (1, 2, 3 days)
- **Right panel**: P-values with significance thresholds (5% and 10%)
- **Lines**: Different colors for IHSG vs USD/IDR tests

**What to look for**:
- Do F-statistics exceed significance thresholds?
- Which lags show statistical significance?
- **Interpretation**: Only IHSG at lag 2 shows marginal significance (p=0.092), below 10% threshold but above 5%.

---

### 10. `lag_structure.png`
**What it shows**: Correlations between sentiment and market returns at different time lags.

**How to read**:
- **Left**: Line plot of correlations by lag (0-5 days)
- **Right**: Heatmap showing correlation strength
- **Gray dashed lines**: Approximate significance thresholds

**What to look for**:
- Do correlations peak at specific lags?
- Are lagged correlations stronger than contemporaneous?
- **Interpretation**: Correlations are weak across all lags, with no clear pattern.

---

### 11. `rolling_correlations.png`
**What it shows**: 10-day rolling correlations between sentiment and markets over time.

**How to read**:
- **Red line**: Rolling sentiment-IHSG correlation
- **Green line**: Rolling sentiment-USD/IDR correlation
- **X-axis**: Date

**What to look for**:
- Are correlations stable or time-varying?
- Do correlations strengthen during specific periods?
- **Interpretation**: Correlations are unstable and vary significantly over time, suggesting weak underlying relationship.

---

## **CATEGORY 4: Event & Regime Analysis (4 plots)**

### 12. `extreme_sentiment_days.png`
**What it shows**: Identification and market impact of extreme sentiment days (top/bottom 20%).

**How to read**:
- **Top panel**: Time series with extreme high (green triangles) and low (red triangles) sentiment marked
- **Bottom panel**: IHSG returns on extreme sentiment days

**What to look for**:
- Do extreme sentiment days cluster?
- Do markets react consistently to extreme sentiment?
- **Interpretation**: Extreme sentiment days don't show consistent market reactions.

---

### 13. `event_study.png`
**What it shows**: Market returns in 3-day windows around extreme sentiment events.

**How to read**:
- **Four panels**: Different extreme sentiment events
- **X-axis**: Days from event (-3 to +3)
- **Y-axis**: IHSG return percentage
- **Gray vertical line**: Event day (day 0)

**What to look for**:
- Do markets move before, during, or after events?
- Are reactions consistent across events?
- **Interpretation**: No consistent pattern of market reaction around extreme sentiment events.

---

### 14. `volatility_regimes.png`
**What it shows**: Sentiment-market relationships in high vs low volatility periods.

**How to read**:
- **Left**: High volatility regime (red)
- **Middle**: Low volatility regime (blue)
- **Right**: Correlation comparison by regime

**What to look for**:
- Are correlations stronger in certain volatility regimes?
- Do regimes show different patterns?
- **Interpretation**: Correlations are weak in both regimes, with slight differences but no strong regime effect.

---

### 15. `cumulative_returns.png`
**What it shows**: Cumulative market performance with extreme sentiment events marked.

**How to read**:
- **Top**: Cumulative IHSG returns with high (green triangles) and low (red triangles) sentiment days
- **Bottom**: Cumulative USD/IDR returns with sentiment events
- **X-axis**: Date

**What to look for**:
- Do extreme sentiment days coincide with trend changes?
- Are cumulative returns affected by sentiment events?
- **Interpretation**: Extreme sentiment days don't consistently predict trend changes or major market moves.

---

## **CATEGORY 5: Model Diagnostics (2 plots)**

### 16. `qq_diagnostics.png`
**What it shows**: Distribution and autocorrelation diagnostics.

**How to read**:
- **Top left**: QQ plot for sentiment (normality check)
- **Top right**: QQ plot for IHSG returns (normality check)
- **Bottom left**: Sentiment autocorrelation by lag
- **Bottom right**: Sentiment partial autocorrelation by lag

**What to look for**:
- Do points follow the straight line in QQ plots?
- Are autocorrelations significant (outside red dashed lines)?
- **Interpretation**: Sentiment shows significant autocorrelation at lag 1, indicating persistence.

---

### 17. `enhanced_correlation_matrix.png`
**What it shows**: Correlations including lagged variables.

**How to read**:
- **Matrix**: Correlations between sentiment, lagged sentiment, market returns, and lagged returns
- **Colors**: Red (positive), blue (negative), intensity = strength
- **Mask**: Upper triangle hidden for clarity

**What to look for**:
- Are lagged variables more correlated than contemporaneous?
- Which variable pairs show strongest relationships?
- **Interpretation**: Sentiment is highly autocorrelated (0.497 at lag 1) but shows weak cross-correlations with markets.

---

## **How to Use These Plots**

### **For Academic Papers:**
- Use **time series plots** (1-5) in results section
- Include **distribution plots** (6-8) for data description
- Present **statistical tests** (9-11) for hypothesis testing
- Add **event/regime plots** (12-15) for robustness checks
- Show **diagnostics** (16-17) in methodology appendix

### **For Presentations:**
- Start with **combined_analysis.png** for overview
- Focus on **granger_causality_visualization.png** for key findings
- Use **event_study.png** to illustrate specific examples
- End with **enhanced_correlation_matrix.png** for summary

### **For Reports:**
- Include all plots with captions explaining key insights
- Reference specific visualizations when discussing findings
- Use consistent interpretation framework across sections

---

## **Key Takeaways from All Plots**

1. **Weak Relationships**: All visualizations consistently show weak sentiment-market connections
2. **Marginal Significance**: Only lag-2 Granger test for IHSG approaches significance
3. **No Consistent Patterns**: Event studies and regime analysis find no reliable predictive patterns
4. **High Volatility Persistence**: GARCH shows markets have high volatility clustering
5. **Sentiment Persistence**: Sentiment is autocorrelated but doesn't predict markets well

**Bottom Line**: The visualizations provide comprehensive evidence that Twitter sentiment had limited predictive power for market movements during the Indonesian protests period.