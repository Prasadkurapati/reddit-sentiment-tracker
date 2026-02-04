# Reddit Sentiment Tracker

Real-time stock sentiment analysis from Reddit discussions.

## What It Does

- **Scrapes** hot posts from r/wallstreetbets (stock trading community)
- **Extracts** stock tickers ($AAPL, TSLA, NVDA, etc.) from post titles
- **Analyzes sentiment** (Bullish/Bearish/Neutral) using VADER NLP
- **Returns aggregated data** showing which stocks are trending and market mood

## Example Use Case

Input: "GME to the moon! 🚀 TSLA earnings beat expectations"
Output:

- GME: Bullish (confidence: 0.85), 15 mentions
- TSLA: Bullish (confidence: 0.72), 8 mentions

## Tech Stack

- **Data**: Reddit JSON API, PRAW
- **NLP**: VADER Sentiment (lightweight, rule-based)
- **API**: FastAPI (Python)
- **Container**: Docker
- **Cloud**: Render (free tier)
- **Versioning**: DVC for datasets

## Live Demo

- **API Root**: https://reddit-sentiment-tracker-464p.onrender.com
- **API Docs**: https://reddit-sentiment-tracker-464p.onrender.com/docs
- **Example Query**: https://reddit-sentiment-tracker-464p.onrender.com/analyze?limit=10

## Project Structure

```text
reddit-sentiment-tracker/
├── app/
│   ├── main.py              # FastAPI endpoints
│   └── dashboard.py         # Streamlit UI
├── reddit_sentiment_tracker/
│   ├── data.py              # Reddit API scraper
│   ├── features.py          # Ticker extraction
│   ├── models.py            # VADER sentiment
│   └── database.py          # SQLite storage
├── data/                    # DVC-tracked datasets
├── models/                  # Saved models
├── notebooks/               # Jupyter notebooks
├── Dockerfile               # Container config
├── requirements.txt
└── README.md
```

## Key Files

| File                                   | Description                       |
| -------------------------------------- | --------------------------------- |
| `app/main.py`                          | FastAPI routes (/fetch, /analyze) |
| `reddit_sentiment_tracker/data.py`     | Reddit JSON API client            |
| `reddit_sentiment_tracker/features.py` | Regex ticker extraction           |
| `reddit_sentiment_tracker/models.py`   | VADER sentiment analysis          |
| `Dockerfile`                           | Multi-service container setup     |
