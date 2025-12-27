import streamlit as st
import pandas as pd

def render_cost_scale(report):
    data = report.get("CostScaleAnalyzer", {})

    st.subheader("🏭 Cost & Scale")

    col1, col2 = st.columns(2)

    col1.metric("Revenue", f"${data.get('revenue', 0):,}")
    col2.metric("Operating Margin", data.get("operating_margin", "N/A"))

    # Simple visualization
    df = pd.DataFrame({
        "Metric": ["Revenue"],
        "Value": [data.get("revenue", 0)]
    })

    st.bar_chart(df.set_index("Metric"))
