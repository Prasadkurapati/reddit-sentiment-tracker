# Reddit Sentiment Tracker

[![Live Demo](https://img.shields.io/badge/Live%20Demo-Render-green)](https://reddit-sentiment-tracker-464p.onrender.com)

[![Python](https://img.shields.io/badge/Python-3.11-blue)](https://python.org)

[![FastAPI](https://img.shields.io/badge/FastAPI-0.128.0-teal)](https://fastapi.tiangolo.com)

[![Docker](https://img.shields.io/badge/Docker-Enabled-blue)](https://docker.com)

Real-time stock sentiment analysis from Reddit discussions using NLP. Deployed on Render free tier.

---

## Live Demo

- **API**: https://reddit-sentiment-tracker-464p.onrender.com

- **API Docs**: https://reddit-sentiment-tracker-464p.onrender.com/docs

- **Example**: https://reddit-sentiment-tracker-464p.onrender.com/analyze?limit=10

---

## Architecture

    Reddit API
        ↓
    FastAPI
        ↓
    VADER NLP
        ↓
    JSON Response
        ↓
    Docker
        ↓
    Render Cloud

---

## Quick Start

#### Local Development

    git clone https://github.com/Prasadkurapati/reddit-sentiment-tracker.git
    cd reddit-sentiment-tracker
    pip install -r requirements.txt
    uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
    curl "http://localhost:8000/analyze?limit=10"

## Docker

    docker build -t reddit-sentiment .
    docker run -p 8000:8000 reddit-sentiment
    curl "http://localhost:8000/analyze?limit=10"

## API Endpoints

| Endpoint | Method | Parameters | Description |

| ---------- | ------ | -------------------- | -------------------------------- |

| `/` | GET | - | Health check |

| `/analyze` | GET | `subreddit`, `limit` | Fetch posts + sentiment analysis |

| `/fetch` | GET | `subreddit`, `limit` | Fetch raw posts only |

## Example Response

    {
        "analyzed_posts": 10,
        "posts_with_tickers": 3,
        "ticker_sentiment": [
        {
          "ticker": "AAPL",
          "avg_sentiment": -1.0,
          "avg_confidence": 0.95,
          "mention_count": 2
        }
      ]
    }

## Tech Stack

| Component   | Technology         |
| ----------- | ------------------ |
| Backend     | FastAPI (Python)   |
| NLP Engine  | VADER Sentiment    |
| Data Source | Reddit JSON API    |
| Container   | Docker             |
| Cloud       | Render (Free Tier) |
| Versioning  | DVC (data)         |

## Project Structure

    reddit-sentiment-tracker/
    ├── app/
    │   ├── main.py
    │   └── dashboard.py
    ├── reddit_sentiment_tracker/
    │   ├── data.py
    │   ├── features.py
    │   └── models.py
    ├── Dockerfile
    ├── requirements.txt
    ├── README.md
    └── LICENSE

## Features

- Real-time sentiment analysis
- Stock ticker extraction
- REST API endpoints
- Dockerized deployment
- Cloud hosted on Render

## Performance

- Latency: ~1–2 seconds for 50 posts
- Memory: <512MB (runs on Render free tier)
- Cold Start: ~30 seconds (free tier limitation)
- Uptime: 24/7 with auto-sleep after 15 min inactivity

## Limitations

- Reddit API rate limits (60 requests/minute)
- Free tier spins down after 15 minutes inactivity
- VADER is rule-based (faster but less nuanced than BERT)
- No persistent database (data not stored between requests)

## Future Improvements

- [ ] Add PostgreSQL for historical data
- [ ] Implement Redis caching
- [ ] Add more subreddits (r/stocks, r/investing)
- [ ] WebSocket for real-time updates
- [ ] Historical sentiment charts

## Local Dashboard

Run Streamlit dashboard locally (not deployed due to memory constraints):

    streamlit run app/dashboard.py

Access at: http://localhost:8501

#### License

MIT License - see LICENSE file

Built by Prasad Kurapati | Live Demo
