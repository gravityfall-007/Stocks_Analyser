def trend_efficiency(df):
    net_move = abs(df['Close'].iloc[-1] - df['Close'].iloc[0])
    total_move = df['Close'].diff().abs().sum()

    efficiency = net_move / total_move

    return {
        "trend_efficiency": round(efficiency, 2),
        "trend_quality": "Clean" if efficiency > 0.4 else "Choppy"
    }
