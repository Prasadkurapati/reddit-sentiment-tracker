from fastapi import FastAPI
from reddit_sentiment_tracker.data import fetch_reddit_json
from reddit_sentiment_tracker.features import extract_tickers
import pandas as pd

app = FastAPI(title="Reddit Sentiment API")

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
    """Fetch and analyze sentiment"""
    df = fetch_reddit_json(subreddit, limit)
    df['tickers'] = df['title'].apply(extract_tickers)
    
    # Filter posts with tickers
    posts_with_tickers = df[df['tickers'].apply(lambda x: len(x) > 0)]
    
    return {
        "analyzed_posts": len(df),
        "posts_with_tickers_count": len(posts_with_tickers),
        "posts_with_tickers": posts_with_tickers[['title', 'tickers', 'score']].to_dict('records')
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
