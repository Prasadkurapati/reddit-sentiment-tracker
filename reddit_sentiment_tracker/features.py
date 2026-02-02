import re
import pandas as pd

def extract_tickers(text):
    """Extract stock tickers from text using $SYMBOL or ALL CAPS pattern"""
    pattern = r'\$([A-Z]{1,5})\b|\b([A-Z]{2,5})\b'
    matches = re.findall(pattern, text)
    
    # Flatten tuples and remove empty strings
    tickers = [t for pair in matches for t in pair if t]
    
    # Filter out common words that aren't tickers
    common_words = {'I', 'A', 'IT', 'IS', 'BE', 'TO', 'OF', 'AND', 'THE', 'FOR', 
                   'ARE', 'BUT', 'NOT', 'YOU', 'ALL', 'CAN', 'HER', 'WAS', 'ONE',
                   'OUR', 'OUT', 'DAY', 'GET', 'HAS', 'HIM', 'HIS', 'HOW', 'MAN',
                   'NEW', 'NOW', 'OLD', 'SEE', 'TWO', 'WAY', 'WHO', 'BOY', 'DID',
                   'ITS', 'LET', 'PUT', 'SAY', 'SHE', 'TOO', 'USE', 'THAT', 'WITH',
                   'HAVE', 'THIS', 'WILL', 'YOUR', 'FROM', 'THEY', 'BEEN', 'CALL',
                   'WANT', 'WERE', 'SAID', 'TIME', 'THAN', 'THEM', 'WELL', 'ALSO',
                   'MY', 'GO', 'ME', 'UP', 'SO', 'IF', 'NO', 'DO', 'HE', 'WE',
                   'Q', 'K', 'C', 'R', 'W', 'J', 'V', 'Z', 'X', 'Y', 'F', 'P',
                   'ON', 'AN', 'AS', 'AT', 'BY', 'OR', 'GO', 'US', 'AM', 'TV',
                   'CEO', 'GDP', 'CPI', 'FED', 'IRS', 'SEC', 'IPO', 'ETF', 'GDP',
                   'IMO', 'LMAO', 'YOLO', 'DD', 'OTM', 'ITM', 'ATM', 'RH', 'WSB'}
    
    filtered = [t for t in tickers if t not in common_words and len(t) >= 2]
    
    return list(set(filtered))

df = pd.read_csv('raw_posts.csv')

df['tickers'] = df['title'].apply(extract_tickers)

print("Sample of posts with extracted tickers:")
print(df[['title', 'tickers']].head(10))

all_tickers = [t for tickers in df['tickers'] for t in tickers]
ticker_counts = pd.Series(all_tickers).value_counts().head(10)

print(f"\nTop 10 mentioned tickers:")
print(ticker_counts)

df.to_csv('posts_with_tickers.csv', index=False)
print(f"\nSaved to posts_with_tickers.csv")