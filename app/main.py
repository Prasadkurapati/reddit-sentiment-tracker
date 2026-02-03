from fastapi import FastAPI
from reddit_sentiment_tracker.data import fetch_reddit_json
from reddit_sentiment_tracker.features import extract_tickers
from reddit_sentiment_tracker.models import SentimentAnalyzer
import pandas as pd

app = FastAPI(title="Reddit Sentiment API")

# Initialize sentiment analyzer (loads model once at startup)
print("Initializing API...")
analyzer = SentimentAnalyzer()

@app.get("/")
def root():
    return {"message": "Reddit Sentiment Tracker API", "version": "1.0"}

@app.get("/fetch")
def fetch_posts(subreddit: str = "wallstreetbets", limit: int = 50):
    """Fetch fresh posts from Reddit"""
    df = fetch_reddit_json(subreddit, limit)
    return {
        "posts": df.to_dict('records'),
        "count": len(df)
    }

@app.get("/analyze")
def analyze(subreddit: str = "wallstreetbets", limit: int = 50):
    """Fetch, extract tickers, and analyze sentiment"""
    # Fetch
    df = fetch_reddit_json(subreddit, limit)
    
    # Extract tickers
    df['tickers'] = df['title'].apply(extract_tickers)
    
    # Analyze sentiment
    df = analyzer.analyze_dataframe(df)
    
    # Aggregate by ticker
    ticker_data = []
    for _, row in df.iterrows():
        for ticker in row['tickers']:
            ticker_data.append({
                'ticker': ticker,
                'sentiment': row['sentiment_value'],
                'confidence': row['sentiment_score']
            })
    
    if ticker_data:
        ticker_df = pd.DataFrame(ticker_data)
        ticker_summary = ticker_df.groupby('ticker').agg({
            'sentiment': 'mean',
            'confidence': 'mean',
            'ticker': 'count'
        }).rename(columns={'ticker': 'mention_count', 'sentiment': 'avg_sentiment', 'confidence': 'avg_confidence'}).reset_index()
        ticker_list = ticker_summary.to_dict('records')
    else:
        ticker_list = []
    
    return {
        "analyzed_posts": len(df),
        "posts_with_tickers": len([t for t in df['tickers'] if len(t) > 0]),
        "ticker_sentiment": ticker_list,
        "sample_posts": df[['title', 'tickers', 'sentiment_label', 'sentiment_score']].head(5).to_dict('records')
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
