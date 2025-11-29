"""
Econometric Analysis: Granger Causality, VAR, and GARCH Models
Tests the relationship between Twitter sentiment and market returns
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from statsmodels.tsa.stattools import grangercausalitytests
from statsmodels.tsa.api import VAR
from statsmodels.stats.diagnostic import acorr_ljungbox
from arch import arch_model
import warnings
warnings.filterwarnings('ignore')

# Set professional styling
sns.set_style('whitegrid')
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['font.size'] = 12
plt.rcParams['axes.labelsize'] = 14
plt.rcParams['axes.titlesize'] = 16
plt.rcParams['figure.titlesize'] = 18

def load_and_prepare_data():
    """Load and prepare sentiment and market data"""
    print("Loading and preparing data...")
    
    # Load data (same as in data_analysis.ipynb)
    df_sent = pd.read_csv('data/daily_sentiment_gpt5.csv', parse_dates=['date'])
    df_ihsg = pd.read_csv('data/ihsg_daily.csv', parse_dates=['Date'])
    df_ihsg.rename(columns={'Date': 'date'}, inplace=True)
    df_usd = pd.read_csv('data/usd_idr_daily.csv', parse_dates=['Date'])
    df_usd.rename(columns={'Date': 'date'}, inplace=True)
    
    # Preprocess
    df_sent['date'] = pd.to_datetime(df_sent['date']).dt.strftime('%Y-%m-%d')
    df_ihsg['date'] = pd.to_datetime(df_ihsg['date']).dt.strftime('%Y-%m-%d')
    df_usd['date'] = pd.to_datetime(df_usd['date'], utc=True).dt.strftime('%Y-%m-%d')
    
    # Filter to August-September 2025
    start = '2025-08-01'
    end = '2025-09-29'
    df_sent = df_sent[(df_sent['date'] >= start) & (df_sent['date'] <= end)]
    df_ihsg = df_ihsg[(df_ihsg['date'] >= start) & (df_ihsg['date'] <= end)]
    df_usd = df_usd[(df_usd['date'] >= start) & (df_usd['date'] <= end)]
    
    # Compute returns
    df_ihsg['ihsg_return'] = df_ihsg['Close'].pct_change() * 100
    df_usd['usd_return'] = df_usd['Close'].pct_change() * 100
    
    # Merge datasets
    df_merged = pd.merge(df_sent, df_ihsg[['date', 'ihsg_return']], on='date', how='inner')
    df_full = pd.merge(df_merged, df_usd[['date', 'usd_return']], on='date', how='inner')
    df_full['date'] = pd.to_datetime(df_full['date'])
    
    print(f"Data prepared: {df_full.shape[0]} observations")
    return df_full

def granger_causality_analysis(df, max_lag=3):
    """Perform Granger causality tests"""
    print("\n" + "="*60)
    print("GRANGER CAUSALITY ANALYSIS")
    print("="*60)
    
    results = []
    
    # Test sentiment -> IHSG returns
    print("\nTesting: Sentiment -> IHSG Returns")
    print("-" * 40)
    
    # Prepare data (remove NaN values)
    data_ihsg = df[['ihsg_return', 'net_sent']].dropna()
    
    if len(data_ihsg) > max_lag + 10:  # Ensure sufficient data
        gc_ihsg = grangercausalitytests(data_ihsg, maxlag=max_lag, verbose=False)
        
        for lag in range(1, max_lag + 1):
            f_stat = gc_ihsg[lag][0]['ssr_ftest'][0]
            p_value = gc_ihsg[lag][0]['ssr_ftest'][1]
            results.append({
                'Test': 'Sentiment -> IHSG',
                'Lag': lag,
                'F-Statistic': f_stat,
                'P-Value': p_value,
                'Significant': p_value < 0.05
            })
            print(f"Lag {lag}: F={f_stat:.3f}, p={p_value:.4f} {'***' if p_value < 0.01 else '**' if p_value < 0.05 else '*' if p_value < 0.1 else ''}")
    
    # Test sentiment → USD/IDR returns
    print("\nTesting: Sentiment -> USD/IDR Returns")
    print("-" * 40)
    
    data_usd = df[['usd_return', 'net_sent']].dropna()
    
    if len(data_usd) > max_lag + 10:
        gc_usd = grangercausalitytests(data_usd, maxlag=max_lag, verbose=False)
        
        for lag in range(1, max_lag + 1):
            f_stat = gc_usd[lag][0]['ssr_ftest'][0]
            p_value = gc_usd[lag][0]['ssr_ftest'][1]
            results.append({
                'Test': 'Sentiment -> USD/IDR',
                'Lag': lag,
                'F-Statistic': f_stat,
                'P-Value': p_value,
                'Significant': p_value < 0.05
            })
            print(f"Lag {lag}: F={f_stat:.3f}, p={p_value:.4f} {'***' if p_value < 0.01 else '**' if p_value < 0.05 else '*' if p_value < 0.1 else ''}")
    
    return pd.DataFrame(results)

def var_analysis(df, max_lags=3):
    """Perform Vector Autoregression analysis"""
    print("\n" + "="*60)
    print("VECTOR AUTOREGRESSION (VAR) ANALYSIS")
    print("="*60)
    
    # Prepare data
    var_data = df[['net_sent', 'ihsg_return', 'usd_return']].dropna()
    
    # Fit VAR model
    model = VAR(var_data)
    results = model.fit(maxlags=max_lags, ic='aic')
    
    print(f"\nOptimal lag order: {results.k_ar}")
    
    # Check if we have valid lags
    if results.k_ar == 0:
        print("Warning: Optimal lag order is 0. Using 1 lag for analysis.")
        results = model.fit(maxlags=1)
        print(f"Forced lag order: {results.k_ar}")
    
    print(f"\nModel summary:")
    print(results.summary())
    
    # Impulse Response Functions
    print("\nGenerating Impulse Response Functions...")
    try:
        irf = results.irf(10)
        
        # Plot IRF
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        fig.suptitle('Impulse Response Functions', fontsize=16)
        
        # Response of markets to sentiment shock
        irf.plot(orth=False, impulse='net_sent', response='ihsg_return',
                 subplot_params={'title': 'IHSG Response to Sentiment Shock'}, ax=axes[0,0])
        irf.plot(orth=False, impulse='net_sent', response='usd_return',
                 subplot_params={'title': 'USD/IDR Response to Sentiment Shock'}, ax=axes[0,1])
        
        # Response of sentiment to market shocks
        irf.plot(orth=False, impulse='ihsg_return', response='net_sent',
                 subplot_params={'title': 'Sentiment Response to IHSG Shock'}, ax=axes[1,0])
        irf.plot(orth=False, impulse='usd_return', response='net_sent',
                 subplot_params={'title': 'Sentiment Response to USD/IDR Shock'}, ax=axes[1,1])
        
        plt.tight_layout()
        plt.savefig('plots/var_impulse_response.png', dpi=300, bbox_inches='tight')
        plt.show()
    except Exception as e:
        print(f"Warning: Could not generate IRF: {e}")
        irf = None
    
    # Variance Decomposition
    print("\nVariance Decomposition (10 periods ahead):")
    try:
        fevd = results.fevd(10)
        print(fevd.summary())
    except Exception as e:
        print(f"Warning: Could not generate FEVD: {e}")
        fevd = None
    
    return results, irf, fevd

def garch_analysis(df):
    """Perform GARCH volatility modeling"""
    print("\n" + "="*60)
    print("GARCH VOLATILITY MODELING")
    print("="*60)
    
    # Prepare returns data (convert to decimal) and align with dates
    returns_raw = df['ihsg_return'].copy()
    valid_mask = ~returns_raw.isna()
    returns = returns_raw[valid_mask] * 0.01
    valid_dates = df['date'][valid_mask].reset_index(drop=True)
    
    # Standard GARCH(1,1) model
    print("\nFitting GARCH(1,1) model...")
    garch = arch_model(returns, vol='Garch', p=1, q=1)
    garch_results = garch.fit(disp='off')
    
    print("\nGARCH(1,1) Results:")
    print(garch_results.summary())
    
    # Plot conditional volatility
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10))
    
    # Returns
    ax1.plot(valid_dates, returns, color='blue', alpha=0.7)
    ax1.set_title('IHSG Returns', fontsize=14)
    ax1.set_ylabel('Daily Return')
    ax1.grid(True, alpha=0.3)
    
    # Conditional volatility
    volatility = garch_results.conditional_volatility
    ax2.plot(valid_dates[:len(volatility)], volatility, color='red')
    ax2.set_title('Conditional Volatility (GARCH)', fontsize=14)
    ax2.set_ylabel('Volatility')
    ax2.set_xlabel('Date')
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('plots/garch_volatility.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    # Test if sentiment affects volatility
    print("\nTesting if sentiment affects volatility...")
    sentiment_data = df['net_sent'].dropna().values
    
    # Ensure same length
    min_len = min(len(returns), len(sentiment_data))
    returns_trimmed = returns[:min_len]
    sentiment_trimmed = sentiment_data[:min_len]
    
    # GARCH with sentiment as exogenous variable
    garch_sentiment = arch_model(returns_trimmed, vol='Garch', p=1, q=1, 
                                 x=sentiment_trimmed.reshape(-1, 1))
    sentiment_results = garch_sentiment.fit(disp='off')
    
    print("\nGARCH with Sentiment Results:")
    print(sentiment_results.summary())
    
    return garch_results, sentiment_results

def main():
    """Main analysis function"""
    print("Starting Econometric Analysis...")
    print("="*60)
    
    # Load data
    df = load_and_prepare_data()
    
    # Create output directory
    import os
    os.makedirs('plots', exist_ok=True)
    
    # 1. Granger Causality
    gc_results = granger_causality_analysis(df)
    gc_results.to_csv('granger_causality_results.csv', index=False)
    
    # 2. VAR Analysis
    var_results, irf, fevd = var_analysis(df)
    
    # 3. GARCH Analysis
    garch_results, garch_sentiment_results = garch_analysis(df)
    
    print("\n" + "="*60)
    print("ANALYSIS COMPLETE")
    print("="*60)
    print("\nFiles saved:")
    print("- granger_causality_results.csv")
    print("- plots/var_impulse_response.png")
    print("- plots/garch_volatility.png")

if __name__ == "__main__":
    main()