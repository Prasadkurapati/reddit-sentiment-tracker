from transformers import pipeline
import pandas as pd

class SentimentAnalyzer:
    def __init__(self):
        print("Loading sentiment model...")
        self.classifier = pipeline(
            "sentiment-analysis",
            model="distilbert-base-uncased-finetuned-sst-2-english",
            truncation=True,
            max_length=512
        )
        print("Model loaded.")
    
    def analyze(self, texts):
        """Analyze sentiment of list of texts"""
        if isinstance(texts, str):
            texts = [texts]
        results = self.classifier(texts, batch_size=8)
        return results
    
    def analyze_dataframe(self, df, text_column='title'):
        """Add sentiment columns to dataframe"""
        results = self.analyze(df[text_column].tolist())
        df['sentiment_label'] = [r['label'] for r in results]
        df['sentiment_score'] = [r['score'] for r in results]
        df['sentiment_value'] = df['sentiment_label'].map({'POSITIVE': 1, 'NEGATIVE': -1})
        return df

# Backwards compatibility - keep old function for scripts
def analyze_sentiment(texts):
    analyzer = SentimentAnalyzer()
    return analyzer.analyze(texts)
