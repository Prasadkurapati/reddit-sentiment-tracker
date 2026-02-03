import streamlit as st
import requests
import pandas as pd

st.title("Reddit Sentiment Tracker")
st.markdown("Real-time stock sentiment from r/wallstreetbets")

# Sidebar
st.sidebar.header("Settings")
subreddit = st.sidebar.text_input("Subreddit", "wallstreetbets")
limit = st.sidebar.slider("Number of posts", 10, 100, 50)

# Fetch button
if st.sidebar.button("Analyze"):
    with st.spinner("Fetching and analyzing..."):
        try:
            response = requests.get(
                f"http://localhost:8000/analyze",
                params={"subreddit": subreddit, "limit": limit}
            )
            data = response.json()
            
            st.success(f"Analyzed {data['analyzed_posts']} posts")
            
            # Ticker sentiment table
            if data['ticker_sentiment']:
                st.subheader("Sentiment by Stock")
                df = pd.DataFrame(data['ticker_sentiment'])
                df['avg_sentiment'] = df['avg_sentiment'].map({1.0: 'Bullish', -1.0: 'Bearish'})
                df.columns = ['Ticker', 'Sentiment', 'Confidence', 'Mentions']
                st.dataframe(df.sort_values('Mentions', ascending=False))
            else:
                st.warning("No tickers found in posts")
                    
        except Exception as e:
            st.error(f"Error: {e}")
else:
    st.info("Click 'Analyze' to fetch data")
