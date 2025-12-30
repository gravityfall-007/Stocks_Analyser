def stress_index(df):
    volatility = df['Close'].pct_change().rolling(10).std()
    stress = volatility / volatility.mean()

    return {
        "stress_level": "High" if stress.iloc[-1] > 1.5 else "Normal",
        "stress_score": round(stress.iloc[-1], 2)
    }
