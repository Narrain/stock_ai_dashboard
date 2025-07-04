from prophet import Prophet
from screener import fetch_stock_data

def forecast_prices(ticker, horizon="30d"):
    df = fetch_stock_data(ticker, period="1y")
    if df is None or df.empty or df["Close"].dropna().empty:
        return None

    df_prophet = df.reset_index()[["Date", "Close"]].dropna()
    df_prophet.columns = ["ds", "y"]

    try:
        model = Prophet(daily_seasonality=True)
        model.fit(df_prophet)
        future = model.make_future_dataframe(periods=int(horizon[:-1]))
        forecast = model.predict(future)
        forecast["actual"] = df_prophet.set_index("ds")["y"].reindex(forecast["ds"]).values
        return forecast[["ds", "yhat", "yhat_lower", "yhat_upper", "actual"]]
    except Exception as e:
        print(f"[ERROR] Forecast failed for {ticker}: {e}")
        return None
