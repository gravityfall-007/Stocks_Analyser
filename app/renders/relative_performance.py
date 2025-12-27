import streamlit as st
import plotly.graph_objects as go

def render_relative_performance(performance_series):
    st.subheader("📊 Relative Performance (Indexed)")

    fig = go.Figure()

    for ticker, series in performance_series.items():
        fig.add_trace(go.Scatter(
            x=series.index,
            y=series.values,
            mode="lines",
            name=ticker
        ))

    fig.update_layout(
        template="plotly_dark",
        height=450,
        margin=dict(l=20, r=20, t=30, b=20),
        yaxis_title="Indexed Performance (Base = 100)",
        xaxis_title="Date"
    )

    st.plotly_chart(fig, use_container_width=True)
