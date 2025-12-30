from src.new_strategy.llm.groq_client import generate_llm_summary

def philosophy_summary(metrics: dict) -> str:
    """
    Convert computed metrics into a structured LLM prompt.
    """

    prompt = f"""
Market Structure Summary:

• Market Regime: {metrics.get("regime")}
• Regime Strength Score: {metrics.get("regime_score")}

• Trend Quality: {metrics.get("trend_quality")}
• Trend Efficiency: {metrics.get("trend_efficiency")}

• Cycle State: {metrics.get("cycle_state")}
• Range Compression Score: {metrics.get("range_score")}

• Crowd Bias: {metrics.get("crowd_bias")}
• Trader Stress Level: {metrics.get("stress_level")}
• Blowup Risk Level: {metrics.get("blowup_risk")}

Explain what this environment implies about:
1. Market structure
2. Risk conditions
3. Trader psychology
4. Time vs trend considerations

Do not provide predictions or trade advice.
"""

    return generate_llm_summary(prompt)
