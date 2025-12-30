from src.utils.market_data_loader import load_market_data
from src.utils.performance import normalize_prices

def load_relative_performance(tickers):
    series = {}

    for ticker in tickers:
        df = load_market_data(ticker)
        series[ticker] = normalize_prices(df)

    return series
