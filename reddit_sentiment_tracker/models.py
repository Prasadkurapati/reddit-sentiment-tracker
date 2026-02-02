from transformers import pipeline
import pandas as pd

print("Loading sentiment model...")
classifier = pipeline(
    "sentiment-analysis",
    model="distilbert-base-uncased-finetuned-sst-2-english",
    truncation=True,
    max_length=512
)

df = pd.read_csv('posts_with_tickers.csv')

print(f"Analyzing {len(df)} posts...")

# sentiment analysis
results = classifier(df['title'].tolist(), batch_size=8)

# results to dataframe
df['sentiment_label'] = [r['label'] for r in results]
df['sentiment_score'] = [r['score'] for r in results]

# Map to numeric for aggregation
df['sentiment_value'] = df['sentiment_label'].map({'POSITIVE': 1, 'NEGATIVE': -1})

print("\nSample results:")
print(df[['title', 'tickers', 'sentiment_label', 'sentiment_score']].head(10))

# Aggregate by ticker
print("\n--- SENTIMENT BY STOCK ---")
all_mentions = []

for _, row in df.iterrows():
    for ticker in eval(row['tickers']) if isinstance(row['tickers'], str) else row['tickers']:
        all_mentions.append({
            'ticker': ticker,
            'sentiment': row['sentiment_value'],
            'confidence': row['sentiment_score'],
            'title': row['title']
        })

if all_mentions:
    mentions_df = pd.DataFrame(all_mentions)
    
    # Calculate average sentiment per ticker
    ticker_sentiment = mentions_df.groupby('ticker').agg({
        'sentiment': 'mean',
        'confidence': 'mean',
        'ticker': 'count'
    }).rename(columns={'ticker': 'mention_count'})
    
    ticker_sentiment = ticker_sentiment.sort_values('mention_count', ascending=False)
    print(ticker_sentiment.head(10))

df.to_csv('posts_with_sentiment.csv', index=False)
print(f"\nSaved to posts_with_sentiment.csv")