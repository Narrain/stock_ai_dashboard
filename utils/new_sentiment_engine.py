from textblob import TextBlob
import requests
import pandas as pd

def fetch_news_sentiment(ticker):
    # Replace with your NewsAPI key
    url = f"https://newsapi.org/v2/everything?q={ticker}&apiKey=YOUR_KEY"
    articles = requests.get(url).json().get("articles", [])
    sentiments = [TextBlob(a["title"]).sentiment.polarity for a in articles if a.get("title")]
    return sum(sentiments) / len(sentiments) if sentiments else 0.0

def fetch_macro_sentiment():
    # Placeholder: you can scrape RBI, Fed, IMF, etc.
    return {
        "inflation_sentiment": -0.2,
        "interest_rate_sentiment": -0.1,
        "geopolitical_sentiment": 0.3
    }
