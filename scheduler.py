from apscheduler.schedulers.blocking import BlockingScheduler
from screener import rank_stocks
from utils.logger import log_picks
from utils.telegram_alert import send_telegram_message
from config import DEFAULT_ALLOCATION

def daily_job():
    tickers = ["RELIANCE.NS", "TCS.NS", "INFY.NS", "ICICIBANK.NS"]
    top = rank_stocks(tickers)
    per_stock = DEFAULT_ALLOCATION // len(top)
    log_picks(top)
    msg = "📈 Daily Forecast:\n" + "\n".join(f"{s[0]} → ₹{per_stock}" for s in top)
    send_telegram_message(msg)

def start_scheduler():
    scheduler = BlockingScheduler()
    scheduler.add_job(daily_job, 'cron', hour=9, minute=0)
    scheduler.start()
