import streamlit as st
import sys
import os

# Add project root to sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
if project_root not in sys.path:
    sys.path.append(project_root)

from src.utils.report_loader import (
    load_available_reports,
    load_report
)

from app.renders.cost_scale import render_cost_scale
from app.renders.market_position import render_market_position
from app.renders.security import render_security
from src.utils.relative_loader import load_relative_performance
from app.renders.relative_performance import render_relative_performance


# -------------------------------------------------
# Page Config
# -------------------------------------------------
st.set_page_config(
    page_title="Bloomberg-Style Company Analysis",
    layout="wide"
)

st.title("📊 Stocks Analyzer")

# -------------------------------------------------
# Sidebar – Report Selector
# -------------------------------------------------
st.sidebar.header("Company Universe")

available_tickers = load_available_reports()

ticker = st.sidebar.selectbox(
    "Select Company",
    options=available_tickers
)

# -------------------------------------------------
# Load Report
# -------------------------------------------------
report = load_report(ticker)

# -------------------------------------------------
# Header
# -------------------------------------------------
st.subheader(f"{ticker} — Analytical Overview")

st.divider()

# -------------------------------------------------
# Tabs (Bloomberg Functions)
# -------------------------------------------------
tabs = st.tabs([
    "Cost & Scale",
    "Market Position",
    "Security",
    "Relative Performance"
])

with tabs[0]:
    render_cost_scale(report)

with tabs[1]:
    render_market_position(report)

with tabs[2]:
    render_security(report)

with tabs[3]:
    st.write("Compare multiple stocks relative to a common base value.")

    selected = st.multiselect(
        "Select stocks to compare",
        options=available_tickers,
        default=available_tickers[:3]
    )

    if len(selected) >= 2:
        perf_data = load_relative_performance(selected)
        render_relative_performance(perf_data)
    else:
        st.warning("Select at least two stocks for comparison.")


compare_tab, = st.tabs(["Compare Companies"])

with compare_tab:
    selected = st.multiselect(
        "Select companies to compare",
        options=available_tickers,
        default=available_tickers[:3]
    )

    rows = []
    for t in selected:
        r = load_report(t)
        cs = r["CostScaleAnalyzer"]
        rows.append({
            "Ticker": t,
            "Revenue": cs.get("revenue", 0),
            "Economies of Scale": cs.get("economies_of_scale")
        })

    st.dataframe(rows, use_container_width=True)

