def blowup_risk(volatility, position_size=0.04):
    risk = volatility * position_size * 100

    return {
        "blowup_risk": "High" if risk > 2 else "Acceptable",
        "risk_score": round(risk, 2)
    }
