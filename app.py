import streamlit as st
import pandas as pd
from screener import rank_stocks
from predictor import forecast_prices
from charts import plot_forecast_vs_actual, compute_rmse
from intraday_predictor import forecast_intraday

st.set_page_config(page_title="📈 Multi-Horizon Stock Forecaster", layout="wide")
st.title("🔮 AI-Powered Stock Forecast & Allocation Dashboard")

# 🔘 User Input
tickers_input = st.text_input(
    "Enter comma-separated NSE tickers (e.g. RELIANCE.NS, TCS.NS, INFY.NS)",
    value="RELIANCE.NS, TCS.NS, INFY.NS, ICICIBANK.NS, SBIN.NS"
)
tickers = [t.strip().upper() for t in tickers_input.split(",") if t.strip()]
allocation_total = st.number_input("Total Investment Capital (₹)", value=500000, step=10000)

run_button = st.button("🚀 Run Prediction & Allocation")
ranked = []

if run_button:
    st.subheader("📊 Top Ranked Stocks")
    ranked = rank_stocks(tickers)
    if not ranked:
        st.error("No valid tickers could be scored. Please check your input symbols.")
    else:
        df_ranked = pd.DataFrame(ranked, columns=["Ticker", "Score", "Trend"])
        st.dataframe(df_ranked, use_container_width=True)

        n_stocks = len(ranked)
        per_stock = allocation_total // n_stocks
        st.success(f"💸 Allocating ₹{allocation_total:,} equally: ₹{per_stock:,} per stock")

        # Forecasting Tabs
        tabs = st.tabs(["📅 1 Week", "📆 1 Month", "📘 3 Months", "📙 6 Months", "📗 1 Year"])
        horizons = ["7d", "30d", "90d", "180d", "365d"]

        for tab, horizon in zip(tabs, horizons):
            with tab:
                for ticker, _, _ in ranked:
                    st.markdown(f"### 📌 {ticker}")
                    forecast = forecast_prices(ticker, horizon=horizon)

                    if forecast is not None:
                        st.plotly_chart(plot_forecast_vs_actual(forecast, ticker), use_container_width=True)
                        rmse = compute_rmse(forecast)
                        st.metric(label=f"📉 RMSE ({horizon})", value=f"{rmse:.2f}")
                        st.markdown(f"💰 Recommended Investment: ₹{per_stock:,}")
                    else:
                        st.warning(f"⚠️ Forecast unavailable for {ticker} at {horizon}.")

from intraday_predictor import forecast_intraday
from charts import plot_intraday_forecast

st.markdown("---")
st.subheader("⏱️ Intraday Forecast Explorer")

if ranked:
    intraday_stock = st.selectbox("Select Stock for Intraday Forecast", [s[0] for s in ranked])
    interval = st.selectbox("Select Interval", ["5m", "10m", "15m", "30m", "45m", "1h", "2h", "3h", "4h", "8h"])

    forecast = forecast_intraday(intraday_stock, interval=interval)
    if forecast is not None:
        st.markdown(f"### 🔍 {intraday_stock.upper()} @ {interval} Forecast")
        st.plotly_chart(plot_intraday_forecast(forecast, intraday_stock, interval), use_container_width=True)

        high = forecast["yhat_upper"].max()
        low = forecast["yhat_lower"].min()
        st.metric("🔼 Predicted High", f"₹{high:.2f}")
        st.metric("🔽 Predicted Low", f"₹{low:.2f}")
    else:
        st.warning("⚠️ Intraday forecast unavailable for this stock/interval.")
