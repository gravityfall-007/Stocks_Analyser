import yfinance as yf

def load_market_data(ticker, period="5y"):
    stock = yf.Ticker(ticker)
    return stock.history(period=period)
