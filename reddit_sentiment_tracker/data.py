import requests
import pandas as pd
import json
from datetime import datetime

# Reddit JSON API (no auth required for read-only)
def fetch_reddit_json(subreddit, limit=50):
    url = f"https://www.reddit.com/r/{subreddit}/hot.json?limit={limit}"
    headers = {'User-Agent': 'Mozilla/5.0 (SentimentTracker/1.0)'}
    
    response = requests.get(url, headers=headers)
    data = response.json()
    
    posts = []
    for post in data['data']['children']:
        p = post['data']
        posts.append({
            'title': p['title'],
            'score': p['score'],
            'created_utc': datetime.fromtimestamp(p['created_utc']),
            'url': f"https://reddit.com{p['permalink']}",
            'num_comments': p['num_comments']
        })
    
    return pd.DataFrame(posts)

print("Fetching from r/wallstreetbets...")
df = fetch_reddit_json('wallstreetbets', limit=50)
print(f"Fetched {len(df)} posts")
print(df.head())
df.to_csv('raw_posts.csv', index=False)