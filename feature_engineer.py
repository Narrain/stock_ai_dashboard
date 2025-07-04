def build_feature_vector(price_df, macro_df, sentiment_dict):
    df = price_df.copy()
    df["Returns"] = df["Close"].pct_change()
    df["SMA_20"] = df["Close"].rolling(20).mean()
    df["RSI"] = compute_rsi(df["Close"])
    df = df.join(macro_df, how="left")
    for k, v in sentiment_dict.items():
        df[k] = v
    return df.dropna()
