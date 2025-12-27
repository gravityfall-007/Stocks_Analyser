import yfinance as yf

def load_fundamentals(ticker):
    return yf.Ticker(ticker).info
