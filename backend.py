# backend.py

from sentiment import analyze_sentiment
from database import insert_sentiment

# Process text and analyze sentiment, then store results
def process_text(text):
    sentiment, score = analyze_sentiment(text)
    insert_sentiment(text, sentiment, score)
    return sentiment, score
