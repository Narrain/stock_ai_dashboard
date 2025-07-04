# Simple ML/logic for trend classification
def classify_trend(df):
    if df["SMA_20"].iloc[-1] > df["SMA_50"].iloc[-1]:
        return "Bullish"
    elif df["SMA_20"].iloc[-1] < df["SMA_50"].iloc[-1]:
        return "Bearish"
    else:
        return "Neutral"
