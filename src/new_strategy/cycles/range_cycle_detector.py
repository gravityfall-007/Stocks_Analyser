def range_cycle(df):
    high_low_range = (df['High'] - df['Low']) / df['Close']
    compression = high_low_range.rolling(20).mean()

    return {
        "cycle_state": "Compression" if compression.iloc[-1] < compression.mean() else "Expansion",
        "range_score": round(compression.iloc[-1], 4)
    }
