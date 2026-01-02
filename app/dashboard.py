import streamlit as st
import sys
import os

# -------------------------------------------------
# Path setup
# -------------------------------------------------
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
if project_root not in sys.path:
    sys.path.append(project_root)

# -------------------------------------------------
# Report & Data Loaders
# -------------------------------------------------
from src.utils.report_loader import (
    load_available_reports,
    load_report
)

from src.utils.relative_loader import load_relative_performance
from src.utils.market_data_loader import load_market_data

# -------------------------------------------------
# Renderers (existing)
# -------------------------------------------------
from app.renders.cost_scale import render_cost_scale
from app.renders.market_position import render_market_position
from app.renders.security import render_security
from app.renders.relative_performance import render_relative_performance

# -------------------------------------------------
# NEW: Philosophy & Risk new_strategy
# -------------------------------------------------
from src.new_strategy.market_philosophy.regime_detector import market_regime
from src.new_strategy.market_philosophy.trend_quality import trend_efficiency
from src.new_strategy.positioning.crowd_bias import crowd_bias
from src.new_strategy.cycles.range_cycle_detector import range_cycle
from src.new_strategy.risk.blowup_risk import blowup_risk
from src.new_strategy.psychology.trader_stress_index import stress_index
from src.new_strategy.llm.philosophy_summary import philosophy_summary


# -------------------------------------------------
# NEW: Forecasting, Evaluation & Explainability
# -------------------------------------------------
from src.forecasting.statsmodels_sarimax import StatsmodelsSARIMAX
from src.forecasting.statsmodels_ets import StatsmodelsETS
from src.forecasting.meta_prophet_model import ProphetForecaster
from src.forecasting.tbats_model import TBATSForecaster
from src.forecasting.darts_nbeats import DartsNBEATS
from src.forecasting.sktime_model import SKTimeML
from src.forecasting.pytorch_tft import PyTorchTFT
#from src.forecasting.gluonts_deepar import GluonTSDeepAR

from src.evaluation.backtesting import walk_forward_validation
from src.registry.model_registry import ModelRegistry
from src.new_strategy.llm.groq_client import explain

# -------------------------------------------------
# Page Config
# -------------------------------------------------
st.set_page_config(
    page_title="Bloomberg-Style Company Analysis",
    layout="wide"
)

st.title("📊 Stocks Analyzer")

# -------------------------------------------------
# Sidebar – Company Selector
# -------------------------------------------------
st.sidebar.header("Company Universe")

available_tickers = load_available_reports()

ticker = st.sidebar.selectbox(
    "Select Company",
    options=available_tickers
)

# -------------------------------------------------
# Load Data
# -------------------------------------------------
report = load_report(ticker)
df = load_market_data(ticker)

# -------------------------------------------------
# Header
# -------------------------------------------------
st.subheader(f"{ticker} — Analytical Overview")
st.divider()

# -------------------------------------------------
# Tabs
# -------------------------------------------------
tabs = st.tabs([
    "Cost & Scale",
    "Market Position",
    "Security",
    "Market Structure",
    "Relative Performance",
    "Compare Companies",
    "Forecasting & Evaluation"
])

# -------------------------------------------------
# Existing Tabs
# -------------------------------------------------
with tabs[0]:
    render_cost_scale(report)

with tabs[1]:
    render_market_position(report)

with tabs[2]:
    render_security(report)

# -------------------------------------------------
# NEW: Market Structure & Philosophy
# -------------------------------------------------
with tabs[3]:
    st.subheader("📐 Market Structure & Risk Context")

    col1, col2, col3 = st.columns(3)

    regime = market_regime(df)
    trend = trend_efficiency(df)
    cycle = range_cycle(df)

    with col1:
        st.metric("Market Regime", regime["regime"])
        st.caption(f"Regime Score: {regime['regime_score']}")

    with col2:
        st.metric("Trend Quality", trend["trend_quality"])
        st.caption(f"Efficiency: {trend['trend_efficiency']}")

    with col3:
        st.metric("Cycle State", cycle["cycle_state"])
        st.caption(f"Range Score: {cycle['range_score']}")

    st.divider()

    col4, col5, col6 = st.columns(3)

    crowd = crowd_bias(df)
    stress = stress_index(df)
    risk = blowup_risk(
        volatility=df['Close'].pct_change().rolling(20).std().iloc[-1]
    )

    with col4:
        st.metric("Crowd Bias", crowd["crowd_bias"])
        if crowd["crowd_bias"] == "Crowded":
            st.warning("High public participation detected")

    with col5:
        st.metric("Trader Stress", stress["stress_level"])
        if stress["stress_level"] == "High":
            st.warning("Volatility-driven stress environment")

    with col6:
        st.metric("Blowup Risk", risk["blowup_risk"])
        st.caption(f"Risk Score: {risk['risk_score']}")

    st.divider()

    st.subheader("🧠 Market Philosophy Summary")

    philosophy_prompt = philosophy_summary({
        **regime,
        **trend,
        **cycle,
        **crowd,
        **stress,
        **risk
    })

    st.info("LLM-generated interpretive summary (non-predictive)")
    st.write(philosophy_prompt)

# -------------------------------------------------
# Relative Performance
# -------------------------------------------------
with tabs[4]:
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

# -------------------------------------------------
# Compare Companies
# -------------------------------------------------
with tabs[5]:
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


# -------------------------------------------------
# NEW: Forecasting & Evaluation
# -------------------------------------------------
with tabs[6]:
    st.subheader("📈 Forecasting & Model Evaluation")

    price_series = df["Close"].dropna()

    # -----------------------------
    # Sidebar-like controls
    # -----------------------------
    col1, col2, col3 = st.columns(3)

    with col1:
        horizon = st.number_input("Forecast Horizon (days)", 7, 90, 30)

    with col2:
        train_size = st.number_input(
            "Backtest Train Size",
            min_value=100,
            max_value=len(price_series) - horizon,
            value=min(300, len(price_series) - horizon)
        )

    with col3:
        metric_choice = st.selectbox(
            "Model Selection Metric",
            ["avg_rmse", "avg_mae"]
        )

    st.divider()

    # -----------------------------
    # Model Registry
    # -----------------------------
    registry = ModelRegistry()

    registry.register("SARIMAX", StatsmodelsSARIMAX())
    registry.register("ETS", StatsmodelsETS())
    registry.register("Prophet", ProphetForecaster())
    registry.register("TBATS", TBATSForecaster())
    registry.register("Darts", DartsNBEATS())
    registry.register("sktime", SKTimeML())
    #registry.register("PyTorch TFT", PyTorchTFT())
    #registry.register("GluonTS DeepAR", GluonTSDeepAR())


    # -----------------------------
    # Run Evaluation
    # -----------------------------
    if st.button("🚀 Run Backtesting & Auto-Select Model"):
        with st.spinner("Running walk-forward validation..."):
            registry.evaluate(
                price_series,
                backtest_fn=walk_forward_validation,
                train_size=train_size,
                horizon=horizon
            )

        best_name, best_result = registry.best_model(metric=metric_choice)

        st.success(f"✅ Best Model: **{best_name}**")

        # -----------------------------
        # Metrics Display
        # -----------------------------
        colA, colB = st.columns(2)

        with colA:
            st.metric("Average RMSE", f"{best_result['avg_rmse']:.4f}")

        with colB:
            st.metric("Average MAE", f"{best_result['avg_mae']:.4f}")

        st.divider()

        # -----------------------------
        # Forecast with Best Model
        # -----------------------------
        best_model = registry.models[best_name]
        best_model.fit(price_series)
        forecast = best_model.forecast(horizon)

        st.subheader("📊 Price Forecast")
        st.line_chart(forecast)

        # -----------------------------
        # LLM Explanation
        # -----------------------------
        st.subheader("🧠 Forecast Explanation")

        explainer = ForecastExplainer(
            api_key=os.getenv("GROQ_API_KEY")
        )

        explanation = explainer.explain(
            model_name=best_name,
            metrics=best_result,
            horizon=horizon
        )

        st.info("LLM-generated forecast reasoning (non-financial advice)")
        st.write(explanation)
