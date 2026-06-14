import yfinance as yf
import pandas as pd
import datetime
import os

print("Fetching IHSG data...")
end_date = datetime.date.today().isoformat()
ihsg = yf.download("^JKSE", start="1995-01-01", end=end_date)
print(f"IHSG data shape: {ihsg.shape}")
print(f"Latest date: {ihsg.index[-1] if not ihsg.empty else 'No data'}")

# Save to CSV
ihsg_path = "ihsg_daily.csv"
ihsg.to_csv(ihsg_path)
print(f"Saved IHSG data to {ihsg_path}")

print("\nFetching USD/IDR data...")
ticker_symbol = "IDR=X"
usd_idr = yf.Ticker(ticker_symbol)
hist_data = usd_idr.history(period="max")
if hist_data.empty:
    print(f"No data found for ticker {ticker_symbol}.")
else:
    print(f"USD/IDR data fetched from {hist_data.index.min().date()} to {hist_data.index.max().date()}.")
    usd_idr_path = "usd_idr_daily.csv"
    hist_data.to_csv(usd_idr_path)
    print(f"Saved USD/IDR data to {usd_idr_path}")

print("\nDone.")