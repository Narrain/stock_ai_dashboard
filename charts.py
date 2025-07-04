import plotly.graph_objects as go
from sklearn.metrics import mean_squared_error
import numpy as np

# 📈 Long-Term Forecast vs Actual Plot
def plot_forecast_vs_actual(forecast_df, ticker):
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=forecast_df["ds"],
        y=forecast_df["actual"],
        mode="lines",
        name="Actual Price (₹)",
        line=dict(color="green")
    ))

    fig.add_trace(go.Scatter(
        x=forecast_df["ds"],
        y=forecast_df["yhat"],
        mode="lines",
        name="Predicted Price (₹)",
        line=dict(color="blue", dash="dash")
    ))

    fig.add_trace(go.Scatter(
        x=forecast_df["ds"],
        y=forecast_df["yhat_upper"],
        mode="lines",
        name="Upper Bound",
        line=dict(color="lightblue"),
        opacity=0.2,
        showlegend=False
    ))

    fig.add_trace(go.Scatter(
        x=forecast_df["ds"],
        y=forecast_df["yhat_lower"],
        mode="lines",
        name="Lower Bound",
        line=dict(color="lightblue"),
        opacity=0.2,
        fill='tonexty',
        showlegend=False
    ))

    fig.update_layout(
        title_text=f"📊 Forecast vs Actual — {ticker.upper()}",
        xaxis_title="📅 Date",
        yaxis_title="💸 Price in ₹",
        hovermode="x unified",
        template="plotly_white"
    )

    return fig

# ⏱️ Intraday Forecast Plot
def plot_intraday_forecast(forecast_df, ticker, interval):
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=forecast_df["ds"],
        y=forecast_df["actual"],
        mode="lines",
        name="Actual Price",
        line=dict(color="green")
    ))

    fig.add_trace(go.Scatter(
        x=forecast_df["ds"],
        y=forecast_df["yhat"],
        mode="lines",
        name="Predicted Price",
        line=dict(color="blue", dash="dash")
    ))

    fig.update_layout(
        title_text=f"⏱️ Intraday Forecast — {ticker.upper()} ({interval})",
        xaxis_title="Time",
        yaxis_title="Price (₹)",
        hovermode="x unified",
        template="plotly_white"
    )

    return fig

# 🧮 RMSE Calculator
def compute_rmse(forecast_df):
    actual = forecast_df["actual"].dropna()
    predicted = forecast_df["yhat"].iloc[:len(actual)]
    return np.sqrt(mean_squared_error(actual, predicted))
