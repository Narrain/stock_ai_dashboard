from prophet import Prophet
from screener import fetch_stock_data
import pandas as pd

def forecast_intraday(ticker, interval="15m", period="1d"):
    df = fetch_stock_data(ticker, period=period, interval=interval)
    if df is None or df.empty or df["Close"].dropna().empty:
        return None

    df_prophet = df.reset_index()[["Datetime", "Close"]].dropna()
    df_prophet.columns = ["ds", "y"]

    try:
        model = Prophet(daily_seasonality=True)
        model.fit(df_prophet)
        future = model.make_future_dataframe(periods=12, freq=interval)
        forecast = model.predict(future)
        forecast["actual"] = df_prophet.set_index("ds")["y"].reindex(forecast["ds"]).values
        return forecast[["ds", "yhat", "yhat_lower", "yhat_upper", "actual"]]
    except Exception as e:
        print(f"[ERROR] Intraday forecast failed for {ticker}: {e}")
        return None
