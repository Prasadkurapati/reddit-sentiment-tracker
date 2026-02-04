from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import pandas as pd

class SentimentAnalyzer:
    def __init__(self):
        print("Loading VADER sentiment analyzer...")
        self.analyzer = SentimentIntensityAnalyzer()
        print("VADER loaded.")
    
    def analyze(self, texts):
        """Analyze sentiment of list of texts"""
        if isinstance(texts, str):
            texts = [texts]
        
        results = []
        for text in texts:
            scores = self.analyzer.polarity_scores(text)
            compound = scores['compound']
            if compound >= 0.05:
                label = 'POSITIVE'
            elif compound <= -0.05:
                label = 'NEGATIVE'
            else:
                label = 'NEUTRAL'
            
            results.append({
                'label': label,
                'score': abs(compound)
            })
        return results
    
    def analyze_dataframe(self, df, text_column='title'):
        """Add sentiment columns to dataframe"""
        results = self.analyze(df[text_column].tolist())
        df['sentiment_label'] = [r['label'] for r in results]
        df['sentiment_score'] = [r['score'] for r in results]
        df['sentiment_value'] = df['sentiment_label'].map({
            'POSITIVE': 1, 'NEGATIVE': -1, 'NEUTRAL': 0
        })
        return df

def analyze_sentiment(texts):
    analyzer = SentimentAnalyzer()
    return analyzer.analyze(texts)
