import streamlit as st
import requests
import pandas as pd
import os

API_URL = os.getenv("API_URL", "http://localhost:8000")

st.title("Reddit Sentiment Tracker")
st.markdown("Real-time stock sentiment from r/wallstreetbets")

st.sidebar.header("Settings")
subreddit = st.sidebar.text_input("Subreddit", "wallstreetbets")
limit = st.sidebar.slider("Number of posts", 10, 100, 50)

if st.sidebar.button("Analyze"):
    with st.spinner("Fetching and analyzing..."):
        try:
            response = requests.get(
                f"{API_URL}/analyze",
                params={"subreddit": subreddit, "limit": limit}
            )
            data = response.json()
            
            st.success(f"Analyzed {data['analyzed_posts']} posts")
            
            # Ticker sentiment table
            if data['ticker_sentiment']:
                st.subheader("Sentiment by Stock")
                df = pd.DataFrame(data['ticker_sentiment'])
                df['avg_sentiment'] = df['avg_sentiment'].map({1.0: 'Bullish', -1.0: 'Bearish', 0.0: 'Neutral'})
                df.columns = ['Ticker', 'Sentiment', 'Confidence', 'Mentions']
                st.dataframe(df.sort_values('Mentions', ascending=False))
            else:
                st.warning("No tickers found in posts")
                    
        except Exception as e:
            st.error(f"Error: {e}")
            st.info(f"Make sure the API is running at {API_URL}")
else:
    st.info("Click 'Analyze' to fetch data")