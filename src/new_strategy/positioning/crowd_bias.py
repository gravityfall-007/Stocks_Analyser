def crowd_bias(df):
    """
    Uses volume + volatility as retail crowd proxy
    """
    vol_spike = df['Volume'] / df['Volume'].rolling(20).mean()
    price_volatility = df['Close'].pct_change().rolling(10).std()

    crowd_score = vol_spike * price_volatility

    return {
        "crowd_bias": "Crowded" if crowd_score.mean() > 1 else "Neutral",
        "crowd_score": round(crowd_score.mean(), 2)
    }
