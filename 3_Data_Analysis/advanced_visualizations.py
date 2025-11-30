"""
Advanced Visualizations for Deeper Sentiment-Market Insights
Specialized plots for event studies, regime analysis, and model diagnostics
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import os
from arch import arch_model
from statsmodels.tsa.stattools import pacf, acf

# Set professional styling
sns.set_style('whitegrid')
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['font.size'] = 12
plt.rcParams['axes.labelsize'] = 14
plt.rcParams['axes.titlesize'] = 16
plt.rcParams['figure.titlesize'] = 18

# Create plots directory
os.makedirs('plots', exist_ok=True)

def load_data():
    """Load the prepared data"""
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
    
    # Merge
    df_merged = pd.merge(df_sent, df_ihsg[['date', 'ihsg_return']], on='date', how='inner')
    df_full = pd.merge(df_merged, df_usd[['date', 'usd_return']], on='date', how='inner')
    df_full['date'] = pd.to_datetime(df_full['date'])
    
    return df_full

def plot_event_study(df):
    """Event study: Market reaction around extreme sentiment days"""
    # Define extreme days (top/bottom 15%)
    sent_85th = df['net_sent'].quantile(0.85)
    sent_15th = df['net_sent'].quantile(0.15)
    
    extreme_days = df[(df['net_sent'] >= sent_85th) | (df['net_sent'] <= sent_15th)]
    
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    
    # Event window: 3 days before to 3 days after
    window = 3
    
    for idx, (date_idx, event) in enumerate(extreme_days.iterrows()):
        if idx >= 4:  # Show only first 4 events to avoid clutter
            break
            
        # Find event position
        event_pos = df.index.get_loc(date_idx)
        start_pos = max(0, event_pos - window)
        end_pos = min(len(df), event_pos + window + 1)
        
        event_window = df.iloc[start_pos:end_pos].copy()
        event_window['days_from_event'] = range(-len(event_window.iloc[:event_pos-start_pos]), 
                                               len(event_window.iloc[event_pos-start_pos+1:]) + 1)
        
        row = idx // 2
        col = idx % 2
        
        # Plot IHSG returns
        axes[row, col].plot(event_window['days_from_event'], event_window['ihsg_return'], 
                           'o-', color='darkred', linewidth=2, markersize=6)
        axes[row, col].axvline(x=0, color='gray', linestyle='--', alpha=0.7, label='Event Day')
        axes[row, col].axhline(y=0, color='black', linestyle='-', alpha=0.3)
        
        axes[row, col].set_xlabel('Days from Extreme Sentiment')
        axes[row, col].set_ylabel('IHSG Return (%)')
        axes[row, col].set_title(f'Event {idx+1}: Sentiment = {event["net_sent"]:.3f}')
        axes[row, col].legend()
        axes[row, col].grid(True, alpha=0.3)
    
    plt.suptitle('Event Study: Market Returns Around Extreme Sentiment Days', 
                 fontsize=16, y=0.98)
    plt.tight_layout()
    plt.savefig('plots/event_study.png', dpi=300, bbox_inches='tight')
    plt.show()

def plot_volatility_regimes(df):
    """Analyze correlations in different volatility regimes"""
    # Calculate rolling volatility (5-day window)
    df['ihsg_vol'] = df['ihsg_return'].rolling(5).std()
    
    # Define regimes
    vol_median = df['ihsg_vol'].median()
    high_vol = df[df['ihsg_vol'] > vol_median]
    low_vol = df[df['ihsg_vol'] <= vol_median]
    
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(18, 6))
    
    # High volatility regime
    if len(high_vol.dropna()) > 5:
        ax1.scatter(high_vol['net_sent'], high_vol['ihsg_return'], 
                   color='red', alpha=0.6, s=60, label=f'High Vol (n={len(high_vol)})')
        
        # Add regression line
        valid = high_vol.dropna(subset=['net_sent', 'ihsg_return'])
        if len(valid) > 2:
            slope, intercept, r_value, p_value, _ = stats.linregress(
                valid['net_sent'], valid['ihsg_return'])
            line = slope * valid['net_sent'] + intercept
            ax1.plot(valid['net_sent'], line, 'r--', linewidth=2,
                    label=f'R²={r_value**2:.3f}')
    
    ax1.set_xlabel('Net Sentiment')
    ax1.set_ylabel('IHSG Return (%)')
    ax1.set_title('High Volatility Regime', fontsize=14)
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # Low volatility regime
    if len(low_vol.dropna()) > 5:
        ax2.scatter(low_vol['net_sent'], low_vol['ihsg_return'], 
                   color='blue', alpha=0.6, s=60, label=f'Low Vol (n={len(low_vol)})')
        
        # Add regression line
        valid = low_vol.dropna(subset=['net_sent', 'ihsg_return'])
        if len(valid) > 2:
            slope, intercept, r_value, p_value, _ = stats.linregress(
                valid['net_sent'], valid['ihsg_return'])
            line = slope * valid['net_sent'] + intercept
            ax2.plot(valid['net_sent'], line, 'b--', linewidth=2,
                    label=f'R²={r_value**2:.3f}')
    
    ax2.set_xlabel('Net Sentiment')
    ax2.set_ylabel('IHSG Return (%)')
    ax2.set_title('Low Volatility Regime', fontsize=14)
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    # Compare correlations
    high_corr = high_vol['net_sent'].corr(high_vol['ihsg_return'])
    low_corr = low_vol['net_sent'].corr(low_vol['ihsg_return'])
    
    regimes = ['High Vol', 'Low Vol']
    correlations = [high_corr, low_corr]
    colors_reg = ['red', 'blue']
    
    ax3.bar(regimes, correlations, color=colors_reg, alpha=0.7)
    ax3.set_ylabel('Correlation')
    ax3.set_title('Correlation by Volatility Regime', fontsize=14)
    ax3.grid(True, alpha=0.3)
    
    # Add correlation values on bars
    for i, v in enumerate(correlations):
        if not np.isnan(v):
            ax3.text(i, v + 0.01, f'{v:.3f}', ha='center', va='bottom', fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('plots/volatility_regimes.png', dpi=300, bbox_inches='tight')
    plt.show()

def plot_cumulative_returns(df):
    """Cumulative returns after sentiment events"""
    # Calculate cumulative returns
    df['ihsg_cum'] = (1 + df['ihsg_return'] / 100).cumprod() - 1
    df['usd_cum'] = (1 + df['usd_return'] / 100).cumprod() - 1
    
    # Define sentiment thresholds
    high_sent = df['net_sent'] > df['net_sent'].quantile(0.75)
    low_sent = df['net_sent'] < df['net_sent'].quantile(0.25)
    
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10))
    
    # IHSG cumulative returns
    ax1.plot(df['date'], df['ihsg_cum'] * 100, color='darkred', linewidth=2, 
             label='Cumulative IHSG Return')
    
    # Mark high sentiment days
    high_days = df[high_sent]
    ax1.scatter(high_days['date'], high_days['ihsg_cum'] * 100, 
               color='green', s=100, marker='^', 
               label=f'High Sentiment (n={len(high_days)})')
    
    # Mark low sentiment days
    low_days = df[low_sent]
    ax1.scatter(low_days['date'], low_days['ihsg_cum'] * 100, 
               color='red', s=100, marker='v', 
               label=f'Low Sentiment (n={len(low_days)})')
    
    ax1.set_ylabel('Cumulative Return (%)')
    ax1.set_title('Cumulative IHSG Returns with Sentiment Events', fontsize=14)
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # USD/IDR cumulative returns
    ax2.plot(df['date'], df['usd_cum'] * 100, color='darkgreen', linewidth=2, 
             label='Cumulative USD/IDR Return')
    
    ax2.scatter(high_days['date'], high_days['usd_cum'] * 100, 
               color='green', s=100, marker='^')
    ax2.scatter(low_days['date'], low_days['usd_cum'] * 100, 
               color='red', s=100, marker='v')
    
    ax2.set_xlabel('Date')
    ax2.set_ylabel('Cumulative Return (%)')
    ax2.set_title('Cumulative USD/IDR Returns with Sentiment Events', fontsize=14)
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    # Format dates
    import matplotlib.dates as mdates
    for ax in [ax1, ax2]:
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %d'))
        ax.xaxis.set_major_locator(mdates.DayLocator(interval=5))
        plt.setp(ax.xaxis.get_majorticklabels(), rotation=45, ha='right')
    
    plt.tight_layout()
    plt.savefig('plots/cumulative_returns.png', dpi=300, bbox_inches='tight')
    plt.show()

def plot_qq_diagnostics(df):
    """QQ plots and distributional diagnostics"""
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(14, 10))
    
    # QQ plot for sentiment
    stats.probplot(df['net_sent'], dist="norm", plot=ax1)
    ax1.set_title('QQ Plot: Sentiment', fontsize=14)
    ax1.grid(True, alpha=0.3)
    
    # QQ plot for IHSG returns
    returns_ihsg = df['ihsg_return'].dropna()
    stats.probplot(returns_ihsg, dist="norm", plot=ax2)
    ax2.set_title('QQ Plot: IHSG Returns', fontsize=14)
    ax2.grid(True, alpha=0.3)
    
    # Autocorrelation of sentiment
    sentiment_acf = acf(df['net_sent'], nlags=10, fft=False)
    lags = range(len(sentiment_acf))
    ax3.bar(lags, sentiment_acf, color='steelblue', alpha=0.7)
    ax3.axhline(y=0, color='black', linestyle='-', alpha=0.3)
    ax3.axhline(y=-1.96/np.sqrt(len(df)), color='red', linestyle='--', alpha=0.7)
    ax3.axhline(y=1.96/np.sqrt(len(df)), color='red', linestyle='--', alpha=0.7)
    ax3.set_xlabel('Lag')
    ax3.set_ylabel('Autocorrelation')
    ax3.set_title('Sentiment Autocorrelation', fontsize=14)
    ax3.grid(True, alpha=0.3)
    
    # Partial autocorrelation of sentiment
    sentiment_pacf = pacf(df['net_sent'], nlags=10)
    lags = range(len(sentiment_pacf))
    ax4.bar(lags, sentiment_pacf, color='darkorange', alpha=0.7)
    ax4.axhline(y=0, color='black', linestyle='-', alpha=0.3)
    ax4.axhline(y=-1.96/np.sqrt(len(df)), color='red', linestyle='--', alpha=0.7)
    ax4.axhline(y=1.96/np.sqrt(len(df)), color='red', linestyle='--', alpha=0.7)
    ax4.set_xlabel('Lag')
    ax4.set_ylabel('Partial Autocorrelation')
    ax4.set_title('Sentiment Partial Autocorrelation', fontsize=14)
    ax4.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('plots/qq_diagnostics.png', dpi=300, bbox_inches='tight')
    plt.show()

def plot_lag_structure(df):
    """Analyze correlation structure across multiple lags"""
    max_lags = 5
    
    # Calculate correlations at different lags
    correlations_ihsg = []
    correlations_usd = []
    
    for lag in range(max_lags + 1):
        if lag == 0:
            corr_ihsg = df['net_sent'].corr(df['ihsg_return'])
            corr_usd = df['net_sent'].corr(df['usd_return'])
        else:
            sent_lagged = df['net_sent'].shift(lag)
            corr_ihsg = sent_lagged.corr(df['ihsg_return'])
            corr_usd = sent_lagged.corr(df['usd_return'])
        
        correlations_ihsg.append(corr_ihsg)
        correlations_usd.append(corr_usd)
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    # Plot lag structure
    lags = range(max_lags + 1)
    ax1.plot(lags, correlations_ihsg, 'o-', color='darkred', linewidth=2, 
             markersize=8, label='IHSG')
    ax1.plot(lags, correlations_usd, 's-', color='darkgreen', linewidth=2, 
             markersize=8, label='USD/IDR')
    
    ax1.set_xlabel('Lag (Days)')
    ax1.set_ylabel('Correlation')
    ax1.set_title('Sentiment-Market Correlations by Lag', fontsize=14)
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # Add significance indicators
    n_obs = len(df)
    critical_val = 1.96 / np.sqrt(n_obs)
    ax1.axhline(y=critical_val, color='gray', linestyle='--', alpha=0.5, 
                label='Approx. Significance')
    ax1.axhline(y=-critical_val, color='gray', linestyle='--', alpha=0.5)
    ax1.legend()
    
    # Heatmap of lagged correlations
    lagged_corr_matrix = np.zeros((max_lags + 1, 2))
    lagged_corr_matrix[:, 0] = correlations_ihsg
    lagged_corr_matrix[:, 1] = correlations_usd
    
    im = ax2.imshow(lagged_corr_matrix.T, cmap='coolwarm', aspect='auto', 
                    interpolation='nearest')
    ax2.set_xticks(range(max_lags + 1))
    ax2.set_xticklabels([f'Lag {i}' for i in range(max_lags + 1)])
    ax2.set_yticks([0, 1])
    ax2.set_yticklabels(['IHSG', 'USD/IDR'])
    ax2.set_title('Correlation Heatmap by Lag', fontsize=14)
    
    # Add correlation values
    for i in range(max_lags + 1):
        for j in range(2):
            text = ax2.text(i, j, f'{lagged_corr_matrix[i, j]:.3f}',
                           ha="center", va="center", color="black", fontweight='bold')
    
    plt.colorbar(im, ax=ax2, shrink=0.8)
    
    plt.tight_layout()
    plt.savefig('plots/lag_structure.png', dpi=300, bbox_inches='tight')
    plt.show()

def main():
    """Generate all advanced visualizations"""
    print("Loading data...")
    df = load_data()
    
    print("\nGenerating advanced visualizations...")
    
    print("\n1. Event Study Analysis")
    plot_event_study(df)
    
    print("\n2. Volatility Regimes")
    plot_volatility_regimes(df)
    
    print("\n3. Cumulative Returns")
    plot_cumulative_returns(df)
    
    print("\n4. QQ Diagnostics")
    plot_qq_diagnostics(df)
    
    print("\n5. Lag Structure Analysis")
    plot_lag_structure(df)
    
    print("\nAll advanced visualizations saved to 'plots/' directory!")

if __name__ == "__main__":
    main()