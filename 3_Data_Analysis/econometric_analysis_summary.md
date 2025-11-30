# Econometric Analysis Summary: Twitter Sentiment and Market Returns

**Analysis Period**: August-September 2025 (Indonesian Protests Context)  
**Data Points**: 31 daily observations  
**Methods**: Granger Causality, Vector Autoregression (VAR), GARCH Volatility Modeling

---

## Executive Summary

This analysis employs three advanced econometric methods to test whether Twitter sentiment predicts market movements during the Indonesian protests period. The results provide **limited evidence** of predictive power, with only marginal significance at the 2-day lag for IHSG returns.

### Key Findings:
- **Granger Causality**: Sentiment shows marginal predictive power for IHSG at 2-day lag (p=0.092)
- **VAR Model**: Sentiment explains only 5-6% of market return variance
- **GARCH**: No evidence that sentiment affects market volatility
- **Sample Limitation**: Small sample size (31 obs) limits statistical power

---

## 1. Granger Causality Analysis

### Methodology
Tests whether past values of sentiment help predict future market returns better than using only past market returns.

### Results

| Test | Lag | F-Statistic | P-Value | Significance |
|------|-----|-------------|---------|--------------|
| Sentiment → IHSG | 1 day | 0.364 | 0.551 | - |
| Sentiment → IHSG | 2 days | 2.638 | 0.092 | * |
| Sentiment → IHSG | 3 days | 1.821 | 0.174 | - |
| Sentiment → USD/IDR | 1 day | 0.105 | 0.748 | - |
| Sentiment → USD/IDR | 2 days | 1.936 | 0.166 | - |
| Sentiment → USD/IDR | 3 days | 1.844 | 0.170 | - |

**Interpretation**:
- **IHSG**: Marginally significant at 2-day lag (p < 0.10), suggesting weak predictive power
- **USD/IDR**: No significant Granger causality at any lag
- **Overall**: Limited evidence that sentiment predicts market movements

---

## 2. Vector Autoregression (VAR) Analysis

### Methodology
Models the joint dynamic relationships between sentiment, IHSG returns, and USD/IDR returns.

### Model Summary
- **Optimal Lag Order**: 0 (forced to 1 for analysis)
- **Observations**: 30 (after lag creation)
- **Log-Likelihood**: -25.49

### Coefficient Estimates

**Equation: Sentiment (net_sent)**
| Variable | Coefficient | Std. Error | t-stat | p-value |
|----------|-------------|------------|--------|---------|
| Constant | -0.065 | 0.040 | -1.64 | 0.100 |
| L1.net_sent | **0.497** | 0.168 | **2.96** | **0.003** |
| L1.ihsg_return | -0.046 | 0.030 | -1.56 | 0.118 |
| L1.usd_return | -0.106 | 0.072 | -1.47 | 0.142 |

**Equation: IHSG Returns**
| Variable | Coefficient | Std. Error | t-stat | p-value |
|----------|-------------|------------|--------|---------|
| Constant | 0.432 | 0.261 | 1.66 | 0.097 |
| L1.net_sent | 0.593 | 1.098 | 0.54 | 0.589 |
| L1.ihsg_return | -0.044 | 0.194 | -0.23 | 0.820 |
| L1.usd_return | -0.329 | 0.472 | -0.70 | 0.485 |

**Key Insights**:
- **Sentiment is persistent**: Lagged sentiment significantly predicts current sentiment (p=0.003)
- **Weak market prediction**: Sentiment coefficient in IHSG equation is not significant (p=0.589)
- **Low explanatory power**: Market returns are not well-explained by lagged variables

### Variance Decomposition (10 periods ahead)

**IHSG Returns Variance Explained By:**
- Own shocks: ~92.4%
- Sentiment shocks: ~6.0%
- USD/IDR shocks: ~1.6%

**Interpretation**: Sentiment explains only a small portion (6%) of IHSG return volatility, with most variation driven by market-specific factors.

---

## 3. GARCH Volatility Modeling

### Methodology
Tests whether sentiment affects the volatility (risk) of market returns, not just the returns themselves.

### GARCH(1,1) Results

**Volatility Equation Parameters**:
| Parameter | Estimate | Std. Error | t-stat | p-value |
|-----------|----------|------------|--------|---------|
| omega (constant) | 1.59e-09 | 6.25e-11 | 25.36 | <0.001 |
| alpha[1] (ARCH) | 1.09e-10 | 9.76e-02 | 1.12e-09 | 1.000 |
| beta[1] (GARCH) | **0.9908** | 0.103 | **9.62** | **<0.001** |

**Key Findings**:
- **High volatility persistence**: Beta = 0.99 indicates shocks persist for long periods
- **Sentiment effect**: When sentiment is added as exogenous variable, it does not significantly improve the model
- **No volatility impact**: Sentiment does not appear to affect market volatility levels

---

## 4. Cross-Method Validation

### Consistency Across Methods

| Method | Sentiment → IHSG | Sentiment → USD/IDR | Key Finding |
|--------|------------------|---------------------|-------------|
| Granger Causality | Marginal (lag 2) | None | Weak predictive power |
| VAR Coefficients | Not significant | Not significant | No significant effect |
| Variance Decomp | 6% of variance | 2% of variance | Small contribution |
| GARCH Volatility | No effect | Not tested | No risk impact |

**Conclusion**: All three methods converge on the same conclusion—sentiment has **limited predictive power** for market movements during this period.

---

## 5. Limitations & Caveats

### Statistical Limitations
1. **Small Sample Size**: Only 31 observations limits statistical power
2. **Short Time Series**: May not capture long-term relationships
3. **Structural Breaks**: Protest period may have non-standard relationships
4. **Omitted Variables**: Other factors (news, policy, global markets) not controlled

### Methodological Considerations
1. **Granger Causality**: Tests predictive power, not true causality
2. **VAR Model**: Optimal lag of 0 suggests weak dynamic relationships
3. **GARCH**: High persistence but no sentiment effect on volatility

### Data Quality
1. **Sentiment Aggregation**: Daily aggregation may lose intraday patterns
2. **Market Data**: Limited to closing prices, missing intraday volatility
3. **Protest Period**: Unusual market conditions may not generalize

---

## 6. Practical Implications

### For Trading Strategies
- **Weak Signal**: Sentiment provides limited predictive information
- **Timing**: 2-day lag may be too slow for practical trading
- **Risk Management**: Sentiment does not help forecast volatility

### For Policy Makers
- **Market Monitoring**: Sentiment may provide early warning (weak signal)
- **Intervention Timing**: Effects appear with 2-day delay
- **Limited Impact**: Sentiment explains only small portion of market moves

### For Researchers
- **Sample Size**: Larger samples needed for robust conclusions
- **Methodology**: Consider regime-switching models for protest periods
- **Extensions**: Include more control variables (news, volume, global factors)

---

## 7. Recommendations

### Immediate Actions
1. **Collect More Data**: Extend analysis to longer time periods
2. **Intraday Analysis**: Use higher frequency data if available
3. **Control Variables**: Add news sentiment, trading volume, global indices

### Future Research
1. **Regime-Switching Models**: Account for protest vs normal periods
2. **Non-linear Models**: Test for threshold effects in sentiment
3. **Machine Learning**: Explore non-linear relationships with larger datasets

### Conclusion
While the analysis provides **limited evidence** of sentiment predicting market movements, the marginal significance at 2-day lag for IHSG suggests there may be a weak relationship worth exploring with larger datasets and more sophisticated models.

---

## Files Generated

- `econometric_analysis.py` - Python script with all methods
- `econometric_analysis.ipynb` - Interactive Jupyter notebook
- `granger_causality_results.csv` - Granger test results
- `var_model_summary.txt` - VAR model details
- `garch_results_summary.txt` - GARCH model results
- `plots/garch_volatility.png` - GARCH volatility plot

**GitHub Repository**: All files saved to `3_Data_Analysis/` folder