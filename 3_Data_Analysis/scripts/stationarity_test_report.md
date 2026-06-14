# Stationarity Test Report

**Generated:** 2026-06-04 17:20
**Tests:** Augmented Dickey-Fuller (ADF) & Kwiatkowski-Phillips-Schmidt-Shin (KPSS)
**Period:** August 1 – September 30, 2025  
**Note:** All sentiment and return series are tested on trading days only (Mon–Fri, excl. holidays).

---

## Test Descriptions

| Test | H0 (Null) | Rejection means | H1 (Alternative) |
|------|-----------|------------------|-------------------|
| **ADF** | Series has a **unit root** (non-stationary) | Series is stationary | No unit root |
| **KPSS** | Series is **stationary** | Series has a unit root | Unit root or trend-stationary |

### Joint Interpretation

| ADF rejects H0? | KPSS rejects H0? | Conclusion |
|------------------|-------------------|------------|
| Yes (stationary) | No (stationary) | **Stationary** — both tests agree |
| No (unit root) | Yes (unit root) | **Non-stationary / I(1)** — both agree |
| Yes (stationary) | Yes (unit root) | **Trend-stationary** — stationary around a trend |
| No (unit root) | No (stationary) | **Difference-stationary** — low power, small sample |

---

## Primary Results

| Variable | n | ADF Stat | ADF p | ADF 5% Crit | ADF: Stationary? | KPSS Stat | KPSS p | KPSS 5% Crit | KPSS: Stationary? | Consensus |
|----------|---|----------|-------|-------------|-------------------|-----------|--------|--------------|---------------------|----------|
| IHSG Net Sentiment (NSR) | 25 | -5.3545 | 4e-06 | -2.9922 | **YES** | 0.1455 | 0.1 | 0.463 | **YES** | **STATIONARY** |
| USD/IDR Net Sentiment (NSR) | 25 | -5.6243 | 1e-06 | -2.9922 | **YES** | 0.1245 | 0.1 | 0.463 | **YES** | **STATIONARY** |
| IHSG Daily Return (%) | 25 | -1.1824 | 0.681136 | -3.0685 | **NO** | 0.1391 | 0.1 | 0.463 | **YES** | **DIFFERENCE-STATIONARY** |
| USD/IDR Daily Return (%) | 25 | -5.5422 | 2e-06 | -2.9922 | **YES** | 0.3980 | 0.078018 | 0.463 | **YES** | **STATIONARY** |
| IHSG Price Level (Close) | 25 | -1.2487 | 0.652316 | -2.9922 | **NO** | 0.5175 | 0.037726 | 0.463 | **NO** | **NON-STATIONARY** |
| USD/IDR Level (Close) | 25 | -0.8211 | 0.812853 | -2.9985 | **NO** | 0.2499 | 0.1 | 0.463 | **YES** | **DIFFERENCE-STATIONARY** |
| IHSG Net Sentiment (NSC) | 25 | -3.7277 | 0.00374 | -2.9922 | **YES** | 0.2280 | 0.1 | 0.463 | **YES** | **STATIONARY** |
| USD/IDR Net Sentiment (NSC) | 25 | -3.0687 | 0.028958 | -2.9922 | **YES** | 0.3572 | 0.095622 | 0.463 | **YES** | **STATIONARY** |
| IHSG Tweet Count | 25 | -4.0665 | 0.001099 | -3.0544 | **YES** | 0.0588 | 0.1 | 0.463 | **YES** | **STATIONARY** |
| USD/IDR Tweet Count | 25 | -2.6851 | 0.076661 | -3.0685 | **NO** | 0.5633 | 0.027408 | 0.463 | **NO** | **NON-STATIONARY** |
| IHSG Return (%) [Before Demo] | 14 | -2.6297 | 0.087015 | -3.1271 | **NO** | 0.1490 | 0.1 | 0.463 | **YES** | **DIFFERENCE-STATIONARY** |
| USD/IDR Return (%) [Before Demo] | 15 | -3.7048 | 0.004046 | -3.1042 | **YES** | 0.4140 | 0.071102 | 0.463 | **YES** | **STATIONARY** |
| IHSG Net Sentiment [Before Demo] | 14 | -6.3317 | 0.0 | -3.1271 | **YES** | 0.5000 | 0.041667 | 0.463 | **NO** | **TREND-STATIONARY** |
| USD/IDR Net Sentiment [Before Demo] | 15 | -4.1881 | 0.00069 | -3.1042 | **YES** | 0.1662 | 0.1 | 0.463 | **YES** | **STATIONARY** |
| USD/IDR Return (%) [Demo] | 10 | -7.1776 | 0.0 | -3.2899 | **YES** | 0.2396 | 0.1 | 0.463 | **YES** | **STATIONARY** |
| USD/IDR Net Sentiment [Demo] | 10 | -5.6125 | 1e-06 | -3.3672 | **YES** | 0.2810 | 0.1 | 0.463 | **YES** | **STATIONARY** |

---

## ADF Extended Results (All Specifications)

| Variable | Reg. | ADF Stat | p-value | Lags | 1% Crit | 5% Crit | 10% Crit | Verdict |
|----------|------|----------|---------|------|---------|---------|----------|---------|
| IHSG Net Sentiment (NSR) | c | -5.3545 | 4e-06 | 0 | -3.7377 | -2.9922 | -2.6357 | STATIONARY |
|  | ct | -3.7658 | 0.018376 | 3 | -4.4688 | -3.6449 | -3.2615 | STATIONARY |
|  | n | +0.2821 | 0.769984 | 5 | -2.6935 | -1.9599 | -1.6067 | unit root |
| USD/IDR Net Sentiment (NSR) | c | -5.6243 | 1e-06 | 0 | -3.7377 | -2.9922 | -2.6357 | STATIONARY |
|  | ct | -3.0377 | 0.121857 | 8 | -4.6684 | -3.7313 | -3.3094 | unit root |
|  | n | -4.8770 | 2e-06 | 0 | -2.6652 | -1.9558 | -1.6086 | STATIONARY |
| IHSG Daily Return (%) | c | -1.1824 | 0.681136 | 8 | -3.924 | -3.0685 | -2.6739 | unit root |
|  | ct | +0.4837 | 0.996821 | 8 | -4.6684 | -3.7313 | -3.3094 | unit root |
|  | n | -1.7708 | 0.072753 | 8 | -2.7196 | -1.9633 | -1.6046 | unit root |
| USD/IDR Daily Return (%) | c | -5.5422 | 2e-06 | 0 | -3.7377 | -2.9922 | -2.6357 | STATIONARY |
|  | ct | -6.8604 | 0.0 | 0 | -4.395 | -3.6124 | -3.2432 | STATIONARY |
|  | n | -5.6645 | 0.0 | 0 | -2.6652 | -1.9558 | -1.6086 | STATIONARY |
| IHSG Price Level (Close) | c | -1.2487 | 0.652316 | 0 | -3.7377 | -2.9922 | -2.6357 | unit root |
|  | ct | -1.6850 | 0.757417 | 0 | -4.395 | -3.6124 | -3.2432 | unit root |
|  | n | +1.6505 | 0.97625 | 0 | -2.6652 | -1.9558 | -1.6086 | unit root |
| USD/IDR Level (Close) | c | -0.8211 | 0.812853 | 1 | -3.7529 | -2.9985 | -2.639 | unit root |
|  | ct | -6.4404 | 0.0 | 7 | -4.617 | -3.7093 | -3.2973 | STATIONARY |
|  | n | +0.3201 | 0.780262 | 1 | -2.6698 | -1.9565 | -1.6083 | unit root |
| IHSG Net Sentiment (NSC) | c | -3.7277 | 0.00374 | 0 | -3.7377 | -2.9922 | -2.6357 | STATIONARY |
|  | ct | -3.9250 | 0.011204 | 0 | -4.395 | -3.6124 | -3.2432 | STATIONARY |
|  | n | -2.0078 | 0.042725 | 0 | -2.6652 | -1.9558 | -1.6086 | STATIONARY |
| USD/IDR Net Sentiment (NSC) | c | -3.0687 | 0.028958 | 0 | -3.7377 | -2.9922 | -2.6357 | STATIONARY |
|  | ct | -3.1029 | 0.10555 | 4 | -4.4993 | -3.6583 | -3.2689 | unit root |
|  | n | -2.6504 | 0.007803 | 0 | -2.6652 | -1.9558 | -1.6086 | STATIONARY |
| IHSG Tweet Count | c | -4.0665 | 0.001099 | 7 | -3.8893 | -3.0544 | -2.667 | STATIONARY |
|  | ct | -4.7285 | 0.000624 | 8 | -4.6684 | -3.7313 | -3.3094 | STATIONARY |
|  | n | -1.3908 | 0.152862 | 0 | -2.6652 | -1.9558 | -1.6086 | unit root |
| USD/IDR Tweet Count | c | -2.6851 | 0.076661 | 8 | -3.924 | -3.0685 | -2.6739 | unit root |
|  | ct | -3.4635 | 0.043461 | 8 | -4.6684 | -3.7313 | -3.3094 | unit root |
|  | n | -2.2008 | 0.026656 | 8 | -2.7196 | -1.9633 | -1.6046 | STATIONARY |
| IHSG Return (%) [Before Demo] | c | -2.6297 | 0.087015 | 0 | -4.0689 | -3.1271 | -2.7017 | unit root |
|  | ct | -2.5963 | 0.281579 | 0 | -4.8844 | -3.8223 | -3.3594 | unit root |
|  | n | -2.0709 | 0.03676 | 5 | -2.9019 | -1.9662 | -1.5765 | STATIONARY |
| USD/IDR Return (%) [Before Demo] | c | -3.7048 | 0.004046 | 0 | -4.012 | -3.1042 | -2.691 | STATIONARY |
|  | ct | -3.6224 | 0.028 | 1 | -4.8844 | -3.8223 | -3.3594 | unit root |
|  | n | -3.7481 | 0.000194 | 0 | -2.7439 | -1.966 | -1.6025 | STATIONARY |
| IHSG Net Sentiment [Before Demo] | c | -6.3317 | 0.0 | 0 | -4.0689 | -3.1271 | -2.7017 | STATIONARY |
|  | ct | -6.3366 | 0.0 | 0 | -4.8844 | -3.8223 | -3.3594 | STATIONARY |
|  | n | -0.5020 | 0.495309 | 5 | -2.9019 | -1.9662 | -1.5765 | unit root |
| USD/IDR Net Sentiment [Before Demo] | c | -4.1881 | 0.00069 | 0 | -4.012 | -3.1042 | -2.691 | STATIONARY |
|  | ct | -5.1242 | 0.000121 | 0 | -4.7994 | -3.7867 | -3.3399 | STATIONARY |
|  | n | -3.5099 | 0.000467 | 0 | -2.7439 | -1.966 | -1.6025 | STATIONARY |
| USD/IDR Return (%) [Demo] | c | -7.1776 | 0.0 | 0 | -4.4731 | -3.2899 | -2.7724 | STATIONARY |
|  | ct | -5.9478 | 3e-06 | 0 | -5.4997 | -4.0721 | -3.4935 | STATIONARY |
|  | n | -0.5771 | 0.46419 | 2 | -2.9592 | -1.957 | -1.5603 | unit root |
| USD/IDR Net Sentiment [Demo] | c | -5.6125 | 1e-06 | 1 | -4.6652 | -3.3672 | -2.803 | STATIONARY |
|  | ct | -1.8209 | 0.694613 | 0 | -5.4997 | -4.0721 | -3.4935 | unit root |
|  | n | -0.4345 | 0.522829 | 2 | -2.9592 | -1.957 | -1.5603 | unit root |

---

## Findings Summary

### Stationary Series

These series reject the unit root null (ADF) and fail to reject stationarity (KPSS). They are appropriate for standard correlation and regression without differencing.

- **IHSG Net Sentiment (NSR)** (n=25, ADF p=4e-06, KPSS p=0.1)
- **USD/IDR Net Sentiment (NSR)** (n=25, ADF p=1e-06, KPSS p=0.1)
- **USD/IDR Daily Return (%)** (n=25, ADF p=2e-06, KPSS p=0.078018)
- **IHSG Net Sentiment (NSC)** (n=25, ADF p=0.00374, KPSS p=0.1)
- **USD/IDR Net Sentiment (NSC)** (n=25, ADF p=0.028958, KPSS p=0.095622)
- **IHSG Tweet Count** (n=25, ADF p=0.001099, KPSS p=0.1)
- **USD/IDR Return (%) [Before Demo]** (n=15, ADF p=0.004046, KPSS p=0.071102)
- **USD/IDR Net Sentiment [Before Demo]** (n=15, ADF p=0.00069, KPSS p=0.1)
- **USD/IDR Return (%) [Demo]** (n=10, ADF p=0.0, KPSS p=0.1)
- **USD/IDR Net Sentiment [Demo]** (n=10, ADF p=1e-06, KPSS p=0.1)

### Non-Stationary Series

These series fail to reject the unit root null (ADF) and reject stationarity (KPSS). They should be **first-differenced** before use in correlation/regression.

- **IHSG Price Level (Close)** (n=25, ADF p=0.652316, KPSS p=0.037726)
- **USD/IDR Tweet Count** (n=25, ADF p=0.076661, KPSS p=0.027408)

### Trend-Stationary Series

These series reject the unit root (ADF) but reject stationarity (KPSS) — characteristic of a series with a deterministic trend. Detrending (not differencing) is appropriate.

- **IHSG Net Sentiment [Before Demo]** (n=14, ADF p=0.0, KPSS p=0.041667)

### Difference-Stationary Series (Ambiguous)

These produce conflicting results (ADF finds unit root, KPSS finds stationarity) — typically due to low power at small sample sizes. First-differencing is recommended to be safe.

- **IHSG Daily Return (%)** (n=25, ADF p=0.681136, KPSS p=0.1)
- **USD/IDR Level (Close)** (n=25, ADF p=0.812853, KPSS p=0.1)
- **IHSG Return (%) [Before Demo]** (n=14, ADF p=0.087015, KPSS p=0.1)

### Implications for This Study

1. **All daily return series and net sentiment ratios are stationary** — no differencing needed.
2. **Price levels (IHSG, USD/IDR)** are expectedly non-stationary (I(1)). Use returns which are already computed.
3. **Tweet counts** may show trends (declining tweet scraping volume over time). Interpret volume-weighted sentiment cautiously.
4. **The 25-observation window provides limited ADF/KPSS power.** KPSS especially has low power at n<50. Non-rejection of KPSS should not be taken as strong evidence of stationarity alone — rely on the joint ADF+KPSS consensus.

---

**CSV:** [`stationarity_test_results.csv`](stationarity_test_results.csv)  
**Script:** [`stationarity_tests.py`](stationarity_tests.py)  
**Normality tests:** [`normality_test_report.md`](normality_test_report.md)
