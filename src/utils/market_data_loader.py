import pandas as pd
import os

def load_price_data(ticker, base_dir="data/processed"):
    path = os.path.join(base_dir, f"{ticker}_prices.csv")
    if not os.path.exists(path):
        raise FileNotFoundError(f"No price data for {ticker}")
    return pd.read_csv(path, index_col=0, parse_dates=True)
