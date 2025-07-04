import yfinance as yf
import pandas as pd

def get_price_data(ticker, period="2y"):
    df = yf.download(ticker, period=period)
    return df[["Close", "Volume"]]

def get_macro_data():
    gold = yf.download("GC=F", period="2y")["Close"].rename("Gold")
    oil = yf.download("CL=F", period="2y")["Close"].rename("Oil")
    usd = yf.download("USDINR=X", period="2y")["Close"].rename("USDINR")
    return pd.concat([gold, oil, usd], axis=1)
