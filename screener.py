import yfinance as yf
from utils.indicators import compute_rsi

def fetch_stock_data(ticker, period="6mo", interval="1d"):
    try:
        df = yf.download(ticker, period=period, interval=interval, progress=False)
        if df.empty or "Close" not in df.columns:
            return None
        df["SMA_20"] = df["Close"].rolling(20).mean()
        df["SMA_50"] = df["Close"].rolling(50).mean()
        df["RSI"] = compute_rsi(df["Close"])
        return df
    except Exception:
        return None

def score_stock(df):
    try:
        latest = df.iloc[-1]
        score = 0
        if latest["SMA_20"] > latest["SMA_50"]:
            score += 1
        if 40 < latest["RSI"] < 70:
            score += 1
        return score
    except:
        return 0

def compute_trend(df):
    try:
        return float(df["Close"].pct_change().rolling(5).mean().iloc[-1])
    except:
        return 0.0

def rank_stocks(tickers, top_n=5):
    results = []
    for ticker in tickers:
        df = fetch_stock_data(ticker)
        if df is None or df.empty:
            print(f"[SKIP] No data for {ticker}")
            continue
        score = score_stock(df)
        trend = compute_trend(df)
        results.append((ticker, score, trend))
    if not results:
        print("[ERROR] No valid tickers returned any data.")
    return sorted(results, key=lambda x: (x[1], x[2]), reverse=True)[:top_n]
