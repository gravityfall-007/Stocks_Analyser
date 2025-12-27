from src.utils.market_data_loader import load_price_data
from src.utils.performance import normalize_prices

def load_relative_performance(tickers):
    series = {}

    for ticker in tickers:
        df = load_price_data(ticker)
        series[ticker] = normalize_prices(df)

    return series
