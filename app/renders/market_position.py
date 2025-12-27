import streamlit as st
import pandas as pd

def render_market_position(report):
    data = report.get("MarketPositionAnalyzer", {})

    st.subheader("🏆 Market Position")

    df = pd.DataFrame.from_dict(
        data, orient="index", columns=["Assessment"]
    )

    st.dataframe(df, use_container_width=True)
