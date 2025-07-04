import pandas as pd
from datetime import datetime
import os

def log_picks(picks, path="data/picks_log.csv"):
    df = pd.DataFrame(picks, columns=["Ticker", "Score", "Trend"])
    df["Date"] = datetime.now().strftime("%Y-%m-%d %H:%M")
    os.makedirs("data", exist_ok=True)
    df.to_csv(path, mode="a", header=not os.path.exists(path), index=False)
