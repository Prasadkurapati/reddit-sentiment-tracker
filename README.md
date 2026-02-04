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

├── LICENSE
├── Makefile
├── README.md
├── data/
│   ├── external/
│   ├── interim/
│   ├── processed/
│   └── raw/
├── docs/
├── models/
├── notebooks/
├── pyproject.toml
├── references/
├── reports/
│   └── figures/
├── requirements.txt
├── setup.cfg
└── reddit_sentiment_tracker/
    ├── __init__.py
    ├── config.py
    ├── data.py          # Reddit API scraper
    ├── features.py      # Ticker extraction
    ├── models.py        # VADER sentiment
    ├── database.py      # SQLite storage
    └── modeling/
        ├── __init__.py
        ├── predict.py
        └── train.py

app/
├── main.py             # FastAPI endpoints
└── dashboard.py        # Streamlit UI

Dockerfile              # Container config
