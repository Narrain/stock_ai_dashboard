import streamlit as st
from predictor import predict_future
from model_trainer import train_model
from feature_engineer import build_feature_vector
from sentiment_engine import fetch_news_sentiment, fetch_macro_sentiment
from data_collector import get_price_data, get_macro_data

st.title("📈 AI-Powered Sentiment-Aware Stock Predictor")

ticker = st.text_input("Enter Ticker", "RELIANCE.NS")
price_df = get_price_data(ticker)
macro_df = get_macro_data()
sentiment = {
    "news_sentiment": fetch_news_sentiment(ticker),
    **fetch_macro_sentiment()
}
features = build_feature_vector(price_df, macro_df, sentiment)
model = train_model(features)
prediction = predict_future(model, features)

st.metric(label="📌 Next-Day Forecast", value=f"₹{prediction:.2f}")
st.line_chart(price_df["Close"])
