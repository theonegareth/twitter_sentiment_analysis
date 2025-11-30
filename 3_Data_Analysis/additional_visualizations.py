"""
Additional Visualizations for Sentiment-Market Analysis
Creates supplementary plots to better understand the data and results
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import os

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

def plot_sentiment_distribution(df):
    """Plot sentiment score distribution"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    # Histogram
    ax1.hist(df['net_sent'], bins=15, color='steelblue', alpha=0.7, edgecolor='black')
    ax1.set_xlabel('Net Sentiment Score')
    ax1.set_ylabel('Frequency')
    ax1.set_title('Distribution of Net Sentiment Scores', fontsize=14)
    ax1.grid(True, alpha=0.3)
    
    # Add statistics text
    mean_sent = df['net_sent'].mean()
    std_sent = df['net_sent'].std()
    ax1.axvline(mean_sent, color='red', linestyle='--', label=f'Mean: {mean_sent:.2f}')
    ax1.legend()
    
    # Box plot
    ax2.boxplot(df['net_sent'], vert=True, patch_artist=True, 
                boxprops=dict(facecolor='lightblue', color='blue'),
                medianprops=dict(color='red', linewidth=2))
    ax2.set_ylabel('Net Sentiment Score')
    ax2.set_title('Sentiment Box Plot', fontsize=14)
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('plots/sentiment_distribution.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    print(f"Sentiment Statistics:")
    print(f"Mean: {mean_sent:.3f}")
    print(f"Std: {std_sent:.3f}")
    print(f"Min: {df['net_sent'].min():.3f}")
    print(f"Max: {df['net_sent'].max():.3f}")

def plot_returns_distribution(df):
    """Plot market returns distribution"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    # IHSG returns
    returns_ihsg = df['ihsg_return'].dropna()
    ax1.hist(returns_ihsg, bins=12, color='darkred', alpha=0.7, edgecolor='black')
    ax1.set_xlabel('IHSG Daily Return (%)')
    ax1.set_ylabel('Frequency')
    ax1.set_title('Distribution of IHSG Returns', fontsize=14)
    ax1.grid(True, alpha=0.3)
    
    # Add statistics
    mean_ihsg = returns_ihsg.mean()
    ax1.axvline(mean_ihsg, color='red', linestyle='--', label=f'Mean: {mean_ihsg:.2f}%')
    ax1.legend()
    
    # USD/IDR returns
    returns_usd = df['usd_return'].dropna()
    ax2.hist(returns_usd, bins=12, color='darkgreen', alpha=0.7, edgecolor='black')
    ax2.set_xlabel('USD/IDR Daily Return (%)')
    ax2.set_ylabel('Frequency')
    ax2.set_title('Distribution of USD/IDR Returns', fontsize=14)
    ax2.grid(True, alpha=0.3)
    
    mean_usd = returns_usd.mean()
    ax2.axvline(mean_usd, color='red', linestyle='--', label=f'Mean: {mean_usd:.2f}%')
    ax2.legend()
    
    plt.tight_layout()
    plt.savefig('plots/returns_distribution.png', dpi=300, bbox_inches='tight')
    plt.show()

def plot_granger_results():
    """Visualize Granger causality test results"""
    gc_results = pd.read_csv('granger_causality_results.csv')
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
    
    # Plot F-statistics
    for test in gc_results['Test'].unique():
        data = gc_results[gc_results['Test'] == test]
        marker = 'o-' if 'IHSG' in test else 's--'
        ax1.plot(data['Lag'], data['F-Statistic'], marker, 
                label=test, linewidth=2, markersize=8)
    
    ax1.set_xlabel('Lag (Days)')
    ax1.set_ylabel('F-Statistic')
    ax1.set_title('Granger Causality F-Statistics', fontsize=14)
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # Add significance threshold line
    ax1.axhline(y=2.5, color='gray', linestyle=':', alpha=0.7, 
                label='Approx. Significance Threshold')
    
    # Plot p-values
    for test in gc_results['Test'].unique():
        data = gc_results[gc_results['Test'] == test]
        marker = 'o-' if 'IHSG' in test else 's--'
        ax2.plot(data['Lag'], data['P-Value'], marker,
                label=test, linewidth=2, markersize=8)
    
    ax2.set_xlabel('Lag (Days)')
    ax2.set_ylabel('P-Value')
    ax2.set_title('Granger Causality P-Values', fontsize=14)
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    # Add significance lines
    ax2.axhline(y=0.05, color='red', linestyle='--', alpha=0.7, label='5% Significance')
    ax2.axhline(y=0.10, color='orange', linestyle='--', alpha=0.7, label='10% Significance')
    ax2.legend()
    
    plt.tight_layout()
    plt.savefig('plots/granger_causality_visualization.png', dpi=300, bbox_inches='tight')
    plt.show()

def plot_rolling_correlations(df):
    """Plot rolling window correlations"""
    # Calculate rolling correlations (10-day window)
    window = 10
    rolling_corr_ihsg = df['net_sent'].rolling(window).corr(df['ihsg_return'])
    rolling_corr_usd = df['net_sent'].rolling(window).corr(df['usd_return'])
    
    fig, ax = plt.subplots(figsize=(14, 7))
    
    ax.plot(df['date'], rolling_corr_ihsg, color='red', linewidth=2, 
            label=f'Sentiment-IHSG (Rolling {window}d)', marker='o', markersize=4)
    ax.plot(df['date'], rolling_corr_usd, color='green', linewidth=2, 
            label=f'Sentiment-USD/IDR (Rolling {window}d)', marker='s', markersize=4)
    
    ax.set_xlabel('Date')
    ax.set_ylabel('Rolling Correlation')
    ax.set_title(f'Rolling {window}-Day Correlations: Sentiment vs Markets', fontsize=14)
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    # Format dates
    import matplotlib.dates as mdates
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %d'))
    ax.xaxis.set_major_locator(mdates.DayLocator(interval=5))
    plt.setp(ax.xaxis.get_majorticklabels(), rotation=45, ha='right')
    
    plt.tight_layout()
    plt.savefig('plots/rolling_correlations.png', dpi=300, bbox_inches='tight')
    plt.show()

def plot_scatter_with_regression(df):
    """Scatter plots with regression lines"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    # Sentiment vs IHSG
    valid_ihsg = df.dropna(subset=['ihsg_return'])
    ax1.scatter(valid_ihsg['net_sent'], valid_ihsg['ihsg_return'], 
               color='red', alpha=0.6, s=50)
    
    # Add regression line
    if len(valid_ihsg) > 2:
        slope, intercept, r_value, p_value, std_err = stats.linregress(
            valid_ihsg['net_sent'], valid_ihsg['ihsg_return'])
        line = slope * valid_ihsg['net_sent'] + intercept
        ax1.plot(valid_ihsg['net_sent'], line, 'r--', linewidth=2,
                label=f'R²={r_value**2:.3f}, p={p_value:.3f}')
    
    ax1.set_xlabel('Net Sentiment')
    ax1.set_ylabel('IHSG Daily Return (%)')
    ax1.set_title('Sentiment vs IHSG Returns', fontsize=14)
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # Sentiment vs USD/IDR
    valid_usd = df.dropna(subset=['usd_return'])
    ax2.scatter(valid_usd['net_sent'], valid_usd['usd_return'], 
               color='green', alpha=0.6, s=50)
    
    # Add regression line
    if len(valid_usd) > 2:
        slope, intercept, r_value, p_value, std_err = stats.linregress(
            valid_usd['net_sent'], valid_usd['usd_return'])
        line = slope * valid_usd['net_sent'] + intercept
        ax2.plot(valid_usd['net_sent'], line, 'g--', linewidth=2,
                label=f'R²={r_value**2:.3f}, p={p_value:.3f}')
    
    ax2.set_xlabel('Net Sentiment')
    ax2.set_ylabel('USD/IDR Daily Return (%)')
    ax2.set_title('Sentiment vs USD/IDR Returns', fontsize=14)
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('plots/scatter_regression.png', dpi=300, bbox_inches='tight')
    plt.show()

def plot_extreme_sentiment_days(df):
    """Highlight extreme sentiment days"""
    # Define extreme days (top/bottom 20%)
    sent_80th = df['net_sent'].quantile(0.8)
    sent_20th = df['net_sent'].quantile(0.2)
    
    extreme_high = df[df['net_sent'] >= sent_80th]
    extreme_low = df[df['net_sent'] <= sent_20th]
    
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10))
    
    # Plot sentiment with extreme days highlighted
    ax1.plot(df['date'], df['net_sent'], color='blue', linewidth=2, label='Net Sentiment')
    ax1.scatter(extreme_high['date'], extreme_high['net_sent'], 
               color='green', s=100, marker='^', label=f'High Sentiment (≥{sent_80th:.2f})')
    ax1.scatter(extreme_low['date'], extreme_low['net_sent'], 
               color='red', s=100, marker='v', label=f'Low Sentiment (≤{sent_20th:.2f})')
    
    ax1.set_ylabel('Net Sentiment')
    ax1.set_title('Extreme Sentiment Days', fontsize=14)
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # Show market returns on extreme days
    x_pos = np.arange(len(extreme_high) + len(extreme_low))
    colors = ['green'] * len(extreme_high) + ['red'] * len(extreme_low)
    
    combined_extreme = pd.concat([extreme_high, extreme_low])
    
    ax2.bar(x_pos, combined_extreme['ihsg_return'], 
            color=colors, alpha=0.7, label='IHSG Return')
    
    ax2.set_xlabel('Extreme Sentiment Events')
    ax2.set_ylabel('IHSG Return (%)')
    ax2.set_title('Market Returns on Extreme Sentiment Days', fontsize=14)
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('plots/extreme_sentiment_days.png', dpi=300, bbox_inches='tight')
    plt.show()

def plot_correlation_matrix_enhanced(df):
    """Enhanced correlation matrix with more variables"""
    # Create additional variables
    df['sentiment_lag1'] = df['net_sent'].shift(1)
    df['ihsg_lag1'] = df['ihsg_return'].shift(1)
    df['usd_lag1'] = df['usd_return'].shift(1)
    
    # Select variables for correlation
    corr_vars = ['net_sent', 'sentiment_lag1', 'ihsg_return', 'ihsg_lag1', 
                 'usd_return', 'usd_lag1']
    corr_data = df[corr_vars].corr()
    
    # Rename for clarity
    corr_data.columns = ['Sentiment', 'Sentiment_Lag1', 'IHSG', 'IHSG_Lag1', 
                        'USD/IDR', 'USD/IDR_Lag1']
    corr_data.index = ['Sentiment', 'Sentiment_Lag1', 'IHSG', 'IHSG_Lag1', 
                      'USD/IDR', 'USD/IDR_Lag1']
    
    fig, ax = plt.subplots(figsize=(10, 8))
    
    # Create heatmap
    mask = np.triu(np.ones_like(corr_data, dtype=bool))
    sns.heatmap(corr_data, annot=True, cmap='coolwarm', center=0, 
                square=True, linewidths=0.5, cbar_kws={"shrink": 0.8},
                mask=mask, ax=ax)
    
    ax.set_title('Enhanced Correlation Matrix\n(With Lagged Variables)', 
                 fontsize=14, pad=20)
    
    plt.tight_layout()
    plt.savefig('plots/enhanced_correlation_matrix.png', dpi=300, bbox_inches='tight')
    plt.show()

def main():
    """Generate all additional visualizations"""
    print("Loading data...")
    df = load_data()
    
    print("\nGenerating additional visualizations...")
    
    print("\n1. Sentiment Distribution")
    plot_sentiment_distribution(df)
    
    print("\n2. Returns Distribution")
    plot_returns_distribution(df)
    
    print("\n3. Granger Causality Visualization")
    plot_granger_results()
    
    print("\n4. Rolling Correlations")
    plot_rolling_correlations(df)
    
    print("\n5. Scatter Plots with Regression")
    plot_scatter_with_regression(df)
    
    print("\n6. Extreme Sentiment Days")
    plot_extreme_sentiment_days(df)
    
    print("\n7. Enhanced Correlation Matrix")
    plot_correlation_matrix_enhanced(df)
    
    print("\nAll additional visualizations saved to 'plots/' directory!")

if __name__ == "__main__":
    main()