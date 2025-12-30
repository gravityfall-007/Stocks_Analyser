import pandas as pd
import numpy as np

def market_regime(df):
    """
    Detects regime: Trending vs Ranging
    """
    returns = df['Close'].pct_change()
    volatility = returns.rolling(20).std()

    trend_strength = abs(df['Close'].pct_change(20))
    regime_score = trend_strength / volatility

    return {
        "regime": "Trending" if regime_score.mean() > 1.5 else "Ranging",
        "regime_score": round(regime_score.mean(), 2)
    }
